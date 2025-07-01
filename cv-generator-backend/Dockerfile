FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger')"

# Copy application code
COPY . .

# Create directory for temporary files
RUN mkdir -p /tmp

# Expose port
EXPOSE 5002

# Run application
CMD ["python", "app.py"]
