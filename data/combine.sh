#!/bin/bash
# combine two files line by line
if [ $# -ne 3 ]; then
    echo "Usage: $0 file1 file2 output"
    exit 1
fi
:|paste -d ' ||| ' $1 - - - - $2 > $3