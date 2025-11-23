# Minimal image to run SwarmAI-Lab simulations
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# System utilities for scientific packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

# Copy source last to maximize cache hits
COPY src ./src
COPY tests ./tests
COPY docs ./docs
COPY experiments ./experiments
COPY notebooks ./notebooks

CMD ["python"]
