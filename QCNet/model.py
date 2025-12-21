"""
Improved MTR Model for Waymo Dataset
Based on mentor's architecture with fixes for:
1. Missing current position offset in predictions
2. Loss dilution from invalid timesteps
3. Proper masking in all loss terms
4. Better numerical stability
"""

import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import lightning.pytorch as pl
from torch.nn.functional import smooth_l1_loss, cross_entropy


class MTR(pl.LightningModule):
    def __init__(self, cfg: dict):
        super().__init__()
        self.save_hyperparameters()
        self.cfg = cfg
        self.encoder = Encoder(cfg.get('encoder_layers', 4))
        self.predictor = Predictor(cfg.get('decoder_layers', 4))

    def configure_optimizers(self):
        params_to_update = [p for p in self.parameters() if p.requires_grad]
        assert len(params_to_update) > 0, 'No parameters to update'
        
        optimizer = torch.optim.AdamW(
            params_to_update, 
            lr=self.cfg['lr'],
            weight_decay=self.cfg.get('weight_decay', 0.01)
        )
        
        lr_warmup_step = self.cfg.get('lr_warmup_step', 500)
        lr_step_freq = self.cfg.get('lr_step_freq', 200)
        lr_step_gamma = self.cfg.get('lr_step_gamma', 0.98)

        def lr_update(step):
            if step < lr_warmup_step:
                lr_scale = 1 - (lr_warmup_step - step) / lr_warmup_step * 0.99
            else:
                n = (step - lr_warmup_step) // lr_step_freq
                lr_scale = lr_step_gamma ** n
            return max(lr_scale, 1e-2)
        
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_update)
        return [optimizer], [{"scheduler": scheduler, "interval": "step"}]
        
    def forward(self, inputs):
        encoder_outputs = self.encoder(inputs)
        predictor_outputs = self.predictor(encoder_outputs)
        return predictor_outputs
    
    def forward_and_get_loss(self, batch, prefix=''):
        log_dict = {}
        eps = 1e-7
     
        encoder_outputs = self.encoder(batch)
        predictor_outputs = self.predictor(encoder_outputs)
        ground_truth = batch['fut_gt_trajs']  # [B, N, T, 2]
        ground_truth_valid = batch['fut_valid']  # [B, N, T]

        # ========== Auxiliary Loss (all agents) ==========
        aux_trajs = predictor_outputs['aux_trajs']  # [B, N, T, 2]
        
        # FIXED: Proper masked loss calculation
        aux_mask = ground_truth_valid[..., None].float()  # [B, N, T, 1]
        aux_loss_raw = smooth_l1_loss(aux_trajs, ground_truth, reduction='none')  # [B, N, T, 2]
        aux_loss = (aux_loss_raw * aux_mask).sum() / aux_mask.sum().clamp(min=1)
        
        total_loss = aux_loss
        
        # ========== Main Prediction Loss (center agent only) ==========
        level_K = self.cfg.get('decoder_layers', 4)
        center_gt = ground_truth[:, 0]  # [B, T, 2]
        center_valid = ground_truth_valid[:, 0]  # [B, T]

        for k in range(level_K):
            trajs = predictor_outputs[f"layer_{k}_trajs"]  # [B, Q, T, 2]
            scores = predictor_outputs[f"layer_{k}_scores"]  # [B, Q]
            
            traj_loss, score_loss, weighted_ade = self.predict_loss(
                trajs, scores, center_gt, center_valid
            )
            
            # Loss weighting
            pred_loss = traj_loss + 0.1 * score_loss + 0.1 * weighted_ade
            total_loss = total_loss + pred_loss
        
        # ========== Metrics (using final layer predictions) ==========
        final_trajs = predictor_outputs[f"layer_{level_K-1}_trajs"]
        final_scores = predictor_outputs[f"layer_{level_K-1}_scores"]

        pred_ade, pred_fde = self.calculate_metrics(
            final_trajs, final_scores, center_gt, center_valid
        )
            
        log_dict.update({
            f'{prefix}loss': total_loss.item(),
            f'{prefix}aux_loss': aux_loss.item(),
            f'{prefix}traj_loss': traj_loss.item(),
            f'{prefix}score_loss': score_loss.item(),
            f'{prefix}weighted_ade_loss': weighted_ade.item(),
            f'{prefix}weighted_ADE': pred_ade,
            f'{prefix}weighted_FDE': pred_fde,
        })
        
        return total_loss, log_dict
    
    def training_step(self, batch, batch_idx):
        loss, log_dict = self.forward_and_get_loss(batch, prefix='train/')
        
        if not torch.isfinite(loss):
            print(f"WARNING: Invalid loss at step {self.global_step}, skipping")
            return None
            
        self.log_dict(log_dict, on_step=True, on_epoch=False, sync_dist=True, prog_bar=True)
        return loss
    
    def validation_step(self, batch, batch_idx):
        loss, log_dict = self.forward_and_get_loss(batch, prefix='val/')
        
        if not torch.isfinite(loss):
            return None
            
        self.log_dict(log_dict, on_step=False, on_epoch=True, sync_dist=True, prog_bar=True)
        return loss

    def predict_loss(self, trajs, scores, gt_future, gt_valid):
        """
        Compute trajectory and score losses for center agent predictions.
        
        Args:
            trajs: [B, Q, T, 2] - Q mode predictions
            scores: [B, Q] - mode scores
            gt_future: [B, T, 2] - ground truth
            gt_valid: [B, T] - validity mask
        """
        B, Q, T, _ = trajs.shape
        eps = 1e-7
        
        traj_mask = gt_valid.bool()  # [B, T]
        gt = gt_future[..., :2]  # [B, T, 2]
        
        # Compute distance for all modes
        dist = torch.norm(trajs - gt[:, None], dim=-1)  # [B, Q, T]
        dist_masked = dist * traj_mask[:, None].float()  # [B, Q, T]
        
        # Select best mode (winner-takes-all)
        valid_count = traj_mask.sum(dim=-1, keepdim=True).clamp(min=1).float()  # [B, 1]
        ade_per_mode = dist_masked.sum(dim=-1) / valid_count  # [B, Q]
        best_idx = torch.argmin(ade_per_mode, dim=-1)  # [B]
        
        # Get best trajectory
        batch_idx = torch.arange(B, device=trajs.device)
        best_trajs = trajs[batch_idx, best_idx]  # [B, T, 2]
        
        # ========== Trajectory Loss ==========
        # FIXED: Properly masked mean
        traj_loss_raw = smooth_l1_loss(best_trajs, gt, reduction='none')  # [B, T, 2]
        traj_loss_masked = traj_loss_raw * traj_mask[..., None].float()  # [B, T, 2]
        traj_loss = traj_loss_masked.sum() / (traj_mask.sum() * 2).clamp(min=1)
        
        # ========== Score Loss ==========
        # FIXED: Weight by valid samples
        has_valid = traj_mask.any(dim=-1).float()  # [B] - 1 if sample has any valid timestep
        score_loss_raw = cross_entropy(scores, best_idx, reduction='none', label_smoothing=0.2)  # [B]
        score_loss = (score_loss_raw * has_valid).sum() / has_valid.sum().clamp(min=1)
        
        # ========== Weighted ADE Loss ==========
        weights = F.softmax(scores, dim=1)  # [B, Q]
        weighted_dist = (dist_masked * weights[:, :, None]).sum(dim=1)  # [B, T]
        weighted_ade = weighted_dist.sum() / traj_mask.sum().clamp(min=1)

        return traj_loss, score_loss, weighted_ade
    
    @torch.no_grad()
    def calculate_metrics(self, trajs, scores, gt_future, gt_valid):
        """Calculate weighted ADE and FDE metrics."""
        gt = gt_future[..., :2]  # [B, T, 2]
        gt_mask = gt_valid.bool()  # [B, T]
        
        # Distance for all modes
        dist = torch.norm(trajs[..., :2] - gt[:, None], dim=-1)  # [B, Q, T]
        dist_masked = dist * gt_mask[:, None].float()
        
        # Weight by mode probabilities
        weights = F.softmax(scores, dim=1)  # [B, Q]
        weighted_dist = (dist_masked * weights[:, :, None]).sum(dim=1)  # [B, T]
        
        # ADE: average over all valid timesteps
        weighted_ADE = weighted_dist.sum() / gt_mask.sum().clamp(min=1)
        
        # FDE: only final timestep
        final_mask = gt_mask[:, -1]  # [B]
        weighted_FDE = weighted_dist[:, -1].sum() / final_mask.sum().clamp(min=1)
        
        return weighted_ADE.item(), weighted_FDE.item()


