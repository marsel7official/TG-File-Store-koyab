# Use an official Python 3.8 image as your base image
FROM python:3.11.6

# Install system dependencies and clean up
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Clone your bot repository into /app
RUN git clone https://github.com/Rajbhaiya/TG-File-Store /app

# Set the working directory to /app
WORKDIR /app

# Install Python dependencies from requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy your start.sh script into the container
COPY start.sh /app/start.sh

# Make start.sh executable
RUN chmod +x /app/start.sh

# Install cron
RUN apt-get update -y && apt-get install -y cron

# Add a cron job that runs your script every 24 hours (adjust the timing as needed)
RUN (echo "0 0 * * * /app/start.sh" && crontab -l) | crontab

# Start cron in the foreground to trigger the cron jobs
CMD ["cron", "-f"]
