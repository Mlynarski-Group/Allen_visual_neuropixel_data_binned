#!/bin/bash

set -euo pipefail
trap 'kill 0' EXIT INT TERM

DL="/home/ephys03/.conda/envs/allensdk/bin/datalad"
PY="/home/ephys03/.conda/envs/allensdk-pure/bin/python"
log_file="logs/run.log"

echo "START $(date)" >> "$log_file"

"$DL" run -m "Create sessions-presentations (rerun 383115be)" \
  "bash -lc '$PY code/1_access_allen_data.py'" >> logs/datalad.log 2>&1

echo "END $(date) EXIT:$?" >> "$log_file"