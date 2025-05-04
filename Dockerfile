# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and related files directly into /app
# This copies the *contents* of src/reddit_mind into /app
COPY src/reddit_mind/ .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py (now located at /app/app.py) when the container launches
# The JSON files will also be expected in /app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 