# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set default environment variables for RabbitMQ and PostgreSQL
ENV RABBITMQ_HOST host.docker.internal
ENV RABBITMQ_PORT 5672
ENV POSTGRES_HOST host.docker.internal
ENV POSTGRES_PORT 5432

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r req.txt

# Copy the env.sh script into the container
COPY env.sh .

# Make the env.sh script executable
RUN chmod +x env.sh

# Copy the rest of the application code into the container
COPY . .

# Install fastapi-template
RUN pip install https://github.com/Myortv/fastapi-plugins.git

# Expose the port your FastAPI app will run on (adjust as needed)
EXPOSE 8000

# Run the env.sh script to load environment variables
CMD ["/bin/bash", "env.sh"]

# Command to start your FastAPI application (adjust as needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-config", "app/core/log.config"]