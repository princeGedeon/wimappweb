FROM python:3.10

# Image name & Author
LABEL image_name="friare_webinaire"
LABEL maintainer="princeGedeon - princeyisegnon@gmail.com"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the Docker image
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /var/run/mysqld

# Copy the Django project files to the image
COPY . /app/

# Expose the port that Django runs on
EXPOSE 8081
