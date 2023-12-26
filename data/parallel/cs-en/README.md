## Data preparation
```
gzip -dkc /net/data/czeng20/czeng20-train.gz > czeng20-train
# head czeng20-train | awk -F'\t' 'NF && NF==6 {print $5 " --- " $6}'
awk -F'\t' 'NF==6 {print $5}' czeng20-train > train.ces
awk -F'\t' 'NF==6 {print $6}' czeng20-train > train.eng
