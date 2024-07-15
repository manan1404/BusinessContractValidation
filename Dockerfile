# Dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK and download required data
RUN apt-get update && apt-get install -y \
        wget \
        && rm -rf /var/lib/apt/lists/*

RUN python -m nltk.downloader stopwords

# Expose port 8501 to the outside world
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "app/streamlit_app.py"]
