# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /old_django_test_tasks

# Copy project
COPY ../old_django_test_tasks /old_django_test_tasks/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install virtualenv
RUN pip install -r requirements.txt
