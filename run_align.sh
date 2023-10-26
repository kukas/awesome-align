DATA_FILE=data/full8M.csuk.valid
MODEL_NAME_OR_PATH=bert-base-multilingual-cased
OUTPUT_FILE=outputs/full8M.csuk.valid.nofinetune

CUDA_VISIBLE_DEVICES=0 awesome-align \
	    --output_file=$OUTPUT_FILE \
	        --model_name_or_path=$MODEL_NAME_OR_PATH \
		    --data_file=$DATA_FILE \
		        --extraction 'softmax' \
			    --batch_size 32
