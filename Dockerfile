# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Cloudinary CLI support (optional, if using cloudinary CLI)
# RUN pip install cloudinary-cli

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .


# Collect static files (recommended for prod)
# RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8001

# Start Gunicorn
# CMD ["gunicorn", "apex.wsgi:application", "--bind", "0.0.0.0:8001"]
# CMD ["gunicorn", "apex.wsgi:application", "--bind", "0.0.0.0:8001", "--timeout", "120"]
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn apex.wsgi:application --bind 0.0.0.0:8001 --timeout 120"]

