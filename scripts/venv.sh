#!/bin/bash
set -e

virtualenv -p python3  .env
. .env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
