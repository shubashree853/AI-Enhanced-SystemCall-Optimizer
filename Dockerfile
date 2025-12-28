# ============================================================================
# Dockerfile for AI-Enhanced System Call Optimization Django Application
# ============================================================================
# This Dockerfile creates a production-ready container for the Django app.
# It uses a multi-stage build to keep the final image size small.
# ============================================================================

# Base image with Python
# ----------------------------------------------------------------------------
# Using Python 3.11 slim image as base - smaller size, includes only essential
# packages needed to run Python applications
FROM python:3.11-slim

# Set environment variables
# ----------------------------------------------------------------------------
# PYTHONUNBUFFERED: Ensures Python output is sent straight to terminal
# (no buffering) - important for Docker logs
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory inside container
# ----------------------------------------------------------------------------
# All subsequent commands will run in this directory
WORKDIR /app

# Install system dependencies
# ----------------------------------------------------------------------------
# Installing build-essential and other packages needed for:
# - Compiling Python packages (some packages need compilation)
# - Image processing libraries (for Pillow/PIL)
# - Other system utilities
# Note: We keep gcc/g++ for building Python packages, but can remove them
# after pip install to reduce image size (optional optimization)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first
# ----------------------------------------------------------------------------
# This is done separately to leverage Docker layer caching.
# If requirements.txt doesn't change, Docker will reuse the cached layer
# and won't reinstall packages, making builds faster
COPY requirements.txt .

# Install Python dependencies
# ----------------------------------------------------------------------------
# Installing all Python packages listed in requirements.txt
# --no-cache-dir: Don't store cache to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for security
# ----------------------------------------------------------------------------
# Running as root is a security risk. Creating a non-root user
# to run the application
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Copy application code
# ----------------------------------------------------------------------------
# Copy all application files to the container
# Note: .dockerignore will exclude unnecessary files
COPY --chown=appuser:appuser . .

# Switch to non-root user
# ----------------------------------------------------------------------------
USER appuser

# Collect static files
# ----------------------------------------------------------------------------
# Django's collectstatic command gathers all static files from apps
# and places them in STATIC_ROOT for serving by web server
# Using || true to prevent build failure if static files don't exist yet
RUN python manage.py collectstatic --noinput || true

# Expose port
# ----------------------------------------------------------------------------
# Expose port 8000 - this is where Gunicorn will serve the application
# You can change this if needed, but make sure to update the port mapping
# when running the container
EXPOSE 8000

# Health check
# ----------------------------------------------------------------------------
# Docker will periodically check if the container is healthy
# by making a request to the health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/')" || exit 1

# Run migrations and start server
# ----------------------------------------------------------------------------
# This script will:
# 1. Wait for database to be ready (if using external DB)
# 2. Run Django migrations
# 3. Start Gunicorn server
# Using gunicorn for production WSGI server (better than Django's dev server)
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn syscall_optimizer.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 --access-logfile - --error-logfile -"]

