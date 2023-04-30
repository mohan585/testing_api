# Start from Python 3.8 base image
FROM python:3.8-slim-buster

# Install any necessary dependencies
RUN apt-get update && apt-get install -y openjdk-11-jre-headless && apt-get clean

# Install Waitress
RUN pip install waitress

# Set the working directory
WORKDIR /app

# Expose the port number on which the app will run
EXPOSE 8080

# Copy the requirements file and install the necessary packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files into the container
COPY . .

# Start the app using Waitress
CMD ["waitress-serve", "--port=8080", "main:app"]
