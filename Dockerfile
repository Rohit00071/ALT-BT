# Use light Python image
FROM python:3.11-slim

# Install system dependencies for Manim
# - ffmpeg: required for video rendering
# - build-essential: required for building some python packages
# - libcairo2-dev, libpango1.0-dev, pkg-config, etc.: required for cairo/pango
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    pkg-config \
    libffi-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for output
RUN mkdir -p videos tmp_scenes

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
