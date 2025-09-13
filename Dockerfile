# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash debug-user && \
    chown -R debug-user:debug-user /app
USER debug-user

# Set the entrypoint
ENTRYPOINT ["debug"]

# Default command
CMD ["--help"]