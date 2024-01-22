import torch
from data.parallel.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner
from map_tokenizations import map_tokenization, granularize_tokenization
from timeit import default_timer as timer
import pandas as pd
from tqdm import tqdm
import cProfile

def run(lines, aligner, iters, batch_size):
    for _ in tqdm(range(iters), desc=f"Aligning req_size={len(lines)}, bs={batch_size}, seq_size=?"):
        aligner.align(lines, batch_size=batch_size)

def main():
    print("Loading awesome aligner...")
    model_name_or_path = "finetune/mbert_multilingual_1M-per-lang_only_tlm_add_so_lr5e-6/checkpoint-8600"
    aligner = AwesomeAligner(model_name_or_path=model_name_or_path)
    print("Model loaded.")

    lines = []
    with open("./data/annotated/en-cs/encs.src-tgt") as srctgt:
        for line in srctgt:
            lines.append(line.strip())
    lines = lines[:1]
    iters = 45
    batch_size = 1
    # dry run
    run(lines, aligner, 3, batch_size)

    start = timer()
    with cProfile.Profile() as pr:
        run(lines, aligner, iters, batch_size)
        pr.print_stats()
        pr.dump_stats("benchmark_profile_single_datamainprocess.prof")
    stop = timer()
    print("Time: ", stop - start)
    return stop - start


if __name__ == "__main__":
    main()