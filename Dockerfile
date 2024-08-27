# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt

EXPOSE 8080

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Specify the command to run the app
CMD ["python", "app.py"]