#!/bin/bash
# For MISP server 

# ========================= Set up part ========================
# -1. Install python virtual environment 
sudo apt install python3.11-venv -y


DIRECTORY=".venv"

# 0. Check if folder .venv exist or not, if not do step 1, mkdir if .env not exist 
if [ ! -d "$DIRECTORY" ]; then
  echo "$DIRECTORY does not exist. creating directory \'.venv\'"
  mkdir ".venv"
else
  echo "$DIRECTORY already exist, skipping directory creation step"
fi

# 1. Set a temporary foler to store the environment 
python -m venv .venv # Then a folder .venv will be created which will store the python executable

# 2. Install libraries 
sudo ./.venv/bin/pip3 install -r requirements.txt 

# ============================ Run part =============================

# 3. Run main.py using the virtual environment python, main.py must be ran by that 
sudo ./.venv/bin/python3 main.py
