import torch
import datetime
import argparse
import os

from model import MTR
# from model_simple import MTR
from train_utils import WaymoDataset, load_config, collate_waymo_data
from torch.utils.data import DataLoader

import lightning.pytorch as pl
from lightning.pytorch.callbacks import ModelCheckpoint, LearningRateMonitor
from lightning.pytorch.loggers import WandbLogger, CSVLogger, TensorBoardLogger
from lightning.pytorch.strategies import DDPStrategy


def train(cfg_file):
    print("Start Training")
    torch.set_float32_matmul_precision('high')      
    cfg = load_config(cfg_file)
    pl.seed_everything(cfg['seed'])
    
    # create dataset
    train_dataset = WaymoDataset(cfg['train_data_path'])
    print("Train Dataset:", len(train_dataset))
    val_dataset = WaymoDataset(cfg['val_data_path'])
    print("Val Dataset:", len(val_dataset))

    train_loader = DataLoader(
        train_dataset, 
        batch_size=cfg['batch_size'], 
        pin_memory=True, 
        num_workers=cfg['num_workers'],
        shuffle=True,
        collate_fn=collate_waymo_data
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=cfg['batch_size'],
        pin_memory=True, 
        num_workers=cfg['num_workers'],
        shuffle=False, 
        collate_fn=collate_waymo_data
    )
    
    model = MTR(cfg)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_root = cfg.get('output_path', 'output')
    output_path = f'{output_root}/{cfg["model_name"]}_{timestamp}'
    os.makedirs(output_path, exist_ok=True)
    print("Total GPUS:", torch.cuda.device_count())
    
    logger = CSVLogger(output_path, name='MTR', version=1, flush_logs_every_n_steps=100)

    trainer = pl.Trainer(
        max_epochs=cfg['epochs'],
        devices=-1,
        accelerator='gpu',
        #strategy='ddp',
        enable_progress_bar=True, 
        logger=logger, 
        enable_model_summary=True,
        detect_anomaly=False,
        gradient_clip_val=1.0,  
        gradient_clip_algorithm="norm",
        num_sanity_val_steps=0,
        log_every_n_steps=100,
        callbacks=[
            ModelCheckpoint(
                dirpath=output_path,
                save_top_k=-1,
                save_weights_only=True,
                monitor='val/loss',
                filename='epoch={epoch:02d}',
                auto_insert_metric_name=False,
                every_n_epochs=1,
                save_on_train_epoch_end=False,
            ),
            LearningRateMonitor(logging_interval='step')
        ]
    )
    print("Build Trainer")
    
    trainer.fit(model, train_loader, val_loader)
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='MTR_v1.yaml')
    args = parser.parse_args()
    
    train(args.cfg)
    
