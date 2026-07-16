"""
Inference Time Benchmark for MTR Trajectory Prediction Model

Measures the average forward-pass latency (encoder + predictor) over 100 samples,
excluding all data loading and preprocessing time.

Usage:
    python benchmark_inference.py --checkpoint /path/to/checkpoint_epoch_25.pth --cfg /path/to/mtr-testing-CPX-Prediction.yaml
    python benchmark_inference.py --checkpoint /path/to/checkpoint_epoch_25.pth --cfg /path/to/mtr-testing-CPX-Prediction.yaml --num_samples 100 --warmup 20
"""

import argparse
import sys
import time

import numpy as np
import torch
from tqdm import tqdm

# ── Add MTR package to path ───────────────────────────────────────────────────
MTR_ROOT = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR"
sys.path.insert(0, MTR_ROOT)

from mtr.config import cfg, cfg_from_yaml_file
from mtr.datasets import build_dataloader
from mtr.models.model import MotionTransformer
from mtr.utils import common_utils


def benchmark(args):
    device = torch.device(args.device if torch.cuda.is_available() or args.device == "cpu" else "cpu")
    print(f"Device: {device}")

    # ── Load config ──────────────────────────────────────────────
    cfg_from_yaml_file(args.cfg, cfg)
    print(f"Config loaded from: {args.cfg}")

    # ── Load model ───────────────────────────────────────────────
    logger = common_utils.create_logger()
    model = MotionTransformer(config=cfg.MODEL)
    model.to(device)

    print(f"Loading checkpoint: {args.checkpoint}")
    model.load_params_from_file(filename=args.checkpoint, logger=logger, to_cpu=(args.device == "cpu"))
    model.eval()
    print(f"Model loaded. Parameters: {sum(p.numel() for p in model.parameters()):,}")

    # ── Load dataset (test/val split) ─────────────────────────────
    total_needed = args.warmup + args.num_samples
    _, loader, _ = build_dataloader(
        dataset_cfg=cfg.DATA_CONFIG,
        batch_size=1,
        dist=False,
        workers=4,
        logger=logger,
        training=False,
    )

    # ── Pre-load all batches into memory so data I/O is excluded ─
    print(f"Pre-loading {total_needed} batches (warmup={args.warmup}, measure={args.num_samples})...")
    batches = []
    for batch in tqdm(loader, total=total_needed, desc="Loading data"):
        # move all tensor values to device
        batches.append({k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in batch.items()})
        if len(batches) >= total_needed:
            break

    if len(batches) < total_needed:
        print(f"Warning: only {len(batches)} samples available, adjusting.")
        args.warmup = min(args.warmup, len(batches) // 10)
        args.num_samples = len(batches) - args.warmup

    print(f"Data pre-loaded. Starting benchmark...")

    # ── Warm-up (not timed) ───────────────────────────────────────
    with torch.no_grad():
        for i in range(args.warmup):
            _ = model(batches[i])
    if device.type == "cuda":
        torch.cuda.synchronize()
    print(f"Warm-up complete ({args.warmup} runs).")

    # ── Timed inference ───────────────────────────────────────────
    latencies_ms = []

    with torch.no_grad():
        for i in range(args.warmup, args.warmup + args.num_samples):
            batch = batches[i]

            if device.type == "cuda":
                start_event = torch.cuda.Event(enable_timing=True)
                end_event = torch.cuda.Event(enable_timing=True)
                start_event.record()
                _ = model(batch)
                end_event.record()
                torch.cuda.synchronize()
                latencies_ms.append(start_event.elapsed_time(end_event))
            else:
                t0 = time.perf_counter()
                _ = model(batch)
                t1 = time.perf_counter()
                latencies_ms.append((t1 - t0) * 1000.0)

    # ── Report results ────────────────────────────────────────────
    latencies = np.array(latencies_ms)
    print("\n" + "=" * 50)
    print("  INFERENCE TIME BENCHMARK RESULTS")
    print("=" * 50)
    print(f"  Samples measured : {args.num_samples}")
    print(f"  Device           : {device}")
    print(f"  Batch size       : 1 (per-sample latency)")
    print("-" * 50)
    print(f"  Mean             : {latencies.mean():.2f} ms")
    print(f"  Std              : {latencies.std():.2f} ms")
    print(f"  Min              : {latencies.min():.2f} ms")
    print(f"  Max              : {latencies.max():.2f} ms")
    print(f"  Median (p50)     : {np.percentile(latencies, 50):.2f} ms")
    print(f"  p95              : {np.percentile(latencies, 95):.2f} ms")
    print(f"  p99              : {np.percentile(latencies, 99):.2f} ms")
    print("=" * 50)
    print(f"\nAverage inference time: {latencies.mean():.2f} ms/sample")

    if device.type == "cuda":
        mem_mb = torch.cuda.max_memory_allocated(device) / 1024**2
        print(f"Peak GPU memory used : {mem_mb:.1f} MB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark MTR inference latency")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to .pth checkpoint file")
    parser.add_argument("--cfg", type=str, required=True, help="Path to MTR config YAML")
    parser.add_argument("--num_samples", type=int, default=100, help="Number of timed samples")
    parser.add_argument("--warmup", type=int, default=20, help="Warm-up runs before timing")
    parser.add_argument("--device", type=str, default="cuda", choices=["cuda", "cpu"])
    args = parser.parse_args()
    benchmark(args)
