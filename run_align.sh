DATA_FILE=data/prepared_data/full8M.csuk.valid.10000
#MODEL_NAME_OR_PATH=bert-base-multilingual-cased
MODEL_NAME_OR_PATH=$1
#OUTPUT_FILE=outputs/full8M.csuk.valid.nofinetune
OUTPUT_FILE=outputs/full8M.csuk.valid.$2

CUDA_VISIBLE_DEVICES=0 awesome-align \
	--output_file=$OUTPUT_FILE \
	--model_name_or_path=$MODEL_NAME_OR_PATH \
	--data_file=$DATA_FILE \
	--extraction 'softmax' \
	--batch_size 32
