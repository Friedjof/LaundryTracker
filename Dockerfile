# Use the official Python image from Docker Hub
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container
COPY . .

# Create a directory for the SQLite database
RUN mkdir -p /data
VOLUME ["/data"]

# Set environment variable for database path
ENV SQLITE_PATH=/data/db.sqlite3

# Setup cron job
COPY cron/update /etc/cron.d/update
RUN chmod 0644 /etc/cron.d/update
# Apply cron job
RUN crontab /etc/cron.d/update
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Make the start.sh script executable
RUN chmod +x /app/start.sh

# Expose the port used by the application
EXPOSE 8000

# Start the application using the start.sh script
CMD ["/app/start.sh"]