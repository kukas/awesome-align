def granularize_tokenization(coarse_tokenization, tokenizer):
    """
    Maps coarse tokenization into a more granular tokenization.
    """
    granular_tokenization = []
    granular_to_coarse_mapping = {}
    j = 0
    for i, token in enumerate(coarse_tokenization):
        subtokens = tokenizer(token)
        for subtoken in subtokens:
            granular_tokenization.append(subtoken)
            granular_to_coarse_mapping[j] = i
            j += 1
    return granular_tokenization, granular_to_coarse_mapping

def map_tokenization(granular_alignment, src_token_mapping, trg_token_mapping):
    """
    Maps the granular_alignment into a more corse alignment
    using the src_token_mapping and trg_token_mapping.
    """
    # We do not want duplicate alignments so we keep track of them in a set
    alignment_set = set()
    alignment = []
    for i, j in granular_alignment:
        mapped_alignment = (src_token_mapping[i], trg_token_mapping[j])
        if mapped_alignment in alignment_set:
            continue
        alignment.append(list(mapped_alignment))
        alignment_set.add(mapped_alignment)
    return alignment

def batch_granularize_tokenization(coarse_tokenizations, tokenizer):
    tokenizations_and_mappings = [granularize_tokenization(coarse_tokenization, tokenizer) for coarse_tokenization in coarse_tokenizations]
    return list(zip(*tokenizations_and_mappings))

def batch_map_tokenization(granular_alignments, src_token_mappings, trg_token_mappings):
    return [map_tokenization(*args) for args in zip(granular_alignments, src_token_mappings, trg_token_mappings)]