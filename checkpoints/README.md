# Checkpoints

MTR model checkpoints for CP-X-Prediction, tracked with **Git LFS** (see
`../.gitattributes`). After cloning, run `git lfs pull` to download the actual
`.pth` files (a plain `git clone` only fetches small LFS pointer files).

| File | Description | How it was produced |
|------|-------------|---------------------|
| `checkpoint_epoch_25.pth` | CP-X / Waymo **pretrained** MTR model. Starting point for V2X-PnP finetuning. | Trained with `tools/cfgs/challenge/mtr-training-CPX-Prediction.yaml` on `/data/dataset/CP-X/data/waymo`. |
| `checkpoint_epoch_30.pth` | V2X-PnP **finetuned** model *(added once finetuning completes)*. | Finetuned from `checkpoint_epoch_25.pth` with `tools/cfgs/challenge/mtr-finetuning-V2XPNP.yaml`. |

To evaluate a checkpoint, from
`Intersection-Code/Intersection-MTR/Prediction/MTR/tools`:

```bash
python test.py \
  --cfg_file cfgs/challenge/mtr-testing-CPX-Prediction.yaml \
  --ckpt /path/to/checkpoints/checkpoint_epoch_25.pth
```

See the top-level [README](../README.md) for the full train / finetune / test workflow.
