FROM python:3.11-slim

RUN useradd -ms /bin/bash Bug_Hunter

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bug_bounty_web
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
USER Bug_Hunter

EXPOSE 5505

# WSGI entrypoint
CMD ["gunicorn", "-w 1", "--bind", "127.0.0.1:5505", "wsgi:app"]
