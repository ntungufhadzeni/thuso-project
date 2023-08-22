# Pull base image
FROM python:3.11.4-slim-buster

# Set environment variables
ENV APP_HOME=/home/app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/media

# Set work directory
WORKDIR $APP_HOME

# create the app user
RUN addgroup --system app && adduser --system --group app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Copy project
COPY . .

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change permissions
Run chmod -R 755 $APP_HOME/media

# change to the app user
USER app

EXPOSE 8000
