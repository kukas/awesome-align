#!/bin/bash
#SBATCH -p gpu-troja
#SBATCH --mem=16G
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --time=00:30:00
#SBATCH -o /home/balhar/my-luster/awesome-align/logs/eval_logs/eval_%j.out

MODEL_NAME_OR_PATH=$1
DATA_FILE=$2
OUTPUT_FILE=$3

awesome-align \
	--output_file=$OUTPUT_FILE \
	--model_name_or_path=$MODEL_NAME_OR_PATH \
	--data_file=$DATA_FILE \
	--extraction 'softmax' \
	--batch_size 32
