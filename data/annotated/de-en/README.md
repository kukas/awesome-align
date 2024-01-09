```
wget https://raw.githubusercontent.com/lilt/alignment-scripts/master/preprocess/deen-test.sh
tar -xvzf original_data/DeEnGoldAlignment.tar.gz
mv DeEn/ original_data/
cd original_data/
export prefix="deen"
export DIR_NAME="DeEn"
sed '/^[[:space:]]*$/d' < ${DIR_NAME}/alignmentDeEn.talp > ${prefix}.talp
cat ${DIR_NAME}/de | sed '/^[[:space:]]*$/d' | iconv -f latin1 -t utf-8 > ${prefix}.src
cat ${DIR_NAME}/en | sed '/^[[:space:]]*$/d' | iconv -f latin1 -t utf-8 > ${prefix}.tgt
cd ..
python ../../../tools/combine.py original_data/deen.src original_data/deen.tgt deen.src-tgt
cp original_data/deen.talp deen.gold
```