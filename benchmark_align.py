from data.parallel.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner
from map_tokenizations import map_tokenization, granularize_tokenization
from timeit import default_timer as timer
import pandas as pd
from tqdm import tqdm
def main():
    df = pd.read_csv("benchmark_align_2.csv",index_col=0).reset_index(drop=True)

    print("Loading awesome aligner...")
    model_name_or_path = "finetune/mbert_multilingual_1M-per-lang_only_tlm_add_so_lr5e-6/checkpoint-8600"
    aligner = AwesomeAligner(model_name_or_path=model_name_or_path)
    print("Model loaded.")
    # warm up
    print("Warming up...")
    for _ in range(10):
        aligner.align("hi ||| hi")
    print("Warming up done.")

    results = pd.read_csv("benchmark_align_2.csv",index_col=0).reset_index(drop=True).to_dict("records")
    iters = 50
    for sequence_size in [4,8,16,32,64,128,256,512]:
        for request_size in [1,2,4,8,16,32,64,128]:
            for bs in [1,2,4,8,16,32,64,128]:
                if ((df.sequence_size==sequence_size) & (df.request_size==request_size) & (df.batch_size==bs)).any():
                    print(f"Skipping {sequence_size}, {request_size}, {bs}")
                    continue
                t = test_aligner(aligner, request_size, bs, sequence_size, iters=iters)
                results.append({
                    "batch_size": bs,
                    "request_size": request_size,
                    "sequence_size": sequence_size,
                    "iters": iters,
                    "time": t
                })
                pd.DataFrame(results).to_csv("benchmark_align_2.csv")
    return results

def test_aligner(aligner, request_size, batch_size, sequence_size, iters):
    # create dummy data
    src_text = " ".join(["hi" for i in range(sequence_size)])
    tgt_text = " ".join(["hi" for i in range(sequence_size)])
    line = f"{src_text} ||| {tgt_text}"
    lines = [line for i in range(request_size)]

    start = timer()
    for _ in tqdm(range(iters), desc=f"Aligning req_size={request_size}, bs={batch_size}, seq_size={sequence_size}"):
        aligner.align(lines, batch_size=batch_size)
    stop = timer()
    print("Time: ", stop - start)
    return stop - start


if __name__ == "__main__":
    main()