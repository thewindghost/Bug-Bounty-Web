FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    software-properties-common \
    curl \
    wget \
    git \
    sudo \
    build-essential \
    gcc \
    g++ \
    make \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    && ln -sf python3.11 /usr/bin/python3 \
    && ln -sf pip3 /usr/bin/pip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash Bug_Hunter && \
    echo "Bug_Hunter ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /bug_bounty_web

COPY . .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

USER Bug_Hunter

EXPOSE 5505

CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:5505", "wsgi:app"]
