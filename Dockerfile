# Use official Python image
FROM python:3.10.12

# Install PostgreSQL client
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and set work directory
RUN mkdir /var/app
WORKDIR /var/app

# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Copy dependencies and install them
COPY requirements.txt /var/app/
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy application files
COPY . /var/app/

# Ensure that the run script is executable (optional if already set on local system)
RUN chmod +x run_django_app.sh

# Default command to run the app (can be overridden by docker-compose)
CMD ["bash", "run_django_app.sh"]
