#!/bin/bash
gunicorn --log-syslog -b :19080 -w 1 "align_server:create_app_csuk()"