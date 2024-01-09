## Prepare data
```
wget http://www.l2f.inesc-id.pt/resources/translation/golden_collection.zip
unzip golden_collection
mkdir original_data
mv golden_collection original_data/
mkdir processed_data
# strip tags
python striptags.py original_data/golden_collection/sentences/1-100-final.es processed_data/esfr.src
python striptags.py original_data/golden_collection/sentences/1-100-final.fr processed_data/esfr.tgt
# combine sentences into one file
python ../../../tools/combine.py processed_data/esfr.src processed_data/esfr.tgt esfr.src-tgt
# convert annotations to the Pharaoh format
python ../convert_annotations_flattened.py original_data/golden_collection/es-fr_1-100.wa esfr.gold
```
