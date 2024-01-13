import torch
from data.parallel.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner
from map_tokenizations import map_tokenization, granularize_tokenization
from timeit import default_timer as timer
import pandas as pd
from tqdm import tqdm

def test_sequence_size(aligner, sequence_size, batch_size):
    src_text = " ".join(["hi" for i in range(sequence_size)])
    tgt_text = " ".join(["hi" for i in range(sequence_size)])
    line = f"{src_text} ||| {tgt_text}"
    lines = [line for i in range(batch_size)]
    try:
        print("bs=",batch_size, "-", end="")
        al = aligner.align(lines, batch_size=batch_size)
        torch.cuda.empty_cache()
        return True
    except torch.cuda.OutOfMemoryError as e:
        print("OOM")
        return False

def binary_search(bs_a, bs_b, aligner, sequence_size):
    if bs_b - bs_a <= 1:
        return bs_a, bs_b
    mid = (bs_a + bs_b) // 2
    if test_sequence_size(aligner, sequence_size, mid):
        return binary_search(mid, bs_b, aligner, sequence_size)
    else:
        return binary_search(bs_a, mid, aligner, sequence_size)


def main():
    print("Loading awesome aligner...")
    model_name_or_path = "finetune/mbert_multilingual_1M-per-lang_only_tlm_add_so_lr5e-6/checkpoint-8600"
    aligner = AwesomeAligner(model_name_or_path=model_name_or_path)
    print("Model loaded.")

    # test long sequences
    # for sequence_size in range(1, 2000, 10):
    #     src_text = " ".join(["hi" for i in range(sequence_size)])
    #     tgt_text = " ".join(["hi" for i in range(sequence_size)])
    #     line = f"{src_text} ||| {tgt_text}"
    #     al = aligner.align(line)
    #     print(sequence_size, al)

    # result: tokens with index higher than 509 are not aligned

    # test OOM
    for sequence_size in range(512, 400, -1):
        # sequence_size = 509//s
        print("testing sequence size", sequence_size)
        found = binary_search(250, 300, aligner, sequence_size)
        print("found bs range ", found, "for sequence size", sequence_size)

if __name__ == "__main__":
    main()