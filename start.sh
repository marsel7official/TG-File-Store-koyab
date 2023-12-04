#!/bin/bash

# Output for debugging purposes
echo "Bot container started."

# Pull the latest code from the Git repository
git pull -f -q

# Install Python dependencies from requirements.txt
pip install --quiet -r requirements.txt

# Function to restart the bot
restart_bot() {
    echo "Restarting the bot..."
    # Add your command to start the bot here, e.g., "python3 -m bot"
    uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000} & python3 -m bot
}

# Define the restart time (e.g., midnight)
restart_time="0 0 * * *"

# Schedule the restart using cron
echo "Scheduling a daily restart at midnight..."
(crontab -l 2>/dev/null; echo "$restart_time /bin/bash /app/start.sh >> /app/cron.log 2>&1") | crontab -

# Start your bot
restart_bot
