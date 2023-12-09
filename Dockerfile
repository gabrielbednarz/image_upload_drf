FROM python:3.10-slim-buster

# Set environment variables to ensure Python output is sent straight to terminal (unbuffered)
# and that Python won’t try to write .pyc files on the import of source modules.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

# Update system packages, install system-level dependencies, including libmagic1,
# and install Python dependencies.
# Additionally, clean up the package list to reduce the image size.
RUN apt-get update && apt-get install -y build-essential libpq-dev libmagic1 \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*