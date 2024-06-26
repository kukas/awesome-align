#!/bin/bash
# combine two files line by line
if [ $# -ne 3 ]; then
    echo "Usage: $0 file1 file2 output"
    exit 1
fi
# slow:
# :|paste -d ' ||| ' $1 - - - - $2 > $3
python ../../tools/combine.py $1 $2 $3
# faster:
# awk 'FNR==1 && NR!=1 {print "---"}{print}' $1 $2 > $3
