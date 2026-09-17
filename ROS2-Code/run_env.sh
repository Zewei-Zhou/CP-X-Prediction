#!/usr/bin/env bash
# Source this to set up the ROS 2 Humble (conda) environment, the mtr_prediction_msgs
# overlay, and the MTR package on PYTHONPATH. Paths are derived from this script's
# location so the repo can live anywhere.
#
#   source run_env.sh
#
# Note: the colcon-generated install/setup.bash bakes in absolute build-time paths, so we
# wire the overlay prefix directly here instead of relying on it.

_ROS2_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_REPO_ROOT="$(cd "${_ROS2_DIR}/.." && pwd)"
_CONDA_ROOT="/data/miniconda3"
_ROS_ENV="ros_humble"

# 1. Activate the conda ROS 2 Humble environment (provides rclpy, ros2 cli, typesupport).
if [ -f "${_CONDA_ROOT}/etc/profile.d/conda.sh" ]; then
    # shellcheck disable=SC1091
    source "${_CONDA_ROOT}/etc/profile.d/conda.sh"
    conda activate "${_ROS_ENV}"
else
    export PATH="${_CONDA_ROOT}/envs/${_ROS_ENV}/bin:$PATH"
fi

# 2. Wire the mtr_prediction_msgs overlay prefix directly.
_OVERLAY="${_ROS2_DIR}/install/mtr_prediction_msgs"
_PYVER="$(python -c 'import sys;print("python%d.%d"%sys.version_info[:2])' 2>/dev/null)"
export AMENT_PREFIX_PATH="${_OVERLAY}:${AMENT_PREFIX_PATH}"
export PYTHONPATH="${_OVERLAY}/lib/${_PYVER}/site-packages:${PYTHONPATH}"
export LD_LIBRARY_PATH="${_OVERLAY}/lib:${LD_LIBRARY_PATH}"

# 3. Put the MTR package on PYTHONPATH (model, config, datasets used by node.py).
export PYTHONPATH="${_REPO_ROOT}/Intersection-Code/Intersection-MTR/Prediction/MTR:${PYTHONPATH}"

hash -r
