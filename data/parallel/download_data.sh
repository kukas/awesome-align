#!/bin/bash
mkdir -p en-de/original_data en-es/original_data en-fr/original_data en-pl/original_data ru-cs/original_data en-cs/original_data

mtdata get -l eng-deu --merge --train OPUS-opus100_train-1-deu-eng -o en-de/original_data
mtdata get -l eng-spa --merge --train OPUS-opus100_train-1-eng-spa -o en-es/original_data
mtdata get -l eng-fra --merge --train OPUS-opus100_train-1-eng-fra -o en-fr/original_data
mtdata get -l eng-pol --merge --train OPUS-opus100_train-1-eng-pol -o en-pl/original_data
mtdata get -l rus-ces --merge --train Statmt-news_commentary-16-ces-rus -o ru-cs/original_data
# use czeng20-train instead
# mtdata get -l eng-ces --merge --train OPUS-opus100_train-1-ces-eng -o en-cs/original_data
