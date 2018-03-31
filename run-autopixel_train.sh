#!/bin/sh

#SBATCH -N 1  # nodes requested
#SBATCH -n 1	  # tasks requested
#SBATCH --gres=gpu:1 # use 1 GPU
#SBATCH --mem=16000  # memory in Mb
#SBATCH -t 8:00:00  # time requested in hour:minute:seconds

# Setup CUDA and CUDNN related paths
export CUDA_HOME=/opt/cuda-8.0.44

export CUDNN_HOME=/opt/cuDNN-6.0_8.0

export STUDENT_ID=s1793872

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:${CUDA_HOME}/lib64:$LD_LIBRARY_PATH

export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH

export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}

export PYTHON_PATH=$PATH

# Setup a folder in the very fast scratch disk which can be used for storing experiment objects and any other files
# that may require storage during execution.
mkdir -p /disk/scratch/${STUDENT_ID}

export TMPDIR=/disk/scratch/${STUDENT_ID}/
export TMP=/disk/scratch/${STUDENT_ID}/

# Activate the relevant virtual environment:

source /home/${STUDENT_ID}/miniconda3/bin/activate mlp
python autopixel_train.py --name $1 --append $2
