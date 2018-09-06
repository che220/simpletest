#!/bin/bash

scriptDir=$(dirname $0)
export FLASK_APP=$scriptDir/main.py
python3 -m flask run --host=0.0.0.0 --port=5001
echo
