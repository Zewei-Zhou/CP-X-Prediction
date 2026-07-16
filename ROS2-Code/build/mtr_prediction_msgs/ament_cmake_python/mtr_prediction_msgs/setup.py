from setuptools import find_packages
from setuptools import setup

setup(
    name='mtr_prediction_msgs',
    version='0.0.1',
    packages=find_packages(
        include=('mtr_prediction_msgs', 'mtr_prediction_msgs.*')),
)
