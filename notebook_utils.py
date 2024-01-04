from glob import glob
import re
from tqdm import tqdm
import sys
sys.path.append("tools")
from aer import main as compute_aer, parse_args as parse_aer_args

aer_args = parse_aer_args()

def load_all_results():
    paths = glob("finetune/*/checkpoint-*/*.awesome-align.out")
    results = []
    for path in tqdm(paths):
        path_match = re.search(r'finetune/(.+)/checkpoint-(\d+)/(.+)\.awesome-align\.out', path)
        experiment_name, step, lang_short = path_match.group(1), int(path_match.group(2)), path_match.group(3)
        lang = lang_short[:2] + '-' + lang_short[2:]
        path_gold = f"data/annotated/{lang}/{lang_short}.gold"
        if lang in ("en-fr", "de-en", "es-fr", "ja-en", "ro-en", "zh-en"):
            script_params = ["--oneRef"]
        elif lang in ("cs-uk", "en-cs"):
            script_params = []
        else:
            raise ValueError("Unsupported language")
        aer, precision, recall, f1 = evaluate(path_gold, path, script_params)
        results.append({
            "experiment_name": experiment_name,
            "step": step,
            "lang": lang,
            "aer": aer,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
    return results

def load_results_for_one_checkpoint(path, experiment_name, step):
    paths = glob(f"{path}/*.awesome-align.out")
    results = []
    for path in paths:
        # print(path)
        path_match = re.search(r'(.+)\.awesome-align\.out', path.split("/")[-1])
        lang_short = path_match.group(1)
        lang = lang_short[:2] + '-' + lang_short[2:]
        path_gold = f"data/annotated/{lang}/{lang_short}.gold"
        if lang in ("en-fr", "de-en", "es-fr", "ja-en", "ro-en", "zh-en"):
            script_params = ["--oneRef"]
        elif lang in ("cs-uk", "en-cs"):
            script_params = []
        else:
            raise ValueError("Unsupported language")
        aer, precision, recall, f1 = evaluate(path_gold, path, script_params)
        results.append({
            "experiment_name": experiment_name,
            "step": step,
            "lang": lang,
            "aer": aer,
            "precision": precision,
            "recall": recall,
            "f1": f1
        })
    return results


def evaluate(path_gold, path, script_params):
    # command = ["python", "tools/aer.py", path_gold, path]+script_params
    # result = subprocess.run(command, capture_output=True, text=True)
    # if result.returncode != 0:
    #     print(result.stdout)
    #     print(result.stderr)
    #     raise Exception
    # result = re.search(r': (\d+.\d+)% \((\d+.\d+)%/(\d+.\d+)%/\d+\)\nF-Measure: (\d+.\d+)', result.stdout)
    # aer, precision, recall, f1 = float(result.group(1)), float(result.group(2)), float(result.group(3)), float(result.group(4))
    args = aer_args.parse_args([path_gold, path] + script_params)
    aer, precision, recall, f1 = compute_aer(args, printit=False)
    return aer, precision, recall, f1

def load_results(finetuning_name, add=0, lang="cs-uk", baseline="bert-base-multilingual-cased", script_params=[]):
    lang_short = lang.replace('-', '')
    paths = glob(f"finetune/{finetuning_name}/checkpoint-*/{lang_short}.awesome-align.out")
    steps = list(map(lambda path: int(re.search(r'checkpoint-(\d+)', path).group(1)), paths))
    steps_paths = sorted(list(zip(steps, paths)))
    if add == 0 and baseline is not None:
        steps_paths = [(0, f"finetune/{baseline}/{lang_short}.awesome-align.out")] + steps_paths

    results = []
    path_gold = f"data/annotated/{lang}/{lang_short}.gold"
    for step, path in steps_paths:
        aer, precision, recall, f1 = evaluate(path_gold, path, script_params)
        results.append((step + add, aer))

        # alternative evaluation script by Michal Novák:
        # command = ["python", "/lnet/troja/work/people/mnovak/word_align/tools/eval.py", path_gold, path]
        #result = subprocess.run(command, capture_output=True, text=True)
        #result = float(re.search(r'AER = (\d+.\d+)%', result.stdout).group(1))
        #print(result)
        #results2.append((step, result))
    return results

# import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import statsmodels.api as sm
def plot_results(plt, results, title="", smooth=False):
    # plot results without any smoothing
    colors = mcolors.TABLEAU_COLORS.keys()
    for color, (label, res) in zip(colors, results.items()):
        x, y = zip(*res)
        if smooth:
            plt.plot(x, y, alpha=0.3, color=color)
            z = sm.nonparametric.lowess(y, x, frac=0.1)
            plt.plot(z[:,0], z[:,1], label=label, color=color)
        else:
            plt.plot(x, y, label=label, color=color)

    plt.title(title)
    plt.xlabel("Training step")
    plt.ylabel("AER %")
    plt.legend(title="Experiment")