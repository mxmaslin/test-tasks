# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /tests_django

# Copy project
COPY ./tests_django /tests_django/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN pip install -r requirements.txt
