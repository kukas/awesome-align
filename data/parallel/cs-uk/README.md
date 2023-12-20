To prepare the data:
1. Tokenize it
```bash
python tokenize.py original_data/full8M.uk tokenized_data/full8M.uk uk
python tokenize.py original_data/full8M.cs tokenized_data/full8M.cs cs
```
2. Merge it
```bash
./combine.sh tokenized_data/full8M.cs tokenized_data/full8M.uk prepared_data/full8M.csuk
```
3. Create splits
```bash
./create_splits.sh prepared_data/full8M.csuk
```