import argparse
import os
import tqdm
import mosestokenizer
import tokenize_uk

moses_langs = ["ca","cs","de","el","en","es","fi","fr","hu","is","it","lv","nl","pl","pt","ro","ru","sk","sl","sv","ta"]
tokenizers = {}

def get_tokenizer(language):
    """
    Returns a tokenizer function based on the specified language.

    Parameters:
        language (str): The language for which the tokenizer function is needed.

    Returns:
        function: A tokenizer function that can be used to tokenize text in the specified language.

    Raises:
        ValueError: If the specified language is not supported.
    """
    def _moses_factory(language):
        # Turn off html escaping
        if language in tokenizers:
            moses = tokenizers[language]
        else:
            moses = mosestokenizer.MosesTokenizer(language, no_escape=True)
            tokenizers[language] = moses

        def _tokenize(line):
            output = moses(line)
            # Replace @-@ with -, Moses adds the @ symbols because of aggressive hyphen splitting
            output = [x if x != "@-@" else "-" for x in output]
            return output
        
        return _tokenize

    if language == "uk":
        return tokenize_uk.tokenize_words
    elif language in moses_langs:
        return _moses_factory(language)
    else:
        return _moses_factory("en")  # Default to English if the language is not supported

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    parser.add_argument("output", type=str)
    parser.add_argument("language", type=str, choices=moses_langs + ["uk"])
    args = parser.parse_args()

    tokenizer = get_tokenizer(args.language)

    # check if input file exists
    if not os.path.exists(args.input):
        raise ValueError(f"Input file {args.input} does not exist")

    # check if output directory exists and create it if not
    output_dir = os.path.dirname(args.output)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.input, "r") as f:
        with open(args.output, "w") as out:
            num_lines = sum(1 for _ in f)
            f.seek(0)
            for line in tqdm.tqdm(f, desc="Tokenizing", total=num_lines):
                tokenized = tokenizer(line.strip())
                out.write(" ".join(tokenized) + "\n")


if __name__ == "__main__":
    main()
