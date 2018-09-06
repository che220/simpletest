#!/usr/bin/env bash

echo "{\"image\" : \"ABCEFGDSDSS\"}" | curl -X POST http://127.0.0.1:5001/login -H 'content-type: application/json' -d @-
echo
