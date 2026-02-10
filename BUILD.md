# Build and Deployment Guide

This document provides comprehensive instructions for building and deploying the WebSSH project.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Building the Application](#building-the-application)
- [Running Tests](#running-tests)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)

## Prerequisites

### System Requirements
- **Python**: 3.11+ (tested with 3.11 and 3.12)
- **pip**: Latest version
- **Docker** (optional): For containerized deployment
- **Git**: For version control

### Recommended Tools
- **virtualenv** or **venv**: For Python virtual environments
- **Docker Compose**: For easy container orchestration

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/bifrost0x/webssh.git
cd webssh
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (optional, for testing and linting)
pip install -r requirements-dev.txt
```

### 4. Set Environment Variables

```bash
# Generate a secure secret key
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Set CORS origins
export CORS_ORIGINS="http://localhost:5000"

# Enable debug mode (development only)
export DEBUG=True

# Optional: Set custom port
export PORT=5000
```

### 5. Run the Application

```bash
python start.py
```

The application will be available at `http://localhost:5000`

## Building the Application

### Local Build

The application doesn't require a build step for local development. Simply install dependencies and run:

```bash
pip install -r requirements.txt
python start.py
```

### Production Build Checklist

Before deploying to production:

1. ✅ **Set SECRET_KEY**: Generate a secure, unique secret key
2. ✅ **Configure CORS**: Set specific allowed origins
3. ✅ **Disable DEBUG**: Set `DEBUG=False` or omit it
4. ✅ **Use HTTPS**: Terminate TLS at reverse proxy
5. ✅ **Set Trusted Proxies**: If behind a reverse proxy, set `TRUSTED_PROXIES=1`
6. ✅ **Configure Data Directory**: Set `DATA_DIR` for persistent storage

## Running Tests

### Quick Test Run

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

### Continuous Integration

Tests are automatically run on:
- Pull requests to main branch
- Pushes to main branch

See `.github/workflows/` for CI configuration.

## Docker Deployment

### Build Docker Image

```bash
# Build the image
docker build -t webssh:latest .

# Or build with specific tag
docker build -t webssh:v1.0.0 .
```

### Run with Docker

```bash
# Generate secret key
export SECRET_KEY=$(openssl rand -hex 32)

# Run container
docker run -d \
  --name webssh \
  -p 5000:5000 \
  -e SECRET_KEY=$SECRET_KEY \
  -e CORS_ORIGINS=http://localhost:5000 \
  -v webssh_data:/app/data \
  --restart unless-stopped \
  webssh:latest
```

### Docker Compose Deployment

1. Download or create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  webssh:
    image: ghcr.io/bifrost0x/webssh:latest
    container_name: webssh
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=<YOUR-SECRET-KEY>
      - CORS_ORIGINS=http://localhost:5000
      - TRUSTED_PROXIES=0
    volumes:
      - webssh_data:/app/data
    restart: unless-stopped

volumes:
  webssh_data:
```

2. Generate and insert secret key:

```bash
SECRET=$(openssl rand -hex 32)
sed -i "s/<YOUR-SECRET-KEY>/$SECRET/" docker-compose.yml
```

3. Start the service:

```bash
docker compose up -d
```

### Docker Health Check

The Docker image includes a health check that verifies the application is responding:

```bash
# Check container health
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' webssh
```

## Production Deployment

### Environment Variables

Required variables for production:

```bash
# REQUIRED
export SECRET_KEY="<64-character-hex-string>"
export CORS_ORIGINS="https://ssh.example.com"

# RECOMMENDED
export TRUSTED_PROXIES=1              # If behind reverse proxy
export DATA_DIR=/app/data             # Persistent storage location

# OPTIONAL
export PORT=5000                      # Application port
export HOST=0.0.0.0                   # Bind address
export SESSION_TIMEOUT=1800           # Session timeout in seconds
export REGISTRATION_ENABLED=True      # Allow new registrations
export RATELIMIT_ENABLED=True         # Enable rate limiting
```

### Using Gunicorn (Production Server)

```bash
# Install gunicorn (already in requirements.txt)
pip install gunicorn eventlet

# Run with gunicorn
gunicorn --worker-class eventlet \
  -w 1 \
  --bind 0.0.0.0:5000 \
  start:app
```

### Reverse Proxy Setup

#### Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name ssh.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://webssh:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Traefik (Docker Labels)

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.webssh.rule=Host(`ssh.example.com`)"
  - "traefik.http.routers.webssh.entrypoints=websecure"
  - "traefik.http.routers.webssh.tls.certresolver=letsencrypt"
  - "traefik.http.services.webssh.loadbalancer.server.port=5000"
```

#### Caddy

```caddyfile
ssh.example.com {
    reverse_proxy webssh:5000
}
```

### Systemd Service (Linux)

Create `/etc/systemd/system/webssh.service`:

```ini
[Unit]
Description=WebSSH Terminal
After=network.target

[Service]
Type=simple
User=webssh
WorkingDirectory=/opt/webssh
Environment="SECRET_KEY=<your-secret-key>"
Environment="CORS_ORIGINS=https://ssh.example.com"
Environment="TRUSTED_PROXIES=1"
ExecStart=/opt/webssh/venv/bin/gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 start:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable webssh
sudo systemctl start webssh
sudo systemctl status webssh
```

## Troubleshooting

### Build Issues

**Problem**: Dependency installation fails

```bash
# Solution 1: Update pip
pip install --upgrade pip

# Solution 2: Install with no cache
pip install --no-cache-dir -r requirements.txt

# Solution 3: Use specific Python version
python3.11 -m pip install -r requirements.txt
```

**Problem**: Permission errors with data directory

```bash
# Solution: Create and set permissions
mkdir -p data/keys data/logs
chmod 700 data data/keys data/logs
```

### Runtime Issues

**Problem**: Application won't start - SECRET_KEY error

```bash
# Solution: Set SECRET_KEY environment variable
export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
```

**Problem**: CORS errors in browser

```bash
# Solution: Set correct CORS_ORIGINS
export CORS_ORIGINS="https://your-domain.com"
# Or for homelab use:
export CORS_ORIGINS="*"
export ALLOW_CORS_WILDCARD=true
```

**Problem**: WebSocket connection fails

```bash
# Solution: Ensure reverse proxy is configured for WebSocket upgrade
# Check nginx/caddy/traefik configuration includes WebSocket support
```

### Docker Issues

**Problem**: Container exits immediately

```bash
# Check logs
docker logs webssh

# Common cause: Missing SECRET_KEY
# Solution: Pass SECRET_KEY environment variable
docker run -e SECRET_KEY=$(openssl rand -hex 32) ...
```

**Problem**: Data not persisting

```bash
# Solution: Use volume mount
docker run -v webssh_data:/app/data ...
```

## Performance Optimization

### Production Recommendations

1. **Use a CDN**: Serve static assets from a CDN
2. **Enable HTTP/2**: Configure reverse proxy for HTTP/2
3. **Use connection pooling**: Already configured in the app
4. **Monitor resources**: Use tools like htop, docker stats
5. **Set appropriate timeouts**: Adjust SESSION_TIMEOUT based on usage

### Scaling

For high traffic:
- Deploy behind a load balancer
- Use Redis for session storage (requires code modification)
- Implement database connection pooling
- Use multiple application instances

## Security Checklist

- ✅ Set strong SECRET_KEY (64+ characters)
- ✅ Use HTTPS in production
- ✅ Set specific CORS_ORIGINS (not wildcard)
- ✅ Enable rate limiting (default: enabled)
- ✅ Use reverse proxy with security headers
- ✅ Keep dependencies updated
- ✅ Restrict file permissions on data directory (700)
- ✅ Use non-root user in Docker
- ✅ Enable firewall rules
- ✅ Monitor logs for suspicious activity

## Maintenance

### Update Dependencies

```bash
# Check for updates
pip list --outdated

# Update all dependencies
pip install --upgrade -r requirements.txt

# Run tests after updates
pytest tests/
```

### Backup Data

```bash
# Backup data directory
tar -czf webssh-backup-$(date +%Y%m%d).tar.gz data/

# For Docker volumes
docker run --rm \
  -v webssh_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/webssh-backup.tar.gz -C /data .
```

### Monitor Logs

```bash
# View application logs (if using systemd)
journalctl -u webssh -f

# View Docker logs
docker logs -f webssh

# Application stores logs in data/logs/ directory
tail -f data/logs/app.log
```

## Build Status

✅ **Dependencies**: All dependencies install successfully  
✅ **Application**: Starts without errors  
✅ **Tests**: 25/25 tests passing  
✅ **Docker**: Image builds successfully  
✅ **Security**: No known vulnerabilities in dependencies  

Last updated: 2026-02-10
