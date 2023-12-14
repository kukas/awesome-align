from time import perf_counter
from awesome_aligner import AwesomeAligner
def test_align():
    aa = AwesomeAligner(model_name_or_path="bert-base-multilingual-cased")
    alignment = aa.align("( projektový plán ) . ||| ( корегувати проект ) .")
    print(alignment)

def test_align_finetuned():
    aa = AwesomeAligner(model_name_or_path="./finetune/mbert_full8M_1epoch/checkpoint-28000")
    alignment = aa.align("( projektový plán ) . ||| ( корегувати проект ) .")
    print(alignment)

def benchmark_align():
    aa = AwesomeAligner(model_name_or_path="bert-base-multilingual-cased")
    data = [l.strip() for l in open("data/prepared_data/full8M.csuk.valid")]
    t = perf_counter()
    n = 100
    aa.align(data[:n])
    elapsed = perf_counter() - t
    print(f"Elapsed time {elapsed:.2f} ({n} samples)")
    print(f"Time per sample {elapsed/n:.2f}")

if __name__ == '__main__':
    test_align()
    test_align_finetuned()
    benchmark_align()