#!/bin/bash

# Output for debugging purposes
echo "Bot container started."

# Pull the latest code from the Git repository
git pull -f -q

# Install Python dependencies from requirements.txt
pip install --quiet -r requirements.txt

# Start your bot using uvicorn and python3
uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000} & python3 -m bot
