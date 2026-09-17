# CP-X-Prediction

Trajectory-prediction stack for the CP-X intersection safety project. It is built on
**MTR (Motion TRansformer)** — Shi et al., *"Motion Transformer with Global Intention
Localization and Local Movement Refinement"*, NeurIPS 2022
([arXiv:2209.13508](https://arxiv.org/abs/2209.13508)) — adapted to the TFHRC West
Intersection scenarios and V2X-PnP cooperative data, plus a ROS 2 node that runs the
trained model in real time on live/replayed sensor streams.

> **New to this repo?** On the current lab machine the datasets are already in place and
> the checked-in configs already point at them (see [Datasets](#datasets)), so training,
> finetuning, and testing run out of the box once the conda env is built. If you move to a
> different machine, update each config's `DATA_ROOT` to wherever you put the data.

---

## Repository layout

```
CP-X-Prediction/
├── Intersection-Code/
│   ├── Intersection-MTR/               # main offline prediction pipeline
│   │   ├── Prediction/
│   │   │   ├── MTR/                     # ← the model. Fork of MTR (train/finetune/test here)
│   │   │   ├── QCNet_Pipeline/          # alternative QCNet predictor (experimental)
│   │   │   ├── conflict_prediction/     # conflict / near-miss prediction from trajectories
│   │   │   └── dummy_prediction/        # constant-velocity baseline
│   │   ├── Preprocessing/               # annotation, detection, radar, validation-GT preprocessing
│   │   ├── Postprocessing/              # merge / clean / quality-check prediction results
│   │   ├── Test_Pipeline/              # end-to-end conflict evaluation scripts
│   │   ├── Visualization/               # GT + prediction scenario plotting
│   │   ├── map/                         # TFHRC West Intersection map (.xodr → vector map)
│   │   └── Data/                        # annotation / perception / validation-GT data
│   └── Intersection-MTR-Finetuning/
│       └── v2xpnp_to_waymo_converter.py # converts V2X-PnP scenarios into Waymo/MTR format
└── ROS2-Code/                           # ROS 2 (Humble) real-time inference node
    ├── mtr_prediction_msgs/             # custom prediction messages
    ├── rosbag/                          # sample bags + recorded outputs
    └── run_env.sh                       # sources the ROS overlay + MTR PYTHONPATH
```

The rest of this README focuses on **`Intersection-Code/Intersection-MTR/Prediction/MTR`**,
which is where you train, finetune, and test the model. Throughout, this directory is
abbreviated `MTR_ROOT`:

```
MTR_ROOT = Intersection-Code/Intersection-MTR/Prediction/MTR
```

There is also a shorter component-level README at
`Intersection-Code/Intersection-MTR/README.md`.

---

## Quick start

```bash
# 0. from the repo root
cd Intersection-Code/Intersection-MTR/Prediction/MTR      # = MTR_ROOT

# 1. build the environment (see "Environment setup" for details)
conda create -n cpx-mtr python=3.8 -y
conda activate cpx-mtr
# install a CUDA-matched PyTorch first (example: CUDA 11.x)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
python setup.py develop            # builds the knn / attention CUDA ops

# 2. (only if you moved the data) update DATA_ROOT in the config you plan to run.
#    On the current lab machine the configs already point at the data — skip this.

# 3. train / finetune / test from the tools/ directory
cd tools
python train.py --cfg_file cfgs/challenge/mtr-training-CPX-Prediction.yaml --batch_size 10 --epochs 30
```

---

## Environment setup

Two separate conda environments are used:

| Environment | Used for | Notes |
|-------------|----------|-------|
| `cpx-mtr` (any name) | training / finetuning / testing the MTR model | needs a CUDA toolchain to build the custom ops |
| `ros_humble` | the ROS 2 real-time node in `ROS2-Code/` | ROS 2 Humble + the MTR package on `PYTHONPATH` |

> The exact environment name and package versions the original students used are **not**
> recorded in the repo. The steps below reproduce a working environment; pin versions to
> match your GPU/CUDA if you hit build errors, and cross-check against the upstream MTR
> install guide: <https://github.com/sshaoshuai/MTR>.

### MTR environment

```bash
conda create -n cpx-mtr python=3.8 -y
conda activate cpx-mtr

# 1) PyTorch — install a build that matches your CUDA driver.
#    The custom CUDA ops in setup.py are compiled against this torch/CUDA.
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# 2) Python deps (numpy, torch, tensorboardX, easydict, pyyaml, scikit-image, tqdm)
cd Intersection-Code/Intersection-MTR/Prediction/MTR      # = MTR_ROOT
pip install -r requirements.txt

# 3) Build + install the MTR package (compiles mtr/ops/knn and mtr/ops/attention).
python setup.py develop
```

**Data preprocessing only** additionally needs the Waymo Open Dataset toolkit
(`data_preprocess.py` imports `tensorflow` and `waymo_open_dataset`):

```bash
pip install waymo-open-dataset-tf-2-11-0   # pick the tf build matching your setup
```

You do **not** need TensorFlow / waymo-open-dataset just to train or test on
already-preprocessed `.pkl` scenarios.

### ROS 2 environment

`ROS2-Code/run_env.sh` shows how the node is launched — it prepends a conda env to
`PATH`, sources the ROS overlay, and puts `MTR_ROOT` on `PYTHONPATH`. Update the absolute
paths in that script for this machine before sourcing it:

```bash
# ROS2-Code/run_env.sh (edit the paths, then: source run_env.sh)
export PATH="/data/miniconda3/envs/ros_humble/bin:$PATH"
source <repo>/ROS2-Code/install/setup.bash
export PYTHONPATH="<repo>/Intersection-Code/Intersection-MTR/Prediction/MTR:${PYTHONPATH}"
```

---

## Datasets

### Where the data lives on this machine

| Data | Path on disk | Status |
|------|--------------|--------|
| CP-X / Waymo processed scenarios (pretraining) | `/data/dataset/CP-X/data/waymo/` | **Complete and ready.** 486,995 train + 44,097 val scenarios, both `*_infos.pkl` present. This is what `mtr-training/testing-CPX-Prediction.yaml` point at. |
| V2X-PnP processed scenarios (finetuning) | `/data/dataset/waymo_finetune_v2xpnp_processed/` | **Complete and ready.** train/val/test splits + all three `*_infos.pkl`. This is what `mtr-finetuning-V2XPNP.yaml` points at. `..._both_maps_processed/` and `..._full_map_processed/` are the map-coverage variants. |
| Annotation / perception / validation-GT | `Intersection-Code/Intersection-MTR/Data/` | raw project data |

> **Note on `/data2/CP-X/data/waymo`.** This is an **incomplete partial copy** of the
> CP-X dataset — only `processed_scenarios_training/` with ~33k of the 486,995 scenarios,
> and no validation split or `*_infos.pkl`. Do **not** point configs at it; use the
> canonical `/data/dataset/CP-X/data/waymo` above (where the configs already point).

### Expected structure (what a config's `DATA_ROOT` must contain)

`WaymoDataset` expects, under `DATA_ROOT`:

```
<DATA_ROOT>/
├── processed_scenarios_training/            # SPLIT_DIR['train'] — per-scenario *.pkl
├── processed_scenarios_validation/          # SPLIT_DIR['test']  — per-scenario *.pkl
├── processed_scenarios_training_infos.pkl   # INFO_FILE['train'] — index over the train split
└── processed_scenarios_val_infos.pkl        # INFO_FILE['test']  — index over the val split
```

The `*_infos.pkl` index files and the validation split are produced by the preprocessing
step below. **For the datasets on the current machine this is already done** — both the
CP-X and V2X-PnP `DATA_ROOT`s above already contain the splits and info files, so you only
need the preprocessing step when building a *new* dataset from raw scenario protos.

### Preprocessing raw scenarios → MTR format

```bash
cd Intersection-Code/Intersection-MTR/Prediction/MTR/mtr/datasets/waymo   # = MTR_ROOT/mtr/datasets/waymo

# create_infos_from_protos(raw_data_path, output_path)
python data_preprocess.py <raw_scenario_protos_dir> <output_dir>
```

This writes the per-scenario `.pkl` files and the corresponding `*_infos.pkl` index into
`<output_dir>`. Run it once for the training protos and once for the validation protos so
that `<output_dir>` ends up matching the "Expected structure" above.

To convert **V2X-PnP** cooperative data into this Waymo/MTR format, use
`Intersection-Code/Intersection-MTR-Finetuning/v2xpnp_to_waymo_converter.py`.

### Intention-point clusters

The decoder needs the k-means intention anchors referenced by `INTENTION_POINTS_FILE` in
each config (e.g. `data/waymo/cluster_64_center_dict.pkl`). These are already checked in
under `MTR_ROOT/data/`. Regenerate them with
`MTR_ROOT/data_tools/cluster_intention_points.ipynb` if you change the training set.

---

## Configs

All experiment configs live in `MTR_ROOT/tools/cfgs/challenge/`. The relevant CP-X ones:

| Config | Purpose | `DATA_ROOT` in file |
|--------|---------|---------------------|
| `mtr-training-CPX-Prediction.yaml` | pretrain on CP-X / Waymo (train split, every 2nd frame) | `/data/dataset/CP-X/data/waymo` |
| `mtr-testing-CPX-Prediction.yaml` | evaluate on the CP-X val split | `/data/dataset/CP-X/data/waymo` |
| `mtr-finetuning-V2XPNP.yaml` | finetune the pretrained model on V2X-PnP | `/data/dataset/waymo_finetune_v2xpnp_processed` |
| `mtr-testing-finetuning-V2XPNP.yaml` | evaluate the finetuned model | `/data/dataset/waymo_finetune_v2xpnp_processed` |
| `mtr-finetuning-both-maps-V2XPNP.yaml`, `...-full-map-...` | finetune variants with different map coverage | various `/data/dataset/...` |

Key `OPTIMIZATION` defaults (in the CP-X configs): `BATCH_SIZE_PER_GPU: 10`,
`NUM_EPOCHS: 30`, AdamW, `LR: 1e-4`. Model = MTR encoder (6 layers) + MTR decoder
(6 layers, 6 motion modes, 80 future frames).

---

## Training, finetuning, testing

All commands are run **from `MTR_ROOT/tools`**. Outputs are written to
`MTR_ROOT/output/<exp_group>/<config_stem>/<extra_tag>/`, where `<exp_group>` is the
config's subfolder (`challenge`) and `<extra_tag>` defaults to `default`. Checkpoints land
in `.../ckpt/checkpoint_epoch_*.pth`.

### 1. Pretrain on CP-X / Waymo

Single GPU:
```bash
cd MTR_ROOT/tools
python train.py \
  --cfg_file cfgs/challenge/mtr-training-CPX-Prediction.yaml \
  --batch_size 10 \
  --epochs 30
```

Multi-GPU (recommended; `<N>` = number of GPUs):
```bash
cd MTR_ROOT/tools
bash scripts/dist_train.sh <N> \
  --cfg_file cfgs/challenge/mtr-training-CPX-Prediction.yaml \
  --batch_size 10 \
  --epochs 30
# scripts/torchrun_train.sh is the torchrun-based equivalent.
```

Result: `output/challenge/mtr-training-CPX-Prediction/default/ckpt/checkpoint_epoch_*.pth`.

### 2. Finetune on V2X-PnP

Load the pretrained CP-X weights with `--pretrained_model` (weights only, fresh
optimizer, trains the full `--epochs` — this is how the released finetune was produced;
do **not** use `--ckpt`, which would *resume* from epoch 25 and only train 5 more epochs):

```bash
cd MTR_ROOT/tools
python train.py \
  --cfg_file cfgs/challenge/mtr-finetuning-V2XPNP.yaml \
  --batch_size 1 \
  --epochs 30 \
  --pretrained_model ../output/checkpoint_epoch_25.pth \
  --not_eval_with_train
```

Result: `output/challenge/mtr-finetuning-V2XPNP/default/ckpt/checkpoint_epoch_30.pth`.
A ready-to-use pretrained checkpoint is included at
`MTR_ROOT/output/checkpoint_epoch_25.pth` (see [Checkpoints](#checkpoints)).

> **GPU memory.** V2X-PnP scenes are dense (up to ~145 agents predicted at once), and MTR
> processes all of a scene's agents simultaneously, so a single scene needs >44 GB in
> fp32 — it OOMs a 46 GB GPU at any batch size. Two ways to run it:
> - **80 GB GPU (A100/H100):** run as-is at `--batch_size 1`, no other changes.
> - **≤48 GB GPU (e.g. L40S):** set `MAX_NUM_CENTER_OBJECTS_TRAIN` in the finetune config
>   (default `32`). This randomly subsamples agents-per-scene **during training only**
>   (re-sampled each epoch; eval/inference always use all agents), which drops peak memory
>   to ~13 GB. The released `checkpoint_epoch_30.pth` was finetuned this way on an L40S.

### 3. Test / evaluate

```bash
cd MTR_ROOT/tools
python test.py \
  --cfg_file cfgs/challenge/mtr-testing-CPX-Prediction.yaml \
  --ckpt <path>/checkpoint_epoch_XX.pth
```

Useful flags: `--eval_all` (sweep every checkpoint in a run's `ckpt/` dir),
`--ckpt_dir <dir>`, `--save_to_file`, `--batch_size`. Distributed eval:
`bash scripts/dist_test.sh <N> --cfg_file ... --ckpt ...`.

### 4. Conflict prediction / evaluation

Downstream conflict (near-miss) analysis on top of predicted trajectories lives in
`Intersection-Code/Intersection-MTR/Prediction/conflict_prediction/` and the end-to-end
scripts in `Intersection-Code/Intersection-MTR/Test_Pipeline/`
(`pipeline_test_mtr.py`, `calculate_conflict_from_csv.py`, `conflict.py`).

---

## Checkpoints

Both are committed under `checkpoints/` via **Git LFS** (run `git lfs pull` after cloning):

| Checkpoint | Path | What it is |
|------------|------|------------|
| `checkpoint_epoch_25.pth` | `checkpoints/checkpoint_epoch_25.pth` | CP-X pretrained model — the starting point for V2X-PnP finetuning. |
| `checkpoint_epoch_30.pth` | `checkpoints/checkpoint_epoch_30.pth` | V2X-PnP finetuned model (from `checkpoint_epoch_25` via [step 2](#2-finetune-on-v2x-pnp), `MAX_NUM_CENTER_OBJECTS_TRAIN=32` on an L40S). The ROS 2 node loads this by default. |

Bare `.pth` files elsewhere are git-ignored (see `.gitignore`); only the two under
`checkpoints/` are tracked. To regenerate the finetuned checkpoint, run
[step 2](#2-finetune-on-v2x-pnp) — the data it needs is already in place.

---

## Notes / gotchas

1. **Use the canonical data paths — not the `/data2` copy.** The configs already point at
   the complete datasets under `/data/dataset/...`. `/data2/CP-X/data/waymo` is only a
   partial copy (training subset, no val split, no info files); pointing a config at it
   will fail or silently train on a fraction of the data. If you run on a different
   machine, set each config's `DATA_ROOT` to a directory matching the
   [expected structure](#expected-structure-what-a-configs-data_root-must-contain).

2. **Stale absolute paths in scratch files.** `tools/temp.txt`, `tools/test.txt`, and
   `ROS2-Code/run_env.sh` contain example commands with an older
   `/data/robert/CP-X-Prediction/...` layout. They are illustrative only — update the
   paths for your checkout before using them.

3. **CUDA ops must be built for your torch/CUDA.** If you see import errors for
   `mtr.ops.knn` or `mtr.ops.attention`, re-run `python setup.py develop` inside the same
   conda env / CUDA toolchain you train with.

---

## Attribution

The model and training code are derived from **MTR** by Shaoshuai Shi et al.
(<https://github.com/sshaoshuai/MTR>, Apache License 2.0). CP-X-specific data conversion,
configs, conflict prediction, and the ROS 2 node are additions for this project.
