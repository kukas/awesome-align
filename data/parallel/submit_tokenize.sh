#!/bin/bash

# en-cs
# sbatch run_tokenize.sh cs-en/original_data/train.eng cs-en/tokenized_data/train.en en
sbatch run_tokenize.sh cs-en/original_data/train.ces cs-en/tokenized_data/train.cs cs
# en-de
# sbatch run_tokenize.sh en-de/original_data/train.eng en-de/tokenized_data/train.en en
# sbatch run_tokenize.sh en-de/original_data/train.deu en-de/tokenized_data/train.de de

# en-es
# sbatch run_tokenize.sh en-es/original_data/train.eng en-es/tokenized_data/train.en en
# sbatch run_tokenize.sh en-es/original_data/train.spa en-es/tokenized_data/train.es es

# en-fr
# sbatch run_tokenize.sh en-fr/original_data/train.eng en-fr/tokenized_data/train.en en
# sbatch run_tokenize.sh en-fr/original_data/train.fra en-fr/tokenized_data/train.fr fr

# en-pl
# sbatch run_tokenize.sh en-pl/original_data/train.eng en-pl/tokenized_data/train.en en
# sbatch run_tokenize.sh en-pl/original_data/train.pol en-pl/tokenized_data/train.pl pl

# ru-cs
# sbatch run_tokenize.sh ru-cs/original_data/train.rus ru-cs/tokenized_data/train.ru ru
# sbatch run_tokenize.sh ru-cs/original_data/train.ces ru-cs/tokenized_data/train.cs cs

