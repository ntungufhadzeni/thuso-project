# Pull base image
FROM python:3.10.2-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf xvfb

# Copy project
COPY . .

# Set permissions for the /app directory
RUN chmod -R 777 /code

EXPOSE 8000

