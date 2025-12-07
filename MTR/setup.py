# File: /data/robert/CP-X-Prediction/MTR/setup.py
from setuptools import setup, find_packages

setup(
    name="mtr",
    version="0.1",
    packages=find_packages(where="Prediction"),
    package_dir={"": "Prediction"},
)