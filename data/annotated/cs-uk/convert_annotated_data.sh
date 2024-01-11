#!/bin/bash

python ../convert_annotations_alpaco.py mariia_annotated/flores.wa flores.gold flores.src-tgt
python ../convert_annotations_alpaco.py mariia_annotated/khan.wa khan.gold khan.src-tgt
cat flores.gold khan.gold > csuk.gold
cat flores.src-tgt khan.src-tgt > csuk.src-tgt
