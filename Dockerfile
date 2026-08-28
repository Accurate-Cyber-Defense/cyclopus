# CYCLOPUS - Docker Image (Alpine Linux)
FROM alpine:3.19

# Metadata
LABEL maintainer="Ian Carter Kulani <iancarterkulani@gmail.com>"
LABEL version="1.0.0"
LABEL description="CYCLOPUS - Cybersecurity Command & Control Platform"

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-cryptography \
    py3-paramiko \
    py3-requests \
    py3-psutil \
    py3-colorama \
    py3-ipython \
    py3-flask \
    py3-pillow \
    py3-numpy \
    py3-matplotlib \
    bash \
    curl \
    wget \
    nmap \
    openssh-client \
    netcat-openbsd \
    bind-tools \
    traceroute \
    whois \
    nikto \
    hashcat \
    git \
    make \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pynput \
    py3-selenium \
    py3-qrcode \
    docker \
    sudo

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt && \
    pip3 install --no-cache-dir flask-socketio python-socketio eventlet flask-cors

# Copy application files
COPY cyclopus.py .
COPY commands-test.py .
COPY requirements-check.py .
COPY setup.py .
COPY README.md .
COPY LICENSE .
COPY .env.example .env

# Create necessary directories
RUN mkdir -p .cyclopus .cyclopus/payloads .cyclopus/workspaces .cyclopus/reports \
    .cyclopus/phishing_pages .cyclopus/captured_credentials .cyclopus/ssh_keys \
    .cyclopus/traffic_logs .cyclopus/nikto_results cyclopus_reports \
    .cyclopus/keylog_exfil .cyclopus/deployments .cyclopus/cracking \
    .cyclopus/arp_logs .cyclopus/mac_logs .cyclopus/nat_logs \
    .cyclopus/docker_scans .cyclopus/email_composer .cyclopus/pdf_reports

# Create entrypoint script
RUN echo '#!/bin/sh\n\
echo "🐙 Starting CYCLOPUS..."\n\
echo "Version: 1.0.0"\n\
echo "Author: Ian Carter Kulani, MSc"\n\
echo "========================================="\n\
python3 cyclopus.py "$@"' > /usr/local/bin/cyclopus-entrypoint && \
    chmod +x /usr/local/bin/cyclopus-entrypoint

# Make the script executable
RUN chmod +x /app/cyclopus.py /app/requirements-check.py /app/commands-test.py

# Expose ports
EXPOSE 5000 8080 22

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CYCLOPUS_CONFIG_DIR=/app/.cyclopus
ENV CYCLOPUS_REPORT_DIR=/app/cyclopus_reports

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import socket; socket.socket().connect(('localhost', 5000))" || exit 1

# Entrypoint
ENTRYPOINT ["cyclopus-entrypoint"]
CMD ["--help"]