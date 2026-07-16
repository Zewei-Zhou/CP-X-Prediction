#!/usr/bin/env bash
# Source this: sets up ROS2 humble overlay and MTR PYTHONPATH, using absolute python path.
# Prepend conda env bin to PATH so 'python' resolves to ros_humble.
export PATH="/data/miniconda3/envs/ros_humble/bin:$PATH"
# CMAKE_PREFIX_PATH etc. come from the overlay setup:
source /data/robert/CP-X-Prediction/ROS2-Code/install/setup.bash
export PYTHONPATH="/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR:${PYTHONPATH}"
hash -r
