# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set NLTK data path explicitly
RUN python -c "import nltk; nltk.download('stopwords', download_dir='/usr/share/nltk_data')"

# Expose port 8501 to the outside world
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "app/streamlit_app.py"]
