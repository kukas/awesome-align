#!/bin/bash
#SBATCH --time=02:30:00
#SBATCH -o /home/balhar/my-luster/awesome-align/logs/tokenization_logs/tokenization_%j.out

echo $@
pwd
python tokenize.py $@
