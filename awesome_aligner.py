# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
# Modifications copyright (C) 2020 Zi-Yi Dou
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import random
import itertools
import os
import shutil
import tempfile

import numpy as np
import torch
from tqdm import trange
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, IterableDataset

from awesome_align import modeling
from awesome_align.configuration_bert import BertConfig
from awesome_align.modeling import BertForMaskedLM
from awesome_align.tokenization_bert import BertTokenizer
from awesome_align.tokenization_utils import PreTrainedTokenizer
from awesome_align.modeling_utils import PreTrainedModel

def set_seed(seed):
    if seed >= 0:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

class AwesomeAligner():
    def __init__(self, model_name_or_path, extraction="softmax", align_layer=8, softmax_threshold=0.001, cache_dir=None, seed=0):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.extraction = extraction
        self.align_layer = align_layer
        self.softmax_threshold = softmax_threshold
        set_seed(seed)

        config_class, model_class, tokenizer_class = BertConfig, BertForMaskedLM, BertTokenizer
        config = config_class.from_pretrained(model_name_or_path, cache_dir=cache_dir)
        self.tokenizer = tokenizer_class.from_pretrained(model_name_or_path, cache_dir=cache_dir)

        modeling.PAD_ID = self.tokenizer.pad_token_id
        modeling.CLS_ID = self.tokenizer.cls_token_id
        modeling.SEP_ID = self.tokenizer.sep_token_id

        self.model = model_class.from_pretrained(
            model_name_or_path,
            from_tf=bool(".ckpt" in model_name_or_path),
            config=config,
            cache_dir=cache_dir,
        )

        # word_align(args, model, tokenizer)


    def process_line(self, line):
        if len(line) == 0 or line.isspace() or not len(line.split(' ||| ')) == 2:
            return None

        src, tgt = line.split(' ||| ')
        if src.rstrip() == '' or tgt.rstrip() == '':
            return None

        sent_src, sent_tgt = src.strip().split(), tgt.strip().split()
        token_src, token_tgt = [self.tokenizer.tokenize(word) for word in sent_src], [self.tokenizer.tokenize(word) for word in sent_tgt]
        wid_src, wid_tgt = [self.tokenizer.convert_tokens_to_ids(x) for x in token_src], [self.tokenizer.convert_tokens_to_ids(x) for x in token_tgt]

        ids_src, ids_tgt = self.tokenizer.prepare_for_model(list(itertools.chain(*wid_src)), return_tensors='pt', max_length=self.tokenizer.max_len)['input_ids'], self.tokenizer.prepare_for_model(list(itertools.chain(*wid_tgt)), return_tensors='pt', max_length=self.tokenizer.max_len)['input_ids']
        if len(ids_src[0]) == 2 or len(ids_tgt[0]) == 2:
            return None

        bpe2word_map_src = []
        for i, word_list in enumerate(token_src):
            bpe2word_map_src += [i for x in word_list]
        bpe2word_map_tgt = []
        for i, word_list in enumerate(token_tgt):
            bpe2word_map_tgt += [i for x in word_list]
        worker_id = 0
        return (worker_id, ids_src[0], ids_tgt[0], bpe2word_map_src, bpe2word_map_tgt, sent_src, sent_tgt) 


    def align(self, lines):
        # args, model, tokenizer

        def collate(examples):
            worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt = zip(*examples)
            ids_src = pad_sequence(ids_src, batch_first=True, padding_value=self.tokenizer.pad_token_id)
            ids_tgt = pad_sequence(ids_tgt, batch_first=True, padding_value=self.tokenizer.pad_token_id)
            return worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt

        num_workers = 1
        batch_size = 1

        # offsets = find_offsets(args.data_file, num_workers)
        # dataset = LineByLineTextDataset(tokenizer, file_path=args.data_file, offsets=offsets)
        lines = lines if isinstance(lines, list) else [lines]
        dataset = [self.process_line(line) for line in lines]
        dataloader = DataLoader(
            dataset, batch_size=batch_size, collate_fn=collate, num_workers=num_workers
        )

        self.model.to(self.device)
        self.model.eval()

        output_prob_file = None
        output_word_file = None

        # writers = open_writer_list(args.output_file, num_workers) 
        # if output_prob_file is not None:
        #     prob_writers = open_writer_list(output_prob_file, num_workers)
        # if output_word_file is not None:
        #     word_writers = open_writer_list(output_word_file, num_workers)
        all_alignments = []
        for batch in dataloader:
            with torch.no_grad():
                worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt = batch
                word_aligns_list = self.model.get_aligned_word(ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, self.device, 0, 0, align_layer=self.align_layer, extraction=self.extraction, softmax_threshold=self.softmax_threshold, test=True, output_prob=(output_prob_file is not None))
                for worker_id, word_aligns, sent_src, sent_tgt in zip(worker_ids, word_aligns_list, sents_src, sents_tgt):
                    output_str = []
                    # if output_prob_file is not None:
                    #     output_prob_str = []
                    # if output_word_file is not None:
                    #     output_word_str = []
                    all_alignments += word_aligns
                    # for word_align in word_aligns:
                    #     if word_align[0] != -1:
                    #         output_str.append(f'{word_align[0]}-{word_align[1]}')
                            # if output_prob_file is not None:
                            #     output_prob_str.append(f'{word_aligns[word_align]}')
                            # if output_word_file is not None:
                            #     output_word_str.append(f'{sent_src[word_align[0]]}<sep>{sent_tgt[word_align[1]]}')
                    # print(' '.join(output_str)+'\n')
                    # writers[worker_id].write(' '.join(output_str)+'\n')
                    # if output_prob_file is not None:
                    #     prob_writers[worker_id].write(' '.join(output_prob_str)+'\n')
                    # if output_word_file is not None:
                    #     word_writers[worker_id].write(' '.join(output_word_str)+'\n')

        # merge_files(writers)
        # if output_prob_file is not None:
        #     merge_files(prob_writers)
        # if output_word_file is not None:
        #     merge_files(word_writers)
        return sorted(all_alignments)

