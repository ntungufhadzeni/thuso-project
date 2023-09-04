# Pull base image
FROM python:3.11.4-slim-buster

# Set environment variables
ENV APP_HOME=/home/app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/media/cover_letters

# Set work directory
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf nano

# Copy project
COPY . .


EXPOSE 8000
