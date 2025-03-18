# Use Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies (if any)
RUN pip install flask requests

# Default command (can be overridden in docker-compose)
CMD ["python", "master.py"]
