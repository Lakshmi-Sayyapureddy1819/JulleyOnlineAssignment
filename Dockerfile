# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# 1. Generate the raw/processed data (Does not require API Key)
RUN python scripts/data_generation.py

# 2. Pre-initialize the Vector Database during build
# Note: You must provide OPENAI_API_KEY as a build argument for this to work
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
RUN python scripts/database_setup.py

# Expose ports
EXPOSE 8000
EXPOSE 8501