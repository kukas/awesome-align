#!/bin/bash
echo $@
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 model_path [data files...]"
    exit 1
fi
model_path=$1
shift
data_paths=$@
for data_path in $data_paths
do
    data_file=$(basename $data_path)
    # remove extension
    data_file=${data_file%.*}
    output_path=$model_path/$data_file.awesome-align.out
    if [ ! -f  $output_path ]
    then
        PARAMS="$model_path $data_path $output_path"
        echo $PARAMS
	    sbatch run_align.sh $PARAMS
    fi
done

# example:
# ./submit_align.sh finetune/mbert_multilingual_1M-per-lang_finegrained es fr

# submit one:
# sbatch run_align.sh bert-base-multilingual-cased data/annotated/en-fr/enfr.src-tgt finetune/bert-base-multilingual-cased/enfr.awesome-align.out