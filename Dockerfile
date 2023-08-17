# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Add a new user
RUN useradd -ms /bin/bash app

# Change ownership of the work directory to the new user
RUN chown -R app:app /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Copy project
COPY . .

# Switch to the new user
USER app
