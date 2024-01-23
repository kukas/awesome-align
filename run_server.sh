#!/bin/bash
set -euo pipefail

# activate the virtual environment
source /home/balhar/miniconda3/bin/activate aligner

# run the server (listen on localhost, the service will be reverse proxied using Nginx)
gunicorn -b 127.0.0.1:19080 -w 1 "align_server:create_aligner()"
