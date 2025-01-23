# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ARG REQUIREMENTS_FILE
# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Set the working directory
RUN mkdir /app
WORKDIR /app

COPY ${REQUIREMENTS_FILE} /app/requirements.txt
# Install pip-tools globally
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
