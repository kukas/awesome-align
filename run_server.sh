#!/bin/bash
set -euo pipefail

# activate the virtual environment
source /home/balhar/miniconda3/bin/activate aligner_csuk

# run the server
gunicorn --log-syslog -b :19080 -w 1 "align_server:create_aligner()"