class AgentEncoder(nn.Module):
    def __init__(self, d_model=256, d_ffn=1024, n_heads=8, dropout=0.1):
        super().__init__()
        # FIXED: Reduced type embedding to match Waymo types (0-4)
        self.type_embed = nn.Embedding(8, d_model, padding_idx=0)  # 8 covers all Waymo types with margin
        self.time_embed = nn.Embedding(11, d_model)  # 11 history steps
        self.mlp_encoder = nn.Sequential(
            nn.Linear(5, d_model // 2), 
            nn.ReLU(), 
            nn.Linear(d_model // 2, d_model)
        )
        self.transformer_encoder = nn.TransformerEncoderLayer(
            d_model, n_heads, d_ffn, dropout,
            activation='gelu', batch_first=True
        )
        self.register_buffer('time_indices', torch.arange(11).long())

    def forward(self, object_trajs, valid_mask):
        """
        Args:
            object_trajs: [B, N, T, 6] - [x, y, heading, vx, vy, type]
            valid_mask: [B, N, T] - True for INVALID positions (for transformer mask)
        """
        B, N, T, _ = object_trajs.shape
        
        # Type embedding from last timestep
        obj_type = object_trajs[:, :, -1, -1].long().clamp(0, 7)  # [B, N]
        type_embed = self.type_embed(obj_type)  # [B, N, d_model]

        # MLP encoding of trajectory features (all except type)
        obj_embed = self.mlp_encoder(object_trajs[..., :-1])  # [B, N, T, d_model]
  
        # Reshape for transformer: [B*N, T, d_model]
        obj_embed = obj_embed.view(B * N, T, -1)
        obj_embed = obj_embed + self.time_embed(self.time_indices)

        # Prepare mask: [B*N, T]
        mask = valid_mask.view(B * N, T)
        
        # FIXED: Ensure at least one valid position per sequence
        all_invalid = mask.all(dim=-1)
        if all_invalid.any():
            mask = mask.clone()
            mask[all_invalid, -1] = False  # Make last timestep valid
        
        # Transformer encoding
        encoded = self.transformer_encoder(obj_embed, src_key_padding_mask=mask)
        
        # Take last timestep and add type embedding
        encoded = encoded[:, -1].view(B, N, -1)  # [B, N, d_model]
        encoded = encoded + type_embed

        return encoded


class MapEncoder(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.point_encoder = nn.Sequential(
            nn.Linear(3, d_model // 2), 
            nn.ReLU(), 
            nn.Linear(d_model // 2, d_model)
        )
        self.type_embed = nn.Embedding(8, d_model, padding_idx=0)  # Map polyline types

    def forward(self, inputs):
        """
        Args:
            inputs: [B, M, W, 4] - [x, y, direction, type]
        """
        # Point features
        output = self.point_encoder(inputs[..., :3])  # [B, M, W, d_model]
        output = torch.max(output, dim=-2).values  # Max pool over points: [B, M, d_model]

        # Type embedding
        polyline_type = inputs[:, :, 0, -1].long().clamp(0, 7)  # [B, M]
        type_embed = self.type_embed(polyline_type)  # [B, M, d_model]
        
        return output + type_embed


class Encoder(nn.Module):
    def __init__(self, layers=4):
        super().__init__()
        self.agent_encoder = AgentEncoder()
        self.map_encoder = MapEncoder()
        self.relation_encoder = FourierEmbedding(input_dim=3)
        
        transformer_layer = nn.TransformerEncoderLayer(
            d_model=256, nhead=8, dim_feedforward=1024, 
            dropout=0.1, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(
            transformer_layer, num_layers=layers, 
            enable_nested_tensor=False
        )

    def forward(self, inputs):
        agents = inputs['hist_trajs']  # [B, N, T, 6]
        agents_valid = inputs['hist_valid']  # [B, N, T]
        maps = inputs['maps']  # [B, M, W, 4]

        # Prepare mask for agent encoder (True = invalid for transformer)
        agent_mask = agents_valid.logical_not()
        agent_mask[:, :, 0] = False  # Ensure first timestep is always "valid"
        
        # Encode
        encoded_agents = self.agent_encoder(agents, agent_mask)  # [B, N, d_model]
        encoded_maps = self.map_encoder(maps)  # [B, M, d_model]

        # Relation encoding (positions relative to each element)
        B, N = agents.shape[:2]
        M = maps.shape[1]
        
        # Get current positions: [B, N, 3] and [B, M, 3]
        agent_poses = agents[:, :, -1, :3]  # x, y, heading at last timestep
        map_poses = maps[:, :, 0, :3]  # x, y, direction at first point
        
        # Combined poses for relation encoding: [B, N+M, 3]
        all_poses = torch.cat([agent_poses, map_poses], dim=1)
        
        # Add small offset to prevent division issues
        all_poses = all_poses + 1e-3
        
        # Encode relations: [B, N+M, d_model]
        encoded_relations = self.relation_encoder(all_poses)
        
        # Combine encodings
        combined = torch.cat([encoded_agents, encoded_maps], dim=1)  # [B, N+M, d_model]
        
        # Mask: agents use validity at last timestep, maps always valid
        agents_final_valid = agents_valid[:, :, -1]  # [B, N]
        maps_valid = torch.ones(B, M, dtype=torch.bool, device=maps.device)
        combined_mask = torch.cat([agents_final_valid, maps_valid], dim=-1)  # [B, N+M]
        combined_mask = combined_mask.logical_not()  # Invert for transformer (True = invalid)
        
        # Global transformer encoding
        encodings = self.transformer_encoder(combined, src_key_padding_mask=combined_mask)
        
        return {
            'encodings': encodings,
            'masks': combined_mask,
            'relation_encodings': encoded_relations,
            'agents': agents,
            'num_agents': N
        }


class Predictor(nn.Module):
    def __init__(self, layers=4, num_modes=3, future_steps=80):
        super().__init__()
        self._num_agents = 5
        self._num_modes = num_modes
        self._future_steps = future_steps
        
        self.attention_layers = nn.ModuleList([CrossTransformer() for _ in range(layers)])
        self.mode_embed = nn.Embedding(num_modes, 256)
        self.register_buffer('mode_indices', torch.arange(num_modes).long())
        
        # Trajectory decoders
        self.traj_decoder = nn.Sequential(
            nn.Linear(256, 256), nn.ELU(), nn.Dropout(0.1),
            nn.Linear(256, future_steps * 2)
        )
        self.score_decoder = nn.Sequential(
            nn.Linear(256, 128), nn.ELU(), nn.Dropout(0.1),
            nn.Linear(128, 1)
        )
        self.aux_traj_decoder = nn.Sequential(
            nn.Linear(256, 256), nn.ELU(), nn.Dropout(0.1),
            nn.Linear(256, future_steps * 2)
        )
        
    def forward(self, encoder_outputs):
        encodings = encoder_outputs['encodings']  # [B, N+M, d_model]
        masks = encoder_outputs['masks']  # [B, N+M]
        relations = encoder_outputs['relation_encodings']  # [B, N+M, d_model]
        agents = encoder_outputs['agents']  # [B, N, T, 6]
        num_agents = encoder_outputs['num_agents']
        
        B = encodings.shape[0]
        
        # Current positions for all agents
        current_states = agents[:, :, -1, :2]  # [B, N, 2]
        center_state = current_states[:, :1]  # [B, 1, 2] - just center agent
        
        # ========== Auxiliary Predictions (all agents) ==========
        agent_encodings = encodings[:, :num_agents]  # [B, N, d_model]
        aux_trajs = self.aux_traj_decoder(agent_encodings)
        aux_trajs = aux_trajs.reshape(B, num_agents, self._future_steps, 2)
        # IMPORTANT: Add current positions
        aux_trajs = aux_trajs + current_states[:, :, None, :]
        
        outputs = {'aux_trajs': aux_trajs}
        
        # ========== Main Predictions (center agent, multi-modal) ==========
        # Initialize query with center agent encoding + mode embeddings
        center_encoding = encodings[:, :1]  # [B, 1, d_model]
        mode_embeds = self.mode_embed(self.mode_indices)  # [Q, d_model]
        query = center_encoding + mode_embeds[None, :, :]  # [B, Q, d_model]
        
        for i, layer in enumerate(self.attention_layers):
            query_out = layer(query, encodings, relations, masks)
            
            # Decode trajectories
            trajs = self.traj_decoder(query_out)  # [B, Q, future_steps*2]
            trajs = trajs.reshape(B, self._num_modes, self._future_steps, 2)
            
            # FIX: Add current position to make predictions relative
            trajs = trajs + center_state[:, :, None, :]  # [B, Q, T, 2]
            
            # Decode scores
            scores = self.score_decoder(query_out).squeeze(-1)  # [B, Q]
            
            outputs[f"layer_{i}_trajs"] = trajs
            outputs[f"layer_{i}_scores"] = scores
            
            # Update query with residual
            query = query + query_out

        return outputs


class FourierEmbedding(nn.Module):
    """Learnable Fourier features for continuous inputs."""
    
    def __init__(self, input_dim, hidden_dim=256, num_freq_bands=64):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_freq_bands = num_freq_bands

        # Learnable frequencies (more robust than fixed)
        self.freqs = nn.Embedding(input_dim, num_freq_bands)
        
        # Per-dimension MLPs
        self.mlps = nn.ModuleList([
            nn.Sequential(
                nn.Linear(num_freq_bands * 2 + 1, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.ReLU(inplace=True),
                nn.Linear(hidden_dim, hidden_dim),
            ) for _ in range(input_dim)
        ])
        
        self.to_out = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, x):
        """
        Args:
            x: [..., input_dim] continuous values
        Returns:
            [..., hidden_dim] embeddings
        """
        # Fourier features: [..., input_dim, num_freq_bands]
        x_freq = x.unsqueeze(-1) * self.freqs.weight * 2 * torch.pi
        
        # Sin/cos encoding with original value: [..., input_dim, num_freq_bands*2+1]
        x_encoded = torch.cat([x_freq.cos(), x_freq.sin(), x.unsqueeze(-1)], dim=-1)
        
        # Process each dimension and sum
        outputs = []
        for i in range(self.input_dim):
            outputs.append(self.mlps[i](x_encoded[..., i, :]))
        x_out = torch.stack(outputs, dim=0).sum(dim=0)
        
        return self.to_out(x_out)


class CrossTransformer(nn.Module):
    """Cross-attention layer with relation encoding."""
    
    def __init__(self, heads=8, dim=256, dropout=0.1, d_ffn=1024):
        super().__init__()
        self.cross_attention = nn.MultiheadAttention(dim, heads, dropout, batch_first=True)
        self.norm_1 = nn.LayerNorm(dim)
        self.norm_2 = nn.LayerNorm(dim)
        self.ffn = nn.Sequential(
            nn.Linear(dim, d_ffn), 
            nn.GELU(), 
            nn.Dropout(dropout), 
            nn.Linear(d_ffn, dim), 
            nn.Dropout(dropout)
        )

    def forward(self, query, key, relations=None, mask=None):
        """
        Args:
            query: [B, Q, dim] - mode queries
            key: [B, N+M, dim] - scene encodings
            relations: [B, N+M, dim] - positional relations
            mask: [B, N+M] - True for invalid positions
        """
        # Add relations to key and value
        if relations is not None:
            key = key + relations
        value = key

        # Cross attention
        attn_out, _ = self.cross_attention(query, key, value, key_padding_mask=mask)
        attn_out = self.norm_1(attn_out)
        
        # FFN with residual
        output = self.norm_2(self.ffn(attn_out) + attn_out)
        
        return output