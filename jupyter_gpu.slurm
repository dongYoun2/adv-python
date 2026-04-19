#!/bin/bash
#SBATCH --partition=gpu4_short
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64GB
#SBATCH --time=00-12:00:00
#SBATCH --gres=gpu:1
#SBATCH --job-name=jupyter_gpu
#SBATCH --output=logs/%x/%j.log


# get tunneling info
XDG_RUNTIME_DIR=""
port=8890
node=$(hostname -s)
user=$(whoami)

case "$SLURM_SUBMIT_HOST" in
bigpurple-ln1)
 login_node=bigpurple1.nyumc.org
 ;;
bigpurple-ln2)
 login_node=bigpurple2.nyumc.org
 ;;
bigpurple-ln3)
 login_node=bigpurple3.nyumc.org
 ;;
bigpurple-ln4)
 login_node=bigpurple4.nyumc.org
 ;;
esac

# print tunneling instructions jupyter-log
echo -e "
MacOS or linux terminal command to create your ssh tunnel:
ssh -N -L ${port}:${node}:${port} ${user}@${login_node}

For more info and how to connect from windows,
   see research.computing.yale.edu/jupyter-nb
Here is the MobaXterm info:

Forwarded port:same as remote port
Remote server: ${node}
Remote port: ${port}
SSH server: ${login_node}
SSH login: $user
SSH port: 22
Use a Browser on your local machine to go to:
http://localhost:${port}  (prefix w/ https:// if using password)
Use the token string from the URL printed below and add it to the URL above
"

# load modules or conda environments here

# STEP #1: load necessary modules
# IMPORTANT: do NOT load any cuda/* module. Numba talks directly to the
# host driver (libcuda.so.1 in /lib64). Loading a CUDA toolkit module also
# adds its lib64 (which contains a libcuda stub) to LD_LIBRARY_PATH and
# breaks cuInit with UNKNOWN_CUDA_ERROR.

# STEP #2: enable conda WITHOUT sourcing the full bashrc
# (sourcing .bashrc was pulling in CUDA 9.0/11.8/12.6 paths into
#  LD_LIBRARY_PATH, which shadowed the real libcuda.so.1)
source /gpfs/data/fieremanslab/dayne/miniconda3/etc/profile.d/conda.sh

# STEP #3: activate the conda env
conda activate advpy

# STEP #4: scrub any leftover CUDA toolkit paths from LD_LIBRARY_PATH
# (defensive: in case the cluster's system profile re-injects them)
LD_LIBRARY_PATH=$(echo "$LD_LIBRARY_PATH" | tr ':' '\n' | grep -v '/cuda/' | paste -sd:)
export LD_LIBRARY_PATH
unset LD_PRELOAD

# STEP #5: cd to your workspace
cd /gpfs/data/fieremanslab/dayne/projects/adv-python

# STEP #6: start the jupyter notebook
jupyter-notebook --no-browser --port=${port} --ip=${node}
