#!/bin/bash

####################################
#  Iridis 5 slurm script template  
#                                  
#  Submit script: sbatch filename  
#                                  
####################################
#SBATCH --nodes=1     # Number of nodes requested
##SBATCH --partition=amd
##SBATCH --cpus-per-task=64     # Threads per task
#SBATCH --cpus-per-task=5     # Threads per task
#SBATCH --time=60:00:00   # walltime

# Logs
#SBATCH --output=test.out
#SBATCH --error=test.err

# Not needed as conda is loaded directly without this
# module load conda/py3-latest
#conda info --envs

# This activates the conda environment using the anaconda3 version
source ~/anaconda3/bin/activate e-swarm

# This forces std_out to accept print statements 
# grid_size, scenario and compete can now be passed as args
python -u /home/aoa1v22/MARL_git/z_test/tester2.py \
> test.out