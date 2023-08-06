"""Setup script for object_detection with TF2.0."""
import os
from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'tensorboard>=2.2'
]

setup(
    name='yolov6',
    version='0.0.1',
    install_requires=REQUIRED_PACKAGES,
    include_package_data=True,
    packages=(
        [p for p in find_packages(where='.')]),
    package_dir={

    },
    description='Forthcoming Yolov6 wrapper',
    python_requires='>=3.6.9',
)
