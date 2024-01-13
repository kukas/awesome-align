import os
  
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS

import sys
import re
from pprint import pprint

from data.parallel.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner
from map_tokenizations import map_tokenization, granularize_tokenization

# align_models_path = os.path.join(fast_align_dir, 'models')

def create_aligner(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.json.mimetype = "application/json; charset=utf-8"
    CORS(app)

    supported_languages = ["uk", "cs", "fr", "de", "es", "pl", "ru", "en"]
    tokenizers = {}
    for lang in supported_languages:
        tokenizers[lang] = get_tokenizer(lang)

    app.logger.info("Loading awesome aligner...")
    model_name_or_path = "finetune/mbert_multilingual_1M-per-lang_only_tlm_add_so_lr5e-6/checkpoint-8600"
    csuk_aligner = AwesomeAligner(model_name_or_path=model_name_or_path)
    app.logger.info("Model loaded.")

    @app.route("/")
    def index():
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # info page
    @app.route('/info')
    def info():
        return 'Word alignment server (AwesomeAligner, model: {:s})'.format(model_name_or_path)
    
    def tokenize_text(text, tokenizer):
        normalize_spaces = " ".join(text.split())
        return tokenizer(normalize_spaces)
    
    def compute_alignment(src_tokens, trg_tokens):
        align = []
        if len(src_tokens) > 0 and len(trg_tokens) > 0:
            line = "{:s} ||| {:s}".format(" ".join(src_tokens), " ".join(trg_tokens))
            align = csuk_aligner.align(line)
        return align

    # align cs-uk
    @app.route('/align/<path:lang_pair>', methods=['POST'])
    def align_csuk(lang_pair):
        req_data = request.get_json()

        # máme buď tokeny nebo text
        # pokud máme text, tak tokenizujeme, alignujeme tyto tokenizace a vrátíme alignment s tokeny
        # pokud máme tokeny, tak granularizujeme, alignujeme granulární tokenizace a mapujeme granulární tokeny na původní tokeny

        src_tokens = req_data.get('src_tokens')
        trg_tokens = req_data.get('trg_tokens')
        src_text = req_data.get('src_text')
        trg_text = req_data.get('trg_text')

        if re.match(r'^[a-z]{2}-[a-z]{2}$', lang_pair) is None:
            # return 400 Bad Request
            return "Invalid language pair format", 400
        langs = lang_pair.split('-')
        if langs[0] not in supported_languages or langs[1] not in supported_languages:
            # return 400 Bad Request
            return "Invalid language pair", 400

        src_tokenizer = tokenizers[langs[0]]
        trg_tokenizer = tokenizers[langs[1]]

        if src_text is not None and trg_text is not None:
            src_tokens = tokenize_text(src_text, src_tokenizer)
            trg_tokens = tokenize_text(trg_text, trg_tokenizer)
            align = compute_alignment(src_tokens, trg_tokens)
        elif src_tokens is not None and trg_tokens is not None:
            src_tokens_granular, src_mapping = granularize_tokenization(src_tokens, src_tokenizer)
            trg_tokens_granular, trg_mapping = granularize_tokenization(trg_tokens, trg_tokenizer)
            align = compute_alignment(src_tokens_granular, trg_tokens_granular)
            align = map_tokenization(align, src_mapping, trg_mapping)
        else:
            # return 400 Bad Request
            return "Supply either src_text and trg_text or src_tokens and trg_tokens", 400

        resp = { 'alignment': align, 'src_tokens': src_tokens, 'trg_tokens': trg_tokens }
        return jsonify(resp)
    return app
