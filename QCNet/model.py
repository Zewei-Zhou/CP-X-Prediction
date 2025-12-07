import torch
import torch.nn as nn
import lightning.pytorch as pl


class FourierEmbedding(nn.Module):
    def __init__(self, input_dim, d_model, num_freq_bands=64):
        super().__init__()
        self.num_freq_bands = num_freq_bands
        self.d_model = d_model
        
        # Create frequency bands
        freq_bands = 2.0 ** torch.linspace(0, num_freq_bands-1, num_freq_bands)
        self.register_buffer('freq_bands', freq_bands)
        
        # Project concatenated sins and cosines to d_model
        self.proj = nn.Linear(input_dim * num_freq_bands * 2, d_model)
    
    def forward(self, x):
        # x: (..., input_dim)
        # Expand for frequency bands
        x_freq = x.unsqueeze(-1) * self.freq_bands  # (..., input_dim, num_freq_bands)
        
        # Compute sin and cos
        x_sin = torch.sin(2 * 3.14159 * x_freq)
        x_cos = torch.cos(2 * 3.14159 * x_freq)
        
        # Concatenate and flatten
        x_encoded = torch.cat([x_sin, x_cos], dim=-1)  # (..., input_dim, num_freq_bands*2)
        x_encoded = x_encoded.flatten(start_dim=-2)  # (..., input_dim * num_freq_bands * 2)
        
        return self.proj(x_encoded)


class MTR(pl.LightningModule):
    def __init__(self, config):
        super().__init__()
        self.save_hyperparameters()
        self.config = config
        
        self.encoder = Encoder(config)
        self.predictor = Predictor(config)
        
    def forward_and_get_loss(self, batch, prefix='train/'):
        eps = 1e-7  # Epsilon for numerical stability
        
        hist_trajs = batch['hist_trajs']  # (B, N, 11, 6)
        hist_valid = batch['hist_valid']  # (B, N, 11)
        fut_gt_trajs = batch['fut_gt_trajs']  # (B, N, 80, 2)
        fut_valid = batch['fut_valid']  # (B, N, 80)
        maps = batch['maps']  # (B, M, 10, 4)

        B, N = hist_trajs.shape[:2]
        
        # Forward pass through model
        encoder_outputs = self.encoder(batch)
        predictions = self.predictor(encoder_outputs, batch)
        
        pred_trajs = predictions['trajectories']  # (B, N, K, 80, 2)
        pred_scores = predictions['scores']      # (B, N, K)
        
        K = pred_trajs.shape[2]  # number of modes
        
        # Expand gt for all modes
        gt_trajs = fut_gt_trajs.unsqueeze(2).expand(-1, -1, K, -1, -1)  # (B, N, K, 80, 2)
        valid_mask = fut_valid.unsqueeze(2).expand(-1, -1, K, -1)  # (B, N, K, 80)
        
        # Compute displacement errors for all modes
        displacement = pred_trajs - gt_trajs  # (B, N, K, 80, 2)
        # FIXED: Add epsilon inside sqrt for numerical stability
        distance = torch.sqrt((displacement ** 2).sum(dim=-1) + eps)  # (B, N, K, 80)
        
        # Apply mask
        masked_distance = distance * valid_mask  # (B, N, K, 80)
        
        # ADE for each mode
        ade = masked_distance.mean(dim=-1)  # (B, N, K)
        
        # FIXED: Weighted ADE with safe division
        weighted_ade_loss = (ade * valid_mask[:, :, :, 0]).sum() / valid_mask[:, :, :, 0].sum().clamp(min=1)
        
        # Winner-takes-all: find best mode for each agent
        best_mode_ades, best_mode_idx = ade.min(dim=2)  # (B, N)
        
        # Trajectory regression loss (only on best mode)
        traj_loss = best_mode_ades.mean()
        
        # Mode classification loss (cross-entropy)
        # Target: best mode for each agent
        log_probs = torch.log_softmax(pred_scores, dim=-1)  # (B, N, K)
        
        # Gather log probs for best modes
        best_log_probs = log_probs.gather(2, best_mode_idx.unsqueeze(-1)).squeeze(-1)  # (B, N)
        score_loss = -best_log_probs.mean()
        
        # FIXED: FDE with epsilon in sqrt
        fde = torch.sqrt(((pred_trajs[:, :, :, -1] - gt_trajs[:, :, :, -1]) ** 2).sum(dim=-1) + eps)  # (B, N, K)
        best_mode_fde = fde.gather(2, best_mode_idx.unsqueeze(-1)).squeeze(-1)  # (B, N)
        
        # FIXED: Weighted FDE with safe division
        weighted_FDE = (fde * valid_mask[:, :, :, -1]).sum() / valid_mask[:, :, :, -1].sum().clamp(min=1)
        
        # Total loss
        loss = traj_loss + score_loss
        
        # Safety check for NaN/Inf
        if torch.isnan(loss) or torch.isinf(loss):
            print(f"WARNING: Invalid loss at step {self.global_step}")
            print(f"  traj_loss: {traj_loss}, score_loss: {score_loss}")
            print(f"  pred_trajs: min={pred_trajs.min():.3f}, max={pred_trajs.max():.3f}")
            loss = torch.tensor(1.0, device=loss.device, requires_grad=True)
        
        # Create log dict
        log_dict = {
            f'{prefix}loss': loss,
            f'{prefix}traj_loss': traj_loss,
            f'{prefix}score_loss': score_loss,
            f'{prefix}weighted_ADE': weighted_ade_loss,
            f'{prefix}weighted_FDE': weighted_FDE,
            f'{prefix}weighted_ade_loss': weighted_ade_loss,
        }
        
        return loss, log_dict
    
    def training_step(self, batch, batch_idx):
        try:
            loss, log_dict = self.forward_and_get_loss(batch, prefix='train/')
            
            # Extra safety check
            if torch.isnan(loss):
                print(f"NaN loss at step {self.global_step}, skipping batch")
                return None
            
            self.log_dict(log_dict, prog_bar=True, sync_dist=True)
            return loss
            
        except Exception as e:
            print(f"Error in training step {self.global_step}: {e}")
            return None
    
    def validation_step(self, batch, batch_idx):
        loss, log_dict = self.forward_and_get_loss(batch, prefix='val/')
        self.log_dict(log_dict, prog_bar=True, sync_dist=True)
        return loss
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.config['lr'],
            weight_decay=self.config.get('weight_decay', 0.01)
        )
        
        # Learning rate scheduler with warmup
        def lr_lambda(step):
            warmup_steps = self.config.get('lr_warmup_step', 500)
            if step < warmup_steps:
                return step / warmup_steps
            else:
                # Exponential decay after warmup
                decay_step = (step - warmup_steps) // self.config.get('lr_step_freq', 200)
                return self.config.get('lr_step_gamma', 0.98) ** decay_step
        
        scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'interval': 'step',
                'frequency': 1
            }
        }


class AgentEncoder(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.type_embedding = nn.Embedding(5, d_model)  # 5 object types
        self.pos_embedding = FourierEmbedding(input_dim=2, d_model=d_model)
        self.vel_embedding = FourierEmbedding(input_dim=2, d_model=d_model)
        self.heading_embedding = FourierEmbedding(input_dim=1, d_model=d_model)
        
        self.temporal_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=8, batch_first=True),
            num_layers=2
        )
    
    def forward(self, hist_trajs, hist_valid):
        # hist_trajs: (B, N, 11, 6) - [x, y, heading, vx, vy, type]
        B, N, T, _ = hist_trajs.shape
        
        # Extract features
        pos = hist_trajs[..., :2]  # (B, N, 11, 2)
        heading = hist_trajs[..., 2:3]  # (B, N, 11, 1)
        vel = hist_trajs[..., 3:5]  # (B, N, 11, 2)
        obj_type = hist_trajs[..., 5].long()  # (B, N, 11)
        
        # Embed each feature
        pos_emb = self.pos_embedding(pos)
        heading_emb = self.heading_embedding(heading)
        vel_emb = self.vel_embedding(vel)
        type_emb = self.type_embedding(obj_type)
        
        # Combine embeddings
        combined = pos_emb + heading_emb + vel_emb + type_emb  # (B, N, 11, d_model)
        
        # Flatten batch and agent dims for transformer
        combined_flat = combined.view(B * N, T, -1)
        
        # Create attention mask from validity
        valid_flat = hist_valid.view(B * N, T)
        mask = ~valid_flat.bool()
        
        # Temporal encoding
        encoded = self.temporal_encoder(combined_flat, src_key_padding_mask=mask)
        
        # Take last timestep
        agent_features = encoded[:, -1]  # (B*N, d_model)
        agent_features = agent_features.view(B, N, -1)
        
        return agent_features


class MapEncoder(nn.Module):
    def __init__(self, d_model=256):
        super().__init__()
        self.type_embedding = nn.Embedding(5, d_model)  # 5 map element types
        self.point_embedding = FourierEmbedding(input_dim=3, d_model=d_model)
        
        self.polyline_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=8, batch_first=True),
            num_layers=2
        )
    
    def forward(self, maps):
        # maps: (B, M, 10, 4) - [x, y, direction, type]
        B, M, P, _ = maps.shape
        
        # Extract features
        points = maps[..., :3]  # (B, M, 10, 3) - x, y, direction
        map_type = maps[..., 3].long()  # (B, M, 10)
        
        # Embed
        point_emb = self.point_embedding(points)
        type_emb = self.type_embedding(map_type)
        
        combined = point_emb + type_emb  # (B, M, 10, d_model)
        
        # Flatten for transformer
        combined_flat = combined.view(B * M, P, -1)
        
        # Encode each polyline
        encoded = self.polyline_encoder(combined_flat)
        
        # Max pool over points
        polyline_features = encoded.max(dim=1)[0]  # (B*M, d_model)
        polyline_features = polyline_features.view(B, M, -1)
        
        return polyline_features


class Encoder(nn.Module):
    def __init__(self, config, d_model=256):
        super().__init__()
        self.agent_encoder = AgentEncoder(d_model)
        self.map_encoder = MapEncoder(d_model)
        
        # Cross-attention between agents and map
        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=d_model, nhead=8, batch_first=True),
            num_layers=config.get('encoder_layers', 4)
        )
    
    def forward(self, batch):
        hist_trajs = batch['hist_trajs']
        hist_valid = batch['hist_valid']
        maps = batch['maps']
        
        # Encode agents
        agent_features = self.agent_encoder(hist_trajs, hist_valid)  # (B, N, d_model)
        
        # Encode map
        map_features = self.map_encoder(maps)  # (B, M, d_model)
        
        # Concatenate agents and map
        B, N = agent_features.shape[:2]
        M = map_features.shape[1]
        
        combined = torch.cat([agent_features, map_features], dim=1)  # (B, N+M, d_model)
        
        # Create mask (all agents and map elements are valid)
        masks = torch.zeros(B, N + M, dtype=torch.bool, device=combined.device)
        
        # Global encoding with transformer
        encodings = self.transformer_encoder(combined, src_key_padding_mask=masks)
        
        # Split back into agent and map encodings
        agent_encodings = encodings[:, :N]
        map_encodings = encodings[:, N:]
        
        return {
            'agent_encodings': agent_encodings,
            'map_encodings': map_encodings
        }


class Predictor(nn.Module):
    def __init__(self, config, d_model=256, num_modes=3, future_steps=80):
        super().__init__()
        self.num_modes = num_modes
        self.future_steps = future_steps
        
        # Mode-specific decoders
        self.decoder = nn.TransformerDecoder(
            nn.TransformerDecoderLayer(d_model=d_model, nhead=8, batch_first=True),
            num_layers=config.get('decoder_layers', 4)
        )
        
        # Prediction heads
        self.traj_head = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.ReLU(),
            nn.Linear(d_model, future_steps * 2)  # Predict x, y for each timestep
        )
        
        self.score_head = nn.Linear(d_model, 1)
        
        # Mode queries (learnable)
        self.mode_queries = nn.Parameter(torch.randn(num_modes, d_model))
    
    def forward(self, encoder_outputs, batch):
        agent_encodings = encoder_outputs['agent_encodings']  # (B, N, d_model)
        map_encodings = encoder_outputs['map_encodings']  # (B, M, d_model)
        
        B, N, d_model = agent_encodings.shape
        
        # Expand mode queries for batch and agents
        queries = self.mode_queries.unsqueeze(0).unsqueeze(0).expand(B, N, -1, -1)  # (B, N, K, d_model)
        
        # Flatten for decoding
        queries_flat = queries.reshape(B * N, self.num_modes, d_model)
        agent_flat = agent_encodings.unsqueeze(2).expand(-1, -1, self.num_modes, -1).reshape(B * N, self.num_modes, d_model)
        
        # Decode
        memory = torch.cat([agent_encodings, map_encodings], dim=1)  # (B, N+M, d_model)
        memory_flat = memory.unsqueeze(1).expand(-1, N, -1, -1).reshape(B * N, -1, d_model)
        
        decoded = self.decoder(queries_flat, memory_flat)  # (B*N, K, d_model)
        
        # Predict trajectories
        traj_flat = self.traj_head(decoded)  # (B*N, K, future_steps*2)
        trajectories = traj_flat.view(B, N, self.num_modes, self.future_steps, 2)
        
        # Predict scores
        score_flat = self.score_head(decoded).squeeze(-1)  # (B*N, K)
        scores = score_flat.view(B, N, self.num_modes)
        
        return {
            'trajectories': trajectories,
            'scores': scores
        }