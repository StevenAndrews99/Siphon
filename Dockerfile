# Use a fuller Python base image with apt support
FROM python:3.11

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install FFmpeg and other system deps
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libpq-dev && \
    apt-get clean

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for gunicorn
EXPOSE 8000

# Start the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
