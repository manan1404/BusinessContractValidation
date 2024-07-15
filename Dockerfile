# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV NLTK_DATA /usr/share/nltk_data

# Set working directory in the container
WORKDIR /app

# Copy current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for NLTK data
RUN mkdir -p $NLTK_DATA

# Download NLTK stopwords
RUN python -m nltk.downloader -d $NLTK_DATA stopwords

# Expose port 8501 to the outside world
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "app/streamlit_app.py"]
