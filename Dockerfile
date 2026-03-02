# Base image with Python
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Upgrade pip first, then install libraries
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the download script
COPY download_models.py .

# Build argument for Hugging Face Token
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Download models DURING the build process
RUN python download_models.py

# Now copy the rest of your app (main.py, json file, etc.)
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]