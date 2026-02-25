"""
Training script for improved MTR model on Waymo dataset.
"""

import torch
import datetime
import argparse
import os

from model import MTR
from train_utils import WaymoDataset, load_config, collate_fn
from torch.utils.data import DataLoader

import lightning.pytorch as pl
from lightning.pytorch.callbacks import ModelCheckpoint, LearningRateMonitor
from lightning.pytorch.loggers import CSVLogger


def train(cfg_file, ckpt_path=None):
    print("=" * 60)
    print("MTR Training on Waymo Open Motion Dataset")
    print("=" * 60)
    
    torch.set_float32_matmul_precision('high')
    cfg = load_config(cfg_file)
    pl.seed_everything(cfg.get('seed', 42))
    
    # Data paths
    train_path = cfg.get('train_data_path', [])
    val_path = cfg.get('val_data_path', [])
    
    print(f"\nData paths:")
    print(f"  Training: {train_path}")
    print(f"  Validation: {val_path}")
    
    # Subset configuration
    train_subset = cfg.get('train_subset_fraction', 1.0)
    val_subset = cfg.get('val_subset_fraction', 1.0)
    
    print(f"\nSubset configuration:")
    print(f"  Training: {train_subset * 100:.1f}%")
    print(f"  Validation: {val_subset * 100:.1f}%")
    
    # Create datasets
    print("\n" + "-" * 60)
    print("Loading datasets...")
    print("-" * 60)
    
    train_dataset = WaymoDataset(
        train_path,
        subset_fraction=train_subset,
        random_seed=cfg.get('seed', 42),
        max_map_range=cfg.get('max_map_range', 150.0),
        max_polylines=cfg.get('max_polylines', 256),
    )
    
    val_dataset = WaymoDataset(
        val_path,
        subset_fraction=val_subset,
        random_seed=cfg.get('seed', 42),
        max_map_range=cfg.get('max_map_range', 150.0),
        max_polylines=cfg.get('max_polylines', 256),
    )
    
    print(f"\nDataset sizes:")
    print(f"  Training: {len(train_dataset):,}")
    print(f"  Validation: {len(val_dataset):,}")
    
    # Verify data format
    print("\nVerifying data format...")
    sample = train_dataset[0]
    for key, val in sample.items():
        print(f"  {key}: {val.shape}, dtype={val.dtype}")
    
    # Create DataLoaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=cfg.get('batch_size', 32),
        shuffle=True,
        num_workers=cfg.get('num_workers', 8),
        pin_memory=True,
        drop_last=True,
        collate_fn=collate_fn,
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=cfg.get('batch_size', 32),
        shuffle=False,
        num_workers=cfg.get('num_workers', 8),
        pin_memory=True,
        drop_last=False,
        collate_fn=collate_fn,
    )
    
    print(f"\nBatches per epoch:")
    print(f"  Training: {len(train_loader)}")
    print(f"  Validation: {len(val_loader)}")
    
    # Create model
    print("\n" + "-" * 60)
    print("Initializing model...")
    print("-" * 60)
    print(f"  Encoder layers: {cfg.get('encoder_layers', 4)}")
    print(f"  Decoder layers: {cfg.get('decoder_layers', 4)}")
    print(f"  Learning rate: {cfg.get('lr', 0.0001)}")
    print(f"  Batch size: {cfg.get('batch_size', 32)}")
    
    model = MTR(cfg)
    
    # Output directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_root = cfg.get('output_path', 'output')
    if isinstance(output_root, list):
        output_root = output_root[0]
    
    subset_str = f"_subset{int(train_subset * 100)}pct" if train_subset < 1.0 else ""
    output_path = f"{output_root}/{cfg.get('model_name', 'MTR')}_{timestamp}{subset_str}"
    os.makedirs(output_path, exist_ok=True)
    
    print(f"\nOutput: {output_path}")
    print(f"GPUs: {torch.cuda.device_count()}")
    if torch.cuda.is_available():
        print(f"Device: {torch.cuda.get_device_name(0)}")
    
    # Logger
    logger = CSVLogger(output_path, name='MTR', version=1, flush_logs_every_n_steps=100)
    
    # Trainer
    print("\n" + "-" * 60)
    print("Setting up trainer...")
    print("-" * 60)
    
    trainer = pl.Trainer(
        max_epochs=cfg.get('epochs', 30),
        devices=-1,
        accelerator='gpu' if torch.cuda.is_available() else 'cpu',
        enable_progress_bar=True,
        logger=logger,
        enable_model_summary=True,
        gradient_clip_val=1.0,
        gradient_clip_algorithm="norm",
        num_sanity_val_steps=2,
        log_every_n_steps=100,
        callbacks=[
            ModelCheckpoint(
                dirpath=output_path,
                save_top_k=3,
                save_last=True,
                save_weights_only=False,
                monitor='val/loss',
                mode='min',
                filename='epoch={epoch:02d}-val_loss={val/loss:.4f}',
                every_n_epochs=1,
            ),
            LearningRateMonitor(logging_interval='step'),
        ],
    )
    
    # Train
    print("\n" + "=" * 60)
    print("STARTING TRAINING")
    print("=" * 60)
    print(f"Epochs: {cfg.get('epochs', 30)}")
    print(f"Steps per epoch: ~{len(train_loader)}")
    print("=" * 60 + "\n")
    
    try:
        trainer.fit(model, train_loader, val_loader, ckpt_path=args.ckpt)
        print("\n" + "=" * 60)
        print("TRAINING COMPLETED!")
        print(f"Checkpoints saved to: {output_path}")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        
    except Exception as e:
        print(f"\nTraining failed: {e}")
        raise
        
    finally:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("\nGPU memory released")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train MTR on Waymo Dataset')
    parser.add_argument('--cfg', type=str, default='hparams.yaml', help='Config file path')
    parser.add_argument('--ckpt', type=str, default=None, help='Resume from checkpoint')
    args = parser.parse_args()
    
    train(args.cfg)