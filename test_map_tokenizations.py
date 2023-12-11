import re
from random import shuffle, seed
from map_tokenizations import map_tokenization, granularize_tokenization
#                   0       1       2         3         4    5
user_src_tokens = ["Dnes", "jsem", "potkal", "tchýni", "a", "ex-přítelkyni"]
#                   0        1    2      3     4                5      6
user_trg_tokens = ["Today", "I", "met", "my", "mother-in-law", "and", "ex-girlfriend"]
coarse_alignment = [[0, 0], [1, 1], [2, 2], [3, 4], [4, 5], [5, 6]]

#                          0       1       2         3         4    5     6    7
granular_src_tokens = ["Dnes", "jsem", "potkal", "tchýni", "a", "ex", "-", "přítelkyni"]
#                          0        1    2      3     4         5    6     7    8      9      10    11   12
granular_trg_tokens = ["Today", "I", "met", "my", "mother", "-", "in", "-", "law", "and", "ex", "-", "girlfriend"]
# this is the hypothetical output from our aligner:
granular_alignment = [[0, 0], [1, 1], [2, 2], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8], [4, 9], [5, 10], [6, 11], [7, 12]]

# the mapping is from granular to coarse
src_token_mapping = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:5, 7:5}
trg_token_mapping = {0:0, 1:1, 2:2, 3:3, 4:4, 5:4, 6:4, 7:4, 8:4, 9:5, 10:6, 11:6, 12:6}


def dummy_granular_tokenizer_dash(sentence):
    return re.split(r'(-)', sentence)

def dummy_granular_tokenizer_noop(sentence):
    return sentence

def dummy_granular_tokenizer_crazy(sentence):
    toks = re.split(r'(\w\w)', sentence)
    return [tok for tok in toks if tok != '']

def test_granularize_tokenization():
    granular_result, granular_to_coarse_mapping = granularize_tokenization(user_src_tokens, dummy_granular_tokenizer_dash)

    assert granular_result == granular_src_tokens
    assert granular_to_coarse_mapping == src_token_mapping

    granular_result, granular_to_coarse_mapping = granularize_tokenization(user_trg_tokens, dummy_granular_tokenizer_dash)
    print(user_trg_tokens)
    print(granular_result)
    print(granular_trg_tokens)
    print(granular_to_coarse_mapping)
    print(trg_token_mapping)
    assert granular_result == granular_trg_tokens
    assert granular_to_coarse_mapping == trg_token_mapping

    # granular_src_result, granular_to_coarse_mapping = granularize_tokenization(user_src_tokens, dummy_granular_tokenizer_crazy)
    # print(granular_to_coarse_mapping)

def test_map_tokenization():
    # we want to get the coarse_alignment from granular_alignment
    alignment = map_tokenization(granular_alignment, src_token_mapping, trg_token_mapping)

    assert alignment == coarse_alignment

    seed(42)
    shuffle(granular_alignment)
    alignment = map_tokenization(granular_alignment, src_token_mapping, trg_token_mapping)
    assert sorted(alignment) == sorted(coarse_alignment)


if __name__ == "__main__":
    test_map_tokenization()
    test_granularize_tokenization()