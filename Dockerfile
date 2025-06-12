FROM python:3.11

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install FFmpeg and system tools
RUN apt-get update && \
    apt-get install -y ffmpeg curl wget gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy app code
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Gunicorn
EXPOSE 8000

# Start the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
