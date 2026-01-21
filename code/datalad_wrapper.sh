#!/bin/bash

set -euo pipefail
trap 'kill 0' EXIT INT TERM

DL="/home/ephys03/.conda/envs/allensdk/bin/datalad"
PY="/home/ephys03/.conda/envs/allensdk3/bin/python"
log_file="logs/run.log"

echo "START $(date)" >> "$log_file"

"$DL" run -m "Combine stimulus types to h5 files" \
  "bash -lc '$PY code/2_combine_by_stimulus.py'" >> logs/datalad.log 2>&1

echo "END $(date) EXIT:$?" >> "$log_file"