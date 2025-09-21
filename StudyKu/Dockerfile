# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent .pyc files & enable stdout logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose port
EXPOSE 8000

# Run Gunicorn for production
CMD ["gunicorn", "StudyKu.wsgi:application", "--bind", "0.0.0.0:8000"]
