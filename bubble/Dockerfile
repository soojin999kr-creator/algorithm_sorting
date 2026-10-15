Use lightweight official Python image for production

FROM python:3.11-slim AS base

Set working directory inside container

WORKDIR /app

Prevent Python from writing pyc files and buffering stdout/stderr

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

Install system dependencies if required

RUN apt-get update && apt-get install -y --no-install-recommends 

build-essential 

&& rm -rf /var/lib/apt/lists/*

Copy dependency specifications and install

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

Copy application source code

COPY . .

Create a non-privileged user for security best practices

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

Expose port for Cloud Run

ENV PORT=8080
EXPOSE 8080

Run production WSGI server Gunicorn with optimized worker settings

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "0", "main:app"]
