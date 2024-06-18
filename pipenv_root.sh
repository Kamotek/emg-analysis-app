#!/bin/bash
VENV_PATH=$(pipenv --venv)
module_name=$1
sudo "$VENV_PATH"/bin/python -m "$module_name"

# Example usage
# pipenv_root.sh test.main

# (running ./test/main.py)