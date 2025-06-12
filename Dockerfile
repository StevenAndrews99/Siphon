# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (includes ffmpeg)
RUN apt-get update &&     apt-get install -y ffmpeg gcc libpq-dev &&     apt-get clean

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]