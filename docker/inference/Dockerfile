# Base image
FROM python:3.11-slim

# Setup working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY docker/inference/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copy the inference server script to the working directory
COPY docker/inference/server.py ./server.py

# Declare volume mount points
VOLUME ["/app/models", "/app/logs"]

# Expose the Flask server port
EXPOSE 8081

# Set the command to run the inference server
CMD ["python", "server.py"]
