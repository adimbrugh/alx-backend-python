# Use Python 3.10 as base image
FROM python:3.10

# Set environment variables (use key=value format)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for building packages like Twisted
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy the project code into the container
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Start Django server (you can update the command if using manage.py runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
