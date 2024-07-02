#!/bin/bash

echo "Bot container started."
git pull
pip install --quiet -r requirements.txt
uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000} & python3 -m bot
