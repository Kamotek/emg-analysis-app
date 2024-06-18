#!/bin/bash
VENV_PATH=$(pipenv --venv)
sudo pipenv run $VENV_PATH/bin/python -m $1
