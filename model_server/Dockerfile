# Use an official Python runtime as a parent image
FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
# Set the working directory in the container

RUN mkdir app
WORKDIR /app

# Copy requirements file to the working directory
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
