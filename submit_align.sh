#!/bin/bash
echo $@
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 model_path lang1 lang2"
    exit 1
fi
LANG1=$2
LANG2=$3
DATA_FILE="data/annotated/$LANG1-$LANG2/$LANG1$LANG2.src-tgt"
for model_path in $1/checkpoint*
do
    if [ ! -f  $model_path/$LANG1$LANG2.awesome-align.out ]
    then
        PARAMS="$model_path $DATA_FILE $model_path/$LANG1$LANG2.awesome-align.out"
        echo $PARAMS
	    sbatch run_align.sh $PARAMS
    fi
done

# example:
# ./submit_align.sh finetune/mbert_multilingual_1M-per-lang_finegrained es fr

# submit one:
# sbatch run_align.sh bert-base-multilingual-cased data/annotated/en-fr/enfr.src-tgt finetune/bert-base-multilingual-cased/enfr.awesome-align.out