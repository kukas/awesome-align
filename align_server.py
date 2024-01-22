import os

from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS

import jsonschema
from jsonschema.validators import Draft202012Validator

import sys
import re
from pprint import pprint

from data.parallel.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner
from map_tokenizations import batch_map_tokenization, batch_granularize_tokenization

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

    if test_config is not None:
        model_name_or_path = "dummy_model"
        aligner = test_config["aligner"]
    else:
        app.logger.info("Loading awesome aligner...")
        model_name_or_path = "finetune/mbert_multilingual_1M-per-lang_only_tlm_add_so_lr5e-6/checkpoint-8600"

        aligner = AwesomeAligner(model_name_or_path=model_name_or_path)
        app.logger.info("Model loaded.")

    BATCH_SIZE = 32

    validator_tokens = Draft202012Validator(
        {
            "type": "object",
            "properties": {
                "src_tokens": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "trg_tokens": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
            "required": ["src_tokens", "trg_tokens"],
        }
    )

    validator_texts = Draft202012Validator(
        {
            "type": "object",
            "properties": {
                "src_text": {"type": "string"},
                "trg_text": {"type": "string"},
            },
            "required": ["src_text", "trg_text"],
        }
    )

    validator_tokens_batch = Draft202012Validator(
        {
            "type": "object",
            "properties": {
                "src_tokens": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string"}},
                    "minItems": 1,
                },
                "trg_tokens": {
                    "type": "array",
                    "items": {"type": "array", "items": {"type": "string"}},
                    "minItems": 1,
                },
            },
            "required": ["src_tokens", "trg_tokens"],
        }
    )

    validator_texts_batch = Draft202012Validator(
        {
            "type": "object",
            "properties": {
                "src_text": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
                "trg_text": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                },
            },
            "required": ["src_text", "trg_text"],
        }
    )

    @app.route("/")
    def index():
        response = Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # info page
    @app.route("/info")
    def info():
        return "Word alignment server (AwesomeAligner, model: {:s})".format(
            model_name_or_path
        )

    def tokenize_texts(texts, tokenizer):
        def tokenize_text(text):
            normalize_spaces = " ".join(text.split())
            return tokenizer(normalize_spaces)

        return [tokenize_text(text) for text in texts]

    def compute_alignment(src_tokens_batch, trg_tokens_batch):
        lines = []
        for src_tokens, trg_tokens in zip(src_tokens_batch, trg_tokens_batch):
            line = "{:s} ||| {:s}".format(" ".join(src_tokens), " ".join(trg_tokens))
            lines.append(line)

        align = aligner.align(lines, batch_size=BATCH_SIZE)
        return align

    def handle_text_batch(src_text, trg_text, src_tokenizer, trg_tokenizer):
        src_tokens = tokenize_texts(src_text, src_tokenizer)
        trg_tokens = tokenize_texts(trg_text, trg_tokenizer)
        alignments = compute_alignment(src_tokens, trg_tokens)
        return alignments, src_tokens, trg_tokens

    def handle_token_batch(src_tokens, trg_tokens, src_tokenizer, trg_tokenizer):
        src_tokens_granular, src_mapping = batch_granularize_tokenization(
            src_tokens, src_tokenizer
        )
        trg_tokens_granular, trg_mapping = batch_granularize_tokenization(
            trg_tokens, trg_tokenizer
        )
        align = compute_alignment(src_tokens_granular, trg_tokens_granular)
        align = batch_map_tokenization(align, src_mapping, trg_mapping)
        return align

    def request_is_text(req_data):
        try:
            validator_texts.validate(req_data)
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False

    def request_is_text_batch(req_data):
        try:
            validator_texts_batch.validate(req_data)
            if len(req_data["src_text"]) != len(req_data["trg_text"]):
                return False
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False

    def request_is_tokens(req_data):
        try:
            validator_tokens.validate(req_data)
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False

    def request_is_tokens_batch(req_data):
        try:
            validator_tokens_batch.validate(req_data)
            if len(req_data["src_tokens"]) != len(req_data["trg_tokens"]):
                return False
            return True
        except jsonschema.exceptions.ValidationError as e:
            return False

    # align cs-uk
    @app.route("/align/<path:lang_pair>", methods=["POST"])
    def align(lang_pair):
        if re.match(r"^[a-z]{2}-[a-z]{2}$", lang_pair) is None:
            # return 400 Bad Request
            return "Invalid language pair format", 400
        langs = lang_pair.split("-")
        if langs[0] not in supported_languages or langs[1] not in supported_languages:
            # return 400 Bad Request
            return "Invalid language pair", 400
        src_tokenizer = tokenizers[langs[0]]
        trg_tokenizer = tokenizers[langs[1]]

        # TODO catch json errors
        req_data = request.get_json()

        # máme buď tokeny nebo text
        # pokud máme text, tak tokenizujeme, alignujeme tyto tokenizace a vrátíme alignment s tokeny
        # pokud máme tokeny, tak granularizujeme, alignujeme granulární tokenizace a mapujeme granulární tokeny na původní tokeny

        if request_is_text(req_data):
            src_text = req_data["src_text"]
            trg_text = req_data["trg_text"]
            alignments, src_tokens, trg_tokens = handle_text_batch(
                [src_text], [trg_text], src_tokenizer, trg_tokenizer
            )
            alignments = alignments[0]
            src_tokens = src_tokens[0]
            trg_tokens = trg_tokens[0]
        elif request_is_tokens(req_data):
            src_tokens = req_data["src_tokens"]
            trg_tokens = req_data["trg_tokens"]
            alignments = handle_token_batch(
                [src_tokens], [trg_tokens], src_tokenizer, trg_tokenizer
            )
            alignments = alignments[0]
        elif request_is_text_batch(req_data):
            src_text = req_data["src_text"]
            trg_text = req_data["trg_text"]
            alignments, src_tokens, trg_tokens = handle_text_batch(
                src_text, trg_text, src_tokenizer, trg_tokenizer
            )
        elif request_is_tokens_batch(req_data):
            src_tokens = req_data["src_tokens"]
            trg_tokens = req_data["trg_tokens"]
            alignments = handle_token_batch(
                src_tokens, trg_tokens, src_tokenizer, trg_tokenizer
            )
        else:
            return "Invalid request format", 400

        resp = {
            "alignment": alignments,
            "src_tokens": src_tokens,
            "trg_tokens": trg_tokens,
        }
        return jsonify(resp)

    return app
