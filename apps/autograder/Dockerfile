FROM python:3.12-slim

# Install git (needed for installing from GitHub)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*
# Pip install necessary packages
RUN python -m pip install --upgrade pip setuptools wheel

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Build-time argument for sIArena reference (branch, tag, or commit)
ARG SIARENA_REF=main

WORKDIR /opt/autograder

RUN pip install "git+https://github.com/jparisu/sIArena.git@${SIARENA_REF}"

# Copy your script into the container
COPY apps/autograder/autograder.py /opt/autograder/autograder.py

# Set working directory
WORKDIR /work

# Default command: run your script
ENTRYPOINT ["python", "/opt/autograder/autograder.py"]
