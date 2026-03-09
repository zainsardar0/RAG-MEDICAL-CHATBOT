## Parent image
FROM python:3.13-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

## Installing system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## Copy requirements file first for better caching
COPY requirements-docker.txt .

## Install torch CPU version first separately
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.1.0+cpu

## Install remaining dependencies using docker requirements
RUN pip install --no-cache-dir -r requirements-docker.txt

## Copy rest of application
COPY . .

## Expose only flask port
EXPOSE 5000

## Run the Flask app
CMD ["python", "app/application.py"]