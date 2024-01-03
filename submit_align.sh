#!/bin/bash

DATA_FILE="data/annotated/cs-uk/csuk.src-tgt"
for model_path in $1/checkpoint*
do
    if [ ! -f  $model_path/csuk.awesome-align.out ]
    then
	echo run_align.sh $model_path $DATA_FILE $model_path/csuk.awesome-align.out
	sbatch run_align.sh $model_path $DATA_FILE $model_path/csuk.awesome-align.out
    fi
done
