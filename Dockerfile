FROM python:3.13.2-slim

# Set the working directory
WORKDIR /app

# Copy code
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set PYTHONPATH to avoid import issues
ENV PYTHONPATH=/app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
