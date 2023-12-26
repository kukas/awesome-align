set -x
mkdir -p en-de/prepared_data en-es/prepared_data en-fr/prepared_data en-pl/prepared_data ru-cs/prepared_data cs-en/prepared_data

# time ./combine.sh cs-en/tokenized_data/train.en cs-en/tokenized_data/train.cs cs-en/prepared_data/train.cs-en
# time ./combine.sh en-es/tokenized_data/train.en en-es/tokenized_data/train.es en-es/prepared_data/train.en-es
# time ./combine.sh en-de/tokenized_data/train.en en-de/tokenized_data/train.de en-de/prepared_data/train.en-de
# time ./combine.sh en-fr/tokenized_data/train.en en-fr/tokenized_data/train.fr en-fr/prepared_data/train.en-fr
# time ./combine.sh en-pl/tokenized_data/train.en en-pl/tokenized_data/train.pl en-pl/prepared_data/train.en-pl
# time ./combine.sh ru-cs/tokenized_data/train.ru ru-cs/tokenized_data/train.cs ru-cs/prepared_data/train.ru-cs

mkdir -p all_pairs

time shuf -n 1000000 cs-uk/prepared_data/full8M.csuk.train > all_pairs/train.txt
time shuf -n 1000000 cs-en/prepared_data/train.cs-en >> all_pairs/train.txt
time shuf -n 1000000 en-es/prepared_data/train.en-es >> all_pairs/train.txt
time shuf -n 1000000 en-de/prepared_data/train.en-de >> all_pairs/train.txt
time shuf -n 1000000 en-fr/prepared_data/train.en-fr >> all_pairs/train.txt
time shuf -n 1000000 en-pl/prepared_data/train.en-pl >> all_pairs/train.txt
time shuf -n 1000000 ru-cs/prepared_data/train.ru-cs >> all_pairs/train.txt