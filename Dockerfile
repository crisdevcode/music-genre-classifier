# Build stage
FROM python:3.13.7-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/ src/

# Copy the local artifacts folder into the image
COPY artifacts/ artifacts/

# Expose port
EXPOSE 8000

# Command to run the app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]