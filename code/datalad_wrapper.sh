#!/bin/bash
echo "START $(date)" >> logs/run.log

DL="/home/ephys03/.conda/envs/allensdk/bin/datalad"
PY="/home/ephys03/.conda/envs/allensdk2/bin/python"

"$DL" run -m "Create files by stimulus types" \
  "bash -lc '$PY code/combine_by_stimulus.py'" >> logs/datalad.log 2>&1

echo "END $(date) EXIT:$?" >> logs/run.log