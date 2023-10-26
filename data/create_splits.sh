#!/bin/bash
# TODO: tokenize
# to combine line by line
# :|paste -d ' ||| ' full8M.cs.train - - - - full8M.uk.train  > full8M.csuk.train 
filename=$1
lines=$(wc -l < $filename)
echo "$lines lines"
valid_size=$(($lines / 10))
head -n $valid_size $filename > $filename.valid
tail -n $(($lines-$valid_size)) $filename > $filename.train
# valid_size=$(($lines))
