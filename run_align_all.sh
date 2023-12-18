#!/bin/bash

DATA_FILE="data_manual/csuk.src-tgt"
for model_path in finetune/mbert_full8M_1epoch/checkpoint*
do
    echo run_align.sh $model_path $DATA_FILE $model_path/csuk.awesome-align.out
    sbatch run_align.sh $model_path $DATA_FILE $model_path/csuk.awesome-align.out
    break
done
