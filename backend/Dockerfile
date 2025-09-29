# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]