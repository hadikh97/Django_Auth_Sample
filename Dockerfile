# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables to ensure that Python outputs everything to the terminal and prevents buffering
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 8000 available to the world outside this container
EXPOSE 8000
#RUN python manage.py migrate --fake sessions zero \
#    python manage.py migrate --fake-initial
RUN python manage.py makemigrations
RUN python manage.py migrate
# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

