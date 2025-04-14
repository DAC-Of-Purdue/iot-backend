# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./app/requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the FastAPI app runs on
EXPOSE 8000

# Set the command to run the application
CMD ["fastapi", "run",  "app/main.py", "--port", "8000"]