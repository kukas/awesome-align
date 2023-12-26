#!/bin/bash
#SBATCH -p gpu-troja
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:3
#SBATCH --constraint="gpuram48G"
#SBATCH --time=14-0
#SBATCH -o /home/balhar/my-luster/awesome-align/logs/training_logs/finetune_%j.out

TRAIN_FILE=data/parallel/all_pairs/train.txt
EVAL_DATA_FILE=data/annotated/de-en/deen.src-tgt
EVAL_GOLD_FILE=data/annotated/de-en/deen.gold
OUTPUT_DIR=finetune/mbert_multilingual_1M-per-lang

# source /home/balhar/my-luster/awesome-align/awesome_align_env/bin/activate

awesome-train \
    --output_dir=$OUTPUT_DIR \
    --model_name_or_path=bert-base-multilingual-cased \
    --extraction 'softmax' \
    --do_train \
    --train_tlm \
    --train_so \
    --train_data_file=$TRAIN_FILE \
    --per_gpu_train_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --num_train_epochs 10 \
    --learning_rate 2e-5 \
    --save_steps 10000 \
    --cache_data \
    --do_eval \
    --eval_data_file=$EVAL_DATA_FILE \
    --eval_gold_file=$EVAL_GOLD_FILE \
    --overwrite_output_dir
    # --max_steps 20000
