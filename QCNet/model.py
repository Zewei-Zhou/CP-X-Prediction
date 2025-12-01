import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import lightning.pytorch as pl
from torch.nn.functional import smooth_l1_loss, cross_entropy


class MTR(pl.LightningModule):
    def __init__(
        self,
        cfg: dict,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.cfg = cfg
        self.encoder = Encoder(cfg['encoder_layers'])
        self.predictor = Predictor(cfg['decoder_layers'])

    ################### Training Setup ###################
    def configure_optimizers(self):
        params_to_update = []
        for param in self.parameters():
            if param.requires_grad == True:
                params_to_update.append(param)              
        
        assert len(params_to_update) > 0, 'No parameters to update'
        
        optimizer = torch.optim.AdamW(
            params_to_update, 
            lr=self.cfg['lr'],
            weight_decay=self.cfg['weight_decay']
        )
        
        lr_warmpup_step = self.cfg['lr_warmup_step']
        lr_step_freq = self.cfg['lr_step_freq']
        lr_step_gamma = self.cfg['lr_step_gamma']

        def lr_update(step, warmup_step, step_size, gamma):
            if step < warmup_step:
                # warm up lr
                lr_scale = 1 - (warmup_step - step) / warmup_step * 0.99
            else:
                n = (step - warmup_step) // step_size
                lr_scale = gamma ** n

            if lr_scale < 1e-2:
                lr_scale = 1e-2

            return lr_scale
        
        scheduler = torch.optim.lr_scheduler.LambdaLR(
            optimizer,
            lr_lambda=lambda step: lr_update(
                step, 
                lr_warmpup_step, 
                lr_step_freq,
                lr_step_gamma,
            )
        )
        
        return [optimizer], [{"scheduler": scheduler, "interval": "step"}]
        
    def forward(self, inputs):
        # Encode scene
        encoder_outputs = self.encoder(inputs)

        # predict trajectories
        predictor_outputs = self.predictor(encoder_outputs)

        return predictor_outputs
    
    def forward_and_get_loss(self, batch, prefix=''):
        # data inputs
        log_dict = {}
     
        encoder_outputs = self.encoder(batch)
        predictor_outputs = self.predictor(encoder_outputs)
        ground_truth = batch['fut_gt_trajs']
        ground_truth_valid = batch['fut_valid']

        # Calculate loss        
        predict_trajs = predictor_outputs['aux_trajs'] * ground_truth_valid[..., None]
        total_loss = smooth_l1_loss(predict_trajs, ground_truth)
        level_K = self.cfg['decoder_layers']

        for k in range(level_K):
            traj_loss_mean, score_loss_mean, weighted_ade_loss = self.predict_loss(predictor_outputs[f"layer_{k}_trajs"],
                                                                                   predictor_outputs[f"layer_{k}_scores"],
                                                                                   ground_truth[:, 0], ground_truth_valid[:, 0])
            pred_loss = traj_loss_mean + 0.1 * score_loss_mean + 0.1 * weighted_ade_loss
            total_loss += pred_loss
        
        # Calculate metrics
        trajs = predictor_outputs[f"layer_{self.cfg['decoder_layers']-1}_trajs"]
        scores = predictor_outputs[f"layer_{self.cfg['decoder_layers']-1}_scores"]

        pred_ade, pred_fde = self.calculate_metrics_predict(
            trajs, scores, ground_truth[:, 0], ground_truth_valid[:, 0]
        )
            
        log_dict.update({
            prefix+'weighted_ade_loss': weighted_ade_loss.item(),
            prefix+'traj_loss': traj_loss_mean.item(),
            prefix+'score_loss': score_loss_mean.item(),
            prefix+'weighted_ADE': pred_ade,
            prefix+'weighted_FDE': pred_fde,
        })
        
        log_dict[prefix+'loss'] = total_loss.item()
        
        return total_loss, log_dict
    
    def training_step(self, batch, batch_idx):
        loss, log_dict = self.forward_and_get_loss(batch, prefix='train/')
        self.log_dict(log_dict, 
                      on_step=True, on_epoch=False, sync_dist=True,
                      prog_bar=True)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        loss, log_dict = self.forward_and_get_loss(batch, prefix='val/')
        self.log_dict(log_dict, 
                      on_step=False, on_epoch=True, sync_dist=True,
                      prog_bar=True)
        
        return loss

    def predict_loss(
        self, trajs, scores, agents_future,
        agents_future_valid
    ):
        num_batch = trajs.shape[0]
        traj_mask = agents_future_valid.bool() # [B, T]
        trajs_gt = agents_future[:, :, :2] # [B, T, 2]
        
        # Select the best trajectory
        dist = torch.norm(trajs[:, :, :, :2] - trajs_gt[:, None, :, :2], dim=-1) # [B, Q, T]
        dist = dist * traj_mask[:, None, :] # [B, Q, T]
        idx = torch.argmin(dist.mean(-1), dim=-1) # [B,]
        trajs_select = trajs[torch.arange(num_batch), idx] # [B, T, 2]
        
        # Calculate the trajectory loss
        mu = trajs_select[..., :2] # [B, T, 2]

        '''cov = trajs_select[..., 2:] # [B, T, 2]
        log_std_x = torch.clamp(cov[..., 0], -1, 3)
        log_std_y = torch.clamp(cov[..., 1], -1, 3)
        std_x = torch.exp(log_std_x)
        std_y = torch.exp(log_std_y)
        dx = trajs_gt[..., 0] - mu[..., 0]
        dy = trajs_gt[..., 1] - mu[..., 1]
        traj_loss = log_std_x + log_std_y + 0.5 * (torch.square(dx/std_x) + torch.square(dy/std_y))
        traj_loss = traj_loss * traj_mask # [B, T]'''

        traj_loss = smooth_l1_loss(mu, trajs_gt, reduction='none') # [B, T, 2]
        traj_loss = traj_loss * traj_mask[..., None] # [B, T, 2]
        traj_loss = traj_loss.sum(-1) # [B, T]
        
        # Calculate the score loss
        # scores # [B, Q]
        score_loss = cross_entropy(scores, idx, reduction='none', label_smoothing=0.2) # [B,]
        score_loss = score_loss * traj_mask.sum(-1).bool() # [B,]
        
        # Calculate the mean loss
        traj_loss_mean = torch.mean(traj_loss)
        score_loss_mean = torch.mean(score_loss)
        
        # auxilary loss
        weights = F.softmax(scores, dim=1) # [B, Q]
        weighted_loss = dist * weights[:, :, None] # [B, Q, T]
        weighted_ade_loss = torch.mean(weighted_loss)

        return traj_loss_mean, score_loss_mean, weighted_ade_loss
    
    @torch.no_grad()
    def calculate_metrics_predict(self,
            trajs, scores, agents_future, agents_future_valid,
        ):
        # trajs [B, Q, T, 2]
        gt = agents_future[:, :, :2] # [B, T, 2]
        gt_mask = agents_future_valid.bool() # [B, T]
            
        mse = torch.norm(trajs[..., :2  ] - gt[:, None], dim=-1) # [B, Q, T]
        mse = mse * gt_mask[:, None] # [B, Q, T]
        weights = F.softmax(scores, dim=1) # [B, Q]
        weighted_mse = torch.sum(mse * weights[:, :, None], dim=1) # [B, T]

        weighted_ADE = weighted_mse.sum() / gt_mask.sum().clamp(min=1)
        weighted_FDE = weighted_mse[..., -1].sum() / gt_mask[..., -1].sum().clamp(min=1)
            
        return weighted_ADE.item(), weighted_FDE.item()


class AgentEncoder(nn.Module):
    def __init__(self, d_model=256, d_ffn=1024, n_heads=8, dropout=0.1):
        super().__init__()
        # UPDATED: Changed from 22 object types to 5 (4 Waymo types + 1 padding)
        # Waymo types: 0=Vehicle, 1=Pedestrian, 2=Cyclist, 3=Other
        self.type_embed = nn.Embedding(5, d_model, padding_idx=0)
        self.time_embed = nn.Embedding(11, d_model) # 11 history steps
        self.mlp_encoder = nn.Sequential(nn.Linear(5, d_model//2), nn.ReLU(), nn.Linear(d_model//2, d_model))
        self.transformer_encoder = nn.TransformerEncoderLayer(d_model, n_heads, d_ffn, dropout,
                                                              activation='gelu', batch_first=True)
        self.register_buffer('time', torch.arange(11).long())

    def forward(self, object_trajs, valid_mask):
        # type embedding
        obj_type = object_trajs[:, :, -1, -1].long()
        type_embed = self.type_embed(obj_type)

        # mlp encoding
        obj_embed = self.mlp_encoder(object_trajs[..., :-1]) 
  
        # transformer encoding
        obj_embed = obj_embed.view(-1, obj_embed.shape[-2], obj_embed.shape[-1])
        obj_embed = obj_embed + self.time_embed(self.time)

        valid_mask = valid_mask.view(-1, valid_mask.shape[-1])
        encoded_objects = self.transformer_encoder(obj_embed, src_key_padding_mask=valid_mask)
        encoded_objects = encoded_objects[:, -1].reshape(object_trajs.shape[0], object_trajs.shape[1], -1)
        encoded_objects = encoded_objects + type_embed

        return encoded_objects


class Encoder(nn.Module):
    def __init__(self, layers=6):
        super().__init__()
        self.agent_encoder = AgentEncoder()
        self.map_encoder = MapEncoder()
        self.relation_encoder = FourierEmbedding(input_dim=3)
        transformer_layer = nn.TransformerEncoderLayer(d_model=256, nhead=8, dim_feedforward=1024, 
                                                       dropout=0.1, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(transformer_layer, num_layers=layers, 
                                                         enable_nested_tensor=False)

    def forward(self, inputs):
        # initial encoding
        agents = inputs['hist_trajs']
        agents_valid = inputs['hist_valid']
        maps = inputs['maps']

        mask = agents_valid.logical_not()
        mask[:, :, 0] = False
        encoded_agents = self.agent_encoder(agents, mask)
        encoded_maps = self.map_encoder(maps)

        relations = agents[:, None, :, -1, :3] # x, y, heading
        relations = torch.cat([relations, maps[:, None, :, 0, :3]], dim=-2)
        relations[:, :, 0] = relations[:, :, 0] + 1e-3
        encoded_relations = self.relation_encoder(relations)
        
        # transformer encoding
        encoder_outputs = {}
        agents_mask = agents_valid[:, :, -1]
        inputs = torch.cat([encoded_agents, encoded_maps], dim=1)
        masks = torch.cat([agents_mask, torch.ones_like(maps[:, :, 0, 0], dtype=torch.bool)], dim=-1)
        masks = masks.logical_not()
        encodings = self.transformer_encoder(inputs, src_key_padding_mask=masks)
        
        # store outputs
        encoder_outputs['encodings'] = encodings
        encoder_outputs['masks'] = masks
        encoder_outputs['relation_encodings'] = encoded_relations
        encoder_outputs['agents'] = agents

        return encoder_outputs
    

class MapEncoder(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.point = nn.Sequential(nn.Linear(3, d_model//2), nn.ReLU(), nn.Linear(d_model//2, d_model))
        self.type_embed = nn.Embedding(5, d_model, padding_idx=0) # 4 map polyline types + 1 padding

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        # inputs [B, M, W, 4]  (changed from 5 to 4 in comment, actual dim is still compatible)
        output = self.point(inputs[..., :3]) 
        output = torch.max(output, dim=-2).values # max pooling on W

        polyline_type = inputs[:, :, 0, -1].long()
        type_embed = self.type_embed(polyline_type)
        output = output + type_embed

        return output


class Predictor(nn.Module):
    def __init__(self, layers=6):
        super().__init__()     
        self._agents_len = 5   
        self._num_modalities = 3
        self.attention_layers = nn.ModuleList([CrossTransformer() for _ in range(layers)])
        self.anchor_encoder = nn.Embedding(self._num_modalities, 256)
        self.register_buffer('modality', torch.arange(self._num_modalities).long())
        
        self.traj_decoder = nn.Sequential(nn.Linear(256, 256), nn.ELU(), nn.Dropout(0.1),
                                          nn.Linear(256, 80*2))
        self.score_decoder = nn.Sequential(nn.Linear(256, 128), nn.ELU(), nn.Dropout(0.1),
                                           nn.Linear(128, 1))
        self.aux_traj_decoder = nn.Sequential(nn.Linear(256, 256), nn.ELU(), nn.Dropout(0.1),
                                              nn.Linear(256, 80*2))
        
    def forward(self, inputs):
        anchors_points = self.modality[None, :]
        anchors = self.anchor_encoder(anchors_points)    
        encodings = inputs['encodings']
        query = encodings[:, :1] + anchors # center agent   
        relations = inputs['relation_encodings'].squeeze(1)
        masks = inputs['masks']
        current_states = inputs['agents'][:, :, -1, :2]

        aux_trajs = self.aux_traj_decoder(encodings[:, :self._agents_len])
        aux_trajs = aux_trajs.reshape(-1, self._agents_len, 80, 2)
        aux_trajs = aux_trajs + current_states[:, :, None]
        outputs = {'aux_trajs': aux_trajs}

        for i, layer in enumerate(self.attention_layers):
            query_content = layer(query, encodings, relations, masks)
            trajs = self.traj_decoder(query_content).reshape(-1, query.shape[1], 80, 2)
            scores = self.score_decoder(query_content).squeeze(-1)
            outputs[f"layer_{i}_trajs"] = trajs
            outputs[f"layer_{i}_scores"] = scores
            query = query + query_content

        return outputs
    

class FourierEmbedding(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, num_freq_bands=64):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim

        self.freqs = nn.Embedding(input_dim, num_freq_bands) if input_dim != 0 else None

        self.mlps = nn.ModuleList(
            [nn.Sequential(
                nn.Linear(num_freq_bands * 2 + 1, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ReLU(inplace=True),
                nn.Linear(hidden_dim, hidden_dim),
            ) for _ in range(input_dim)])
        
        self.to_out = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, continuous_inputs: torch.Tensor) -> torch.Tensor:
        x = continuous_inputs.unsqueeze(-1) * self.freqs.weight * 2 * torch.pi
        x = torch.cat([x.cos(), x.sin(), continuous_inputs.unsqueeze(-1)], dim=-1)
        x = torch.stack([self.mlps[i](x[:, :, :, i]) for i in range(self.input_dim)]).sum(dim=0)

        return self.to_out(x)


class CrossTransformer(nn.Module):
    def __init__(self, heads=8, dim=256, dropout=0.1, d_ffn=1024):
        super().__init__()
        self.cross_attention = nn.MultiheadAttention(dim, heads, dropout, batch_first=True)
        self.norm_1 = nn.LayerNorm(dim)
        self.norm_2 = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(nn.Linear(dim, d_ffn), nn.GELU(), nn.Dropout(dropout), 
                                 nn.Linear(d_ffn, dim), nn.Dropout(dropout))

    def forward(self, query, key, relations=None, mask=None):
        # add relations to key and value
        key = key + relations
        value = key

        # cross attention
        attention_output, _ = self.cross_attention(query, key, value, key_padding_mask=mask)
        attention_output = self.norm_1(attention_output)
        output = self.norm_2(self.ffn(attention_output) + attention_output)

        return output  