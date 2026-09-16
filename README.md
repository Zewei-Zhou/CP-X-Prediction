# CP-X-Prediction

Trajectory-prediction stack for the CP-X intersection safety project. It is built on
**MTR (Motion TRansformer)** — Shi et al., *"Motion Transformer with Global Intention
Localization and Local Movement Refinement"*, NeurIPS 2022
([arXiv:2209.13508](https://arxiv.org/abs/2209.13508)) — adapted to the TFHRC West
Intersection scenarios and V2X-PnP cooperative data, plus a ROS 2 node that runs the
trained model in real time on live/replayed sensor streams.

> **New to this repo? Read the [Quick start](#quick-start) and then the
> [Known issues / must-fix before running](#known-issues--must-fix-before-running)
> section first — the checked-in configs point at data paths that no longer exist on
> this machine, so nothing will run until you repoint `DATA_ROOT`.**

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

# 2. point the config at the real data location (see "Known issues")
#    edit DATA_ROOT in tools/cfgs/challenge/mtr-training-CPX-Prediction.yaml

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
| CP-X / Waymo processed scenarios | `/data2/CP-X/data/waymo/` | `processed_scenarios_training/` present (33,011 scenarios). **No validation split and no `*_infos.pkl` yet** — see below. |
| Annotation / perception / validation-GT | `Intersection-Code/Intersection-MTR/Data/` | raw project data |

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
step below. On this machine only the training split currently exists, so **you must run
preprocessing to generate the validation split + both info files before training/testing
end-to-end.**

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

Start from a pretrained CP-X checkpoint via `--ckpt`:
```bash
cd MTR_ROOT/tools
python train.py \
  --cfg_file cfgs/challenge/mtr-finetuning-V2XPNP.yaml \
  --batch_size 6 \
  --epochs 30 \
  --ckpt <path>/checkpoint_epoch_25.pth
```

A ready-to-use pretrained checkpoint is included at
`MTR_ROOT/output/checkpoint_epoch_25.pth` (see [Checkpoints](#checkpoints)).

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

| Checkpoint | Path | What it is |
|------------|------|------------|
| `checkpoint_epoch_25.pth` | `MTR_ROOT/output/checkpoint_epoch_25.pth` | CP-X pretrained model — the starting point for V2X-PnP finetuning. |

`.pth` files are git-ignored (see `.gitignore`), so checkpoints are **not** version
controlled — copy them explicitly when moving machines. To produce an **updated**
finetuned checkpoint, run step 2 above with `--ckpt` pointing at this file once the data
paths are fixed (see below).

---

## Known issues / must-fix before running

1. **`DATA_ROOT` points at stale paths.** Every config in `tools/cfgs/challenge/` points
   at `/data/dataset/...` (e.g. `mtr-training-CPX-Prediction.yaml` →
   `/data/dataset/CP-X/data/waymo`), but on this machine the data actually lives at
   **`/data2/CP-X/data/waymo`**. Edit the `DATA_ROOT:` line of whichever config you run,
   or symlink the expected path. The old scratch notes in `tools/temp.txt` and
   `tools/test.txt`, and `ROS2-Code/run_env.sh`, reference an even older
   `/data/robert/CP-X-Prediction/...` layout — ignore those absolute paths.

2. **Validation split + info files are missing.** `/data2/CP-X/data/waymo/` currently has
   only `processed_scenarios_training/`. Training/testing also need
   `processed_scenarios_validation/`, `processed_scenarios_training_infos.pkl`, and
   `processed_scenarios_val_infos.pkl`. Generate them with the
   [preprocessing step](#preprocessing-raw-scenarios--mtr-format).

3. **CUDA ops must be built for your torch/CUDA.** If you see import errors for
   `mtr.ops.knn` or `mtr.ops.attention`, re-run `python setup.py develop` inside the same
   conda env / CUDA toolchain you train with.

---

## Attribution

The model and training code are derived from **MTR** by Shaoshuai Shi et al.
(<https://github.com/sshaoshuai/MTR>, Apache License 2.0). CP-X-specific data conversion,
configs, conflict prediction, and the ROS 2 node are additions for this project.
