FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# WSGI entrypoint
CMD ["gunicorn", "-w 1", "--bind", "0.0.0.0:5505", "wsgi:app"]
