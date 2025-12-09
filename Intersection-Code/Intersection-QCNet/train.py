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


def train(cfg_file):
    print("="*60)
    print("QCNet Training on Waymo Open Motion Dataset")
    print("="*60)
    
    torch.set_float32_matmul_precision('high')    
    cfg = load_config(cfg_file)
    pl.seed_everything(cfg['seed'])
    
    print(f"\nData paths:")
    print(f"  - Training: {cfg['train_data_path']}")
    print(f"  - Validation: {cfg['val_data_path']}")
    
    # Get subset fractions (default to 1.0 if not specified)
    train_subset = cfg.get('train_subset_fraction', 1.0)
    val_subset = cfg.get('val_subset_fraction', 1.0)
    
    print(f"\nData subset configuration:")
    print(f"  - Training subset: {train_subset*100:.1f}% of dataset")
    print(f"  - Validation subset: {val_subset*100:.1f}% of dataset")
    
    if train_subset < 1.0 or val_subset < 1.0:
        print(f"\n⚠️  Using subset for pretraining (not full dataset)")
    
    # Create Waymo datasets
    print("\n" + "-"*60)
    print("Loading Training Data...")
    print("-"*60)
    train_dataset = WaymoDataset(
        cfg['train_data_path'],
        subset_fraction=train_subset,
        random_seed=cfg['seed']
    )
    
    print("\n" + "-"*60)
    print("Loading Validation Data...")
    print("-"*60)
    val_dataset = WaymoDataset(
        cfg['val_data_path'],
        subset_fraction=val_subset,
        random_seed=cfg['seed']
    )
    
    # Summary
    print("\n" + "="*60)
    print("Dataset Summary:")
    print("="*60)
    print(f"Training samples: {len(train_dataset):,}")
    print(f"Validation samples: {len(val_dataset):,}")
    print(f"Total samples: {len(train_dataset) + len(val_dataset):,}")
    
    if train_subset < 1.0:
        full_train_size = int(len(train_dataset) / train_subset)
        print(f"\n💡 Using {len(train_dataset):,} out of ~{full_train_size:,} available training samples")
    
    # Verify data format
    print("\nVerifying data format...")
    test_sample = train_dataset[0]
    print(f"  ✓ hist_trajs: {test_sample['hist_trajs'].shape}")
    print(f"  ✓ hist_valid: {test_sample['hist_valid'].shape}")
    print(f"  ✓ fut_gt_trajs: {test_sample['fut_gt_trajs'].shape}")
    print(f"  ✓ fut_valid: {test_sample['fut_valid'].shape}")
    print(f"  ✓ maps: {test_sample['maps'].shape}")

    # Create DataLoaders
    print("\n" + "-"*60)
    print("Creating DataLoaders...")
    print("-"*60)
    train_loader = DataLoader(
        train_dataset, 
        batch_size=cfg['batch_size'], 
        pin_memory=True, 
        num_workers=cfg['num_workers'],
        shuffle=True,
        drop_last=True,
        collate_fn=collate_fn
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=cfg['batch_size'],
        pin_memory=True, 
        num_workers=cfg['num_workers'],
        shuffle=False,
        drop_last=False,
        collate_fn=collate_fn
    )
    
    print(f"Training batches per epoch: {len(train_loader)}")
    print(f"Validation batches: {len(val_loader)}")
    
    # Create model
    print("\n" + "-"*60)
    print("Initializing Model...")
    print("-"*60)
    print(f"  - Encoder layers: {cfg['encoder_layers']}")
    print(f"  - Decoder layers: {cfg['decoder_layers']}")
    print(f"  - Learning rate: {cfg['lr']}")
    print(f"  - Batch size: {cfg['batch_size']}")
    
    model = MTR(cfg)
    
    # Setup output directory
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_root = cfg.get('output_path', 'output')
    
    # Add subset info to output path if using subset
    if train_subset < 1.0:
        subset_str = f"_subset{int(train_subset*100)}pct"
    else:
        subset_str = ""
    
    output_path = f'{output_root}/{cfg["model_name"]}_{timestamp}{subset_str}'
    os.makedirs(output_path, exist_ok=True)
    
    print(f"\nOutput: {output_path}")
    print(f"GPUs: {torch.cuda.device_count()}")
    
    if torch.cuda.is_available():
        print(f"Device: {torch.cuda.get_device_name(0)}")
    
    # Logger
    logger = CSVLogger(output_path, name='MTR_v1', version=1, flush_logs_every_n_steps=100)

    # Trainer
    print("\n" + "-"*60)
    print("Setting up Trainer...")
    print("-"*60)
    
    trainer = pl.Trainer(
        max_epochs=cfg['epochs'],
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
                save_weights_only=True,
                monitor='val/loss',
                mode='min',
                filename='epoch={epoch:02d}-val_loss={val/loss:.4f}',
                every_n_epochs=1,
            ),
            LearningRateMonitor(logging_interval='step')
        ]
    )
    
    # Start training
    print("\n" + "="*60)
    print("STARTING TRAINING")
    print("="*60)
    print(f"Epochs: {cfg['epochs']}")
    print(f"Steps per epoch: {len(train_loader)}")
    if train_subset < 1.0:
        print(f"Pretraining mode: Using {train_subset*100:.1f}% of training data")
    print("="*60 + "\n")
    
    try:
        trainer.fit(model, train_loader, val_loader)
        
        print("\n" + "="*60)
        print("TRAINING COMPLETED!")
        print("="*60)
        print(f"Checkpoints: {output_path}")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("Training interrupted")
        print("="*60)
    
    except Exception as e:
        print("\n" + "="*60)
        print(f"Training failed: {e}")
        print("="*60)
        raise

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train QCNet on Waymo Dataset')
    parser.add_argument('--cfg', type=str, default='MTR_v1.yaml', 
                       help='Config file path')
    args = parser.parse_args()
    
    try:
        train(args.cfg)
    finally:
        # Always release GPU, even if training crashes
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("\n✅ GPU memory released")
        import sys
        sys.exit(0)