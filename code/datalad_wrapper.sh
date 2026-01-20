#!/bin/bash

set -euo pipefail
trap 'kill 0' EXIT INT TERM

DL="/home/ephys03/.conda/envs/allensdk/bin/datalad"
PY="/home/ephys03/.conda/envs/allensdk-pure/bin/python"
log_file="logs/params_table.log"

echo "START $(date)" >> "$log_file"

"$DL" run -m "Generate presentations.csv properly concatenated between session types" \
  "bash -lc '$PY code/0_access_stim_params.py'" >> logs/datalad.log 2>&1

echo "END $(date) EXIT:$?" >> "$log_file"