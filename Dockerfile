# Use Python as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV TZ=Europe/London

# Create directory for storing images
RUN mkdir -p /app/images

# Set permissions for camera access
RUN chmod 777 /app/images

# Copy telegram config
COPY telegram-send.conf /root/.config/telegram-send.conf

# Command to run the application
CMD ["python", "security_camera.py"] 