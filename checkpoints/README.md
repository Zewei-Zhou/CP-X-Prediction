# Checkpoints

MTR model checkpoints for CP-X-Prediction, tracked with **Git LFS** (see
`../.gitattributes`). After cloning, run `git lfs pull` to download the actual
`.pth` files (a plain `git clone` only fetches small LFS pointer files).

| File | Description | How it was produced |
|------|-------------|---------------------|
| `checkpoint_epoch_25.pth` | CP-X / Waymo **pretrained** MTR model. Starting point for V2X-PnP finetuning. | Trained with `tools/cfgs/challenge/mtr-training-CPX-Prediction.yaml` on `/data/dataset/CP-X/data/waymo`. |
| `checkpoint_epoch_30.pth` | V2X-PnP **finetuned** model. Loaded by default by the ROS 2 node. | `python train.py --cfg_file cfgs/challenge/mtr-finetuning-V2XPNP.yaml --batch_size 1 --epochs 30 --pretrained_model .../checkpoint_epoch_25.pth --not_eval_with_train`, with `MAX_NUM_CENTER_OBJECTS_TRAIN=32` so the dense scenes fit on a 46 GB L40S (see the finetune section of the top-level README). |

To evaluate a checkpoint, from
`Intersection-Code/Intersection-MTR/Prediction/MTR/tools`:

```bash
python test.py \
  --cfg_file cfgs/challenge/mtr-testing-CPX-Prediction.yaml \
  --ckpt /path/to/checkpoints/checkpoint_epoch_25.pth
```

See the top-level [README](../README.md) for the full train / finetune / test workflow.
