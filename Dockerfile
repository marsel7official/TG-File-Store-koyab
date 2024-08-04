# Use an official Python 3.8 image as your base image
FROM python:3.11.6

# Install system dependencies and clean up
RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends git cron && \
    rm -rf /var/lib/apt/lists/*

# Clone your bot repository into /app
RUN git clone https://github.com/Rajbhaiya/TG-File-Store /app

# Set the working directory to /app
WORKDIR /app

# Install Python dependencies from requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD ["bash", "start.sh"]
