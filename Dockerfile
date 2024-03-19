# Use the Python 3.9 image from Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download the spaCy English model
RUN python -m spacy download en_core_web_md
# download TextBlob model
RUN python -m textblob.download_corpora

# Copy project
COPY . /code/