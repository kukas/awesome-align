#!/bin/bash
#SBATCH -p gpu-troja
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --time=23:59:00
#SBATCH -o /home/balhar/my-luster/awesome-align/training_logs/finetune_%j.out

TRAIN_FILE=data/prepared_data/full8M.csuk.train
OUTPUT_DIR=finetune/mbert_full8M_1epoch

# source /home/balhar/my-luster/awesome-align/awesome_align_env/bin/activate

 awesome-train \
    --output_dir=$OUTPUT_DIR \
    --model_name_or_path=bert-base-multilingual-cased \
    --extraction 'softmax' \
    --do_train \
    --train_tlm \
    --train_so \
    --train_data_file=$TRAIN_FILE \
    --per_gpu_train_batch_size 4 \
    --gradient_accumulation_steps 2 \
    --num_train_epochs 1 \
    --learning_rate 2e-5 \
    --save_steps 4000
    # --max_steps 20000
    # --do_eval
    # --eval_data_file=$EVAL_FILE