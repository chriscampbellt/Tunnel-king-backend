# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

# Set the working directory
WORKDIR /app

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && apt-get clean

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s ~/.local/bin/poetry /usr/local/bin/poetry

# Copy project dependency files to the working directory
COPY pyproject.toml /app/

# Check if poetry.lock exists before copying
COPY poetry.lock /app/

# Install dependencies using Poetry, including dev dependencies
RUN poetry lock && poetry install --with dev --no-interaction --no-ansi --no-root
