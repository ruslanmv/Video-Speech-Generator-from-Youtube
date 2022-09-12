#!/usr/bin/env bash
source activate python3
# check prerequisites
command -v conda >/dev/null 2>&1 || { echo >&2 "conda not found. Please refer to the README and install Miniconda."; exit 1; }
command -v git >/dev/null 2>&1 || { echo >&2 "git not found. Please refer to the README and install Git."; exit 1; }
# Conda environment name
CONDA_ENV_NAME=VideoMessage
source $(conda info --base)/etc/profile.d/conda.sh
conda create -y -n $CONDA_ENV_NAME python=3.7.13
conda activate $CONDA_ENV_NAME
conda install -y  ipykernel
python -m ipykernel install --user --name VideoMessage --display-name "Python 3 (VideoMessage)"
sh install_git-lfs.sh
sh install_ffmpeg.sh




