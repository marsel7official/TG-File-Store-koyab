# Use an official Python 3.8 image as your base im
# Use an official Python 3.10 image as a base image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Define environment variable for port
ENV PORT=8080

# Command to run the application
CMD echo "Bot container started." && \
    git pull && \
    pip install --quiet -r requirements.txt && \
    uvicorn api:app --host=0.0.0.0 --port=${PORT:-8000} & \
    python3 -m bot
