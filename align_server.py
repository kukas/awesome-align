import os
  
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask_cors import CORS

import sys
from pprint import pprint

from data.tokenize import get_tokenizer
from awesome_aligner import AwesomeAligner

# align_models_path = os.path.join(fast_align_dir, 'models')

# def create_aligner(model_type):
#     aligner_params = [ os.path.join(align_models_path, model_type + f) for f in [
#         '.fwd.params',
#         '.fwd.err',
#         '.rev.params',
#         '.rev.err'
#     ]]
#     return Aligner(*aligner_params)

def create_app_csuk(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.json.mimetype = "application/json; charset=utf-8"
    CORS(app)

    cs_tokenizer = get_tokenizer('cs')
    uk_tokenizer = get_tokenizer('uk')

    app.logger.info("Loading awesome aligner...")
    csuk_aligner = AwesomeAligner(model_name_or_path="bert-base-multilingual-cased")
    app.logger.info("Model loaded.")

    @app.route("/")
    def index():
        response = flask.Response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    # info page
    @app.route('/info')
    def info():
        return 'Word alignment server (FastAlign, model: {:s})'.format(align_model_type)
    
    # align cs-uk
    @app.route('/align/cs-uk', methods=['POST'])
    def align_csuk():
        req_data = request.get_json()

        src_tokens = req_data.get('src_tokens')
        trg_tokens = req_data.get('trg_tokens')
        if src_tokens is None:
            src_tokens = cs_tokenizer(" ".join(req_data['src_text'].split()))
        if trg_tokens is None:
            trg_tokens = uk_tokenizer(" ".join(req_data['trg_text'].split()))

        align = ''
        if len(src_tokens) > 0 and len(trg_tokens) > 0:
            line = "{:s} ||| {:s}".format(" ".join(src_tokens), " ".join(trg_tokens))
            align = csuk_aligner.align(line)
        
        resp = { 'alignment': align, 'src_tokens': src_tokens, 'trg_tokens': trg_tokens }
        return jsonify(resp)

    return app
