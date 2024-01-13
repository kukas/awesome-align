import random
import argparse
import sys
import os
from convert_annotations_utils import Alignment

def read_data(input_src_tgt_file, input_gold_file):
    with open(input_src_tgt_file, "r") as f:
        src_tgt_data = f.readlines()
        # split to src sentence and tgt sentence
        src_tgt_data = [line.strip().split(" ||| ") for line in src_tgt_data]
        # split to tokens
        src_tgt_data = [(src.split(), tgt.split()) for src, tgt in src_tgt_data]
    with open(input_gold_file, "r") as f:
        gold_data = f.readlines()
        gold_data = [[Alignment.from_string(index_pair) for index_pair in line.strip().split()] for line in gold_data]

    return list(zip(src_tgt_data, gold_data))

def sample_data(data, num_paragraphs, num_sentences):
    sampled_data = []
    for i in range(num_paragraphs):
        sample = random.sample(data, num_sentences)
        
        sampled_data.append(sample)
    return sampled_data

def write_data(sampled_data, output_src_tgt_file, output_gold_file):
    with open(output_src_tgt_file, "w") as src_tgt_file, open(output_gold_file, "w") as gold_file:
        for samples in sampled_data:
            src_tokens = []
            tgt_tokens = []
            annotations = []
            for (src, tgt), gold in samples:
                current_lengths = (len(src_tokens), len(tgt_tokens))
                src_tokens += src
                tgt_tokens += tgt
                offset_gold = [annot + current_lengths for annot in gold]
                annotations += offset_gold
            src_tgt = " ".join(src_tokens) + " ||| " + " ".join(tgt_tokens)
            gold = " ".join(map(str, annotations))
            src_tgt_file.write(src_tgt + "\n")
            gold_file.write(gold + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_src_tgt_file", type=str)
    parser.add_argument("input_gold_file", type=str)
    parser.add_argument("output_src_tgt_file", type=str)
    parser.add_argument("output_gold_file", type=str)
    parser.add_argument("num_paragraphs", type=int)
    parser.add_argument("num_sentences", type=int)

    args = parser.parse_args()

    data = read_data(args.input_src_tgt_file, args.input_gold_file)
    sampled_data = sample_data(data, args.num_paragraphs, args.num_sentences)
    write_data(sampled_data, args.output_src_tgt_file, args.output_gold_file)