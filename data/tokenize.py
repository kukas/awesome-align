import argparse
import os
import tqdm
import mosestokenizer
import tokenize_uk

def get_tokenizer(language):
    if language == "uk":
        return tokenize_uk.tokenize_words
    elif language == "cs":
        moses = mosestokenizer.MosesTokenizer('cs', no_escape=True) # Turn off html escaping
        def _tokenize(line):
            output = moses(line)
            # Replace @-@ with -, Moses adds the @ symbols because of aggressive hyphen splitting
            output = [x if x != "@-@" else "-" for x in output]
            return output
        return _tokenize
    else:
        raise ValueError(f"Unknown language {language}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    parser.add_argument("language", type=str, choices=["uk", "cs"])
    args = parser.parse_args()

    tokenizer = get_tokenizer(args.language)

    with open(args.input, "r") as f:
        with open(args.output, "w") as out:
            num_lines = sum(1 for _ in f)
            f.seek(0)
            for line in tqdm.tqdm(f, desc="Tokenizing", total=num_lines):
                tokenized = tokenizer(line.strip())
                out.write(" ".join(tokenized) + "\n")

if __name__ == "__main__":
    main()
