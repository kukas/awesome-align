#!/bin/bash
#SBATCH -p gpu-troja
#SBATCH --mem=64G
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:3
#SBATCH --constraint="gpuram48G"
#SBATCH --time=14-0
#SBATCH -o /home/balhar/my-luster/awesome-align/logs/training_logs/finetune_%j.out

TRAIN_FILE=data/parallel/all_pairs/train.txt
COMMON_ARGS="--extraction softmax \
    --do_train \
    --train_tlm \
    --train_data_file=$TRAIN_FILE \
    --per_gpu_train_batch_size 8 \
    --gradient_accumulation_steps 1 \
    --num_train_epochs 1 \
    --learning_rate 2e-5 \
    --cache_data \
    --overwrite_output_dir"

# awesome-train \
#     $COMMON_ARGS \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained \
#     --model_name_or_path=bert-base-multilingual-cased \
#     --train_so \
#     --save_steps 200

# awesome-train \
#      $COMMON_ARGS \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm \
#     --model_name_or_path=bert-base-multilingual-cased \
#     --save_steps 200

# awesome-train \
#      $COMMON_ARGS \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_all_objectives \
#     --model_name_or_path=bert-base-multilingual-cased \
#     --train_mlm \
#     --train_tlm \
#     --train_tlm_full \
#     --train_so \
#     --train_psi \
#     --max_steps 40000

# awesome-train \
#      $COMMON_ARGS \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm_lr2e-4 \
#     --model_name_or_path=bert-base-multilingual-cased \
#     --learning_rate 2e-4 \
#     --save_steps 200

# awesome-train \
#     $COMMON_ARGS \
#     --model_name_or_path=finetune/mbert_multilingual_1M-per-lang_finegrained/checkpoint-45000 \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_continue \
#     --train_so \
#     --seed 20 \
#     --save_steps 2000


# awesome-train \
#     $COMMON_ARGS \
#     --model_name_or_path=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm/checkpoint-45000 \
#     --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm_continue \
#     --seed 20 \
#     --save_steps 2000


awesome-train \
    $COMMON_ARGS \
    --model_name_or_path=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm_continue/checkpoint-290000 \
    --output_dir=finetune/mbert_multilingual_1M-per-lang_finegrained_only_tlm_continue_add_so_lr5e-6 \
    --train_so \
    --seed 30 \
    --save_steps 200 \
    --max_steps 20000 \
    --learning_rate 5e-6

