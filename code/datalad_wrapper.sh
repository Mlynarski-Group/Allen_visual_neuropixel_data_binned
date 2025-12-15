#!/bin/bash
echo "START $(date)" >> logs/run.log
datalad run -m "Create sessions-presentations" "python code/access_allen_data.py" >> logs/run.log 2>&1
echo "END $(date) EXIT:$?" >> logs/run.log