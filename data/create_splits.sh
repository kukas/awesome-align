#!/bin/bash
# create valid and train splits
if [ $# -ne 1 ]; then
    echo "Usage: $0 filename"
    exit 1
fi
filename=$1
lines=$(wc -l < $filename)
echo "$lines lines"
valid_size=$(($lines / 10))
head -n $valid_size $filename > $filename.valid
tail -n $(($lines-$valid_size)) $filename > $filename.train
# valid_size=$(($lines))
