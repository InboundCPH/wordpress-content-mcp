# WordPress MCP Server - Deployment Guide

Guide til deployment af WordPress MCP-serveren i forskellige miljøer.

## Deployment Muligheder

### 1. Lokal Development (Anbefalet til start)

**Fordele:**
- Nem at debugge
- Hurtig iteration
- Ingen hosting omkostninger
- Fuld kontrol

**Setup:**
1. Følg SETUP_GUIDE.md
2. Kør serveren lokalt: `python3 mcp_server.py`
3. Tilføj til Manus som lokal MCP server

**Brug:**
- Perfekt til udvikling og test
- Fungerer kun når din computer kører
- Kan ikke deles med andre

### 2. Railway Deployment (Anbefalet til produktion)

Railway er en moderne cloud platform der gør deployment nemt.

#### Forberedelse

1. **Opret Railway konto**
   - Gå til https://railway.app
   - Sign up med GitHub

2. **Installer Railway CLI** (valgfrit)
   ```bash
   npm install -g @railway/cli
   railway login
   ```

#### Deploy via GitHub

1. **Push til GitHub**
   ```bash
   cd wordpress-content-mcp
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/InboundCPH/wordpress-content-mcp.git
   git push -u origin main
   ```

2. **Opret Railway projekt**
   - Gå til Railway dashboard
   - Klik "New Project"
   - Vælg "Deploy from GitHub repo"
   - Vælg `wordpress-content-mcp` repository

3. **Konfigurer miljøvariabler**
   - Gå til projekt settings
   - Tilføj variabler:
     - `WORDPRESS_URL`
     - `WORDPRESS_USERNAME`
     - `WORDPRESS_APP_PASSWORD`
     - `OPENAI_API_KEY`

4. **Deploy**
   - Railway deployer automatisk
   - Hver push til main branch trigger ny deployment

#### Procfile for Railway

Opret `Procfile` i projektets rod:

```
web: python3 mcp_sse_server.py
```

#### HTTP/SSE Server for Railway

Opret `mcp_sse_server.py` for HTTP deployment:

```python
#!/usr/bin/env python3
"""
WordPress MCP Server - HTTP/SSE transport for Railway deployment
"""

import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import uvicorn

# Import the MCP server
import mcp_server

app = FastAPI(title="WordPress Content Management MCP")

@app.get("/")
async def root():
    return {
        "name": "WordPress Content Management MCP Server",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/sse")
async def sse_endpoint():
    """SSE endpoint for MCP communication."""
    # Implement SSE transport for MCP
    # This allows remote access to MCP tools
    pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### 3. Docker Deployment

#### Dockerfile

Opret `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python3", "mcp_server.py"]
```

#### Docker Compose

Opret `docker-compose.yml`:

```yaml
version: '3.8'

services:
  wordpress-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - WORDPRESS_URL=${WORDPRESS_URL}
      - WORDPRESS_USERNAME=${WORDPRESS_USERNAME}
      - WORDPRESS_APP_PASSWORD=${WORDPRESS_APP_PASSWORD}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

#### Build og Run

```bash
# Build image
docker build -t wordpress-mcp .

# Run container
docker run -p 8000:8000 --env-file .env wordpress-mcp

# Eller med docker-compose
docker-compose up -d
```

### 4. VPS Deployment (DigitalOcean, Linode, etc.)

#### Setup på Ubuntu Server

1. **SSH til server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Installer dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip git
   ```

3. **Clone repository**
   ```bash
   git clone https://github.com/InboundCPH/wordpress-content-mcp.git
   cd wordpress-content-mcp
   ```

4. **Install Python packages**
   ```bash
   pip3 install -r requirements.txt
   ```

5. **Konfigurer .env**
   ```bash
   cp .env.example .env
   nano .env
   # Udfyld credentials
   ```

6. **Opret systemd service**
   
   Opret `/etc/systemd/system/wordpress-mcp.service`:
   
   ```ini
   [Unit]
   Description=WordPress MCP Server
   After=network.target
   
   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/wordpress-content-mcp
   ExecStart=/usr/bin/python3 /home/ubuntu/wordpress-content-mcp/mcp_server.py
   Restart=always
   RestartSec=10
   
   [Install]
   WantedBy=multi-user.target
   ```

7. **Start service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable wordpress-mcp
   sudo systemctl start wordpress-mcp
   sudo systemctl status wordpress-mcp
   ```

## Sikkerhed i Produktion

### 1. Miljøvariabler

**Aldrig:**
- Commit .env til Git
- Hardcode credentials i kode
- Del credentials i plain text

**Altid:**
- Brug miljøvariabler
- Brug secrets management (Railway Secrets, AWS Secrets Manager, etc.)
- Roter credentials regelmæssigt

### 2. HTTPS

**Railway:**
- Automatisk HTTPS
- Gratis SSL certifikater

**VPS:**
- Brug Let's Encrypt
- Konfigurer Nginx som reverse proxy

### 3. Rate Limiting

Implementer rate limiting for at beskytte mod misbrug:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/generate")
@limiter.limit("10/minute")
async def generate_content():
    # ...
```

### 4. Logging

Konfigurer proper logging i produktion:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('wordpress-mcp.log'),
        logging.StreamHandler()
    ]
)
```

## Monitoring

### Health Checks

Implementer health check endpoint:

```python
@app.get("/health")
async def health_check():
    try:
        # Test WordPress connection
        wp_client = WordPressClient()
        wp_client.get_posts(per_page=1)
        
        return {
            "status": "healthy",
            "wordpress": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
```

### Logging og Monitoring

**Railway:**
- Built-in logs viewer
- Metrics dashboard

**VPS:**
- Brug systemd journal: `journalctl -u wordpress-mcp -f`
- Overvej Grafana + Prometheus for metrics

## Backup og Recovery

### 1. Code Backup

- Brug Git for version control
- Push regelmæssigt til GitHub
- Tag releases: `git tag v1.0.0`

### 2. Configuration Backup

- Backup .env fil sikkert (ikke i Git!)
- Dokumenter alle miljøvariabler
- Brug password manager til credentials

### 3. Disaster Recovery Plan

1. **Repository backup**: GitHub
2. **Credentials backup**: Sikker password manager
3. **Deployment documentation**: Denne guide
4. **Recovery time**: < 30 minutter med denne guide

## Opdatering og Vedligeholdelse

### Update Workflow

1. **Test lokalt**
   ```bash
   git pull
   pip3 install -r requirements.txt
   python3 test_mcp_tools.py
   ```

2. **Deploy til staging** (hvis relevant)
   ```bash
   git push origin staging
   ```

3. **Deploy til produktion**
   ```bash
   git push origin main
   ```

### Railway Auto-Deploy

Railway deployer automatisk ved push til main:
- Ingen manuel intervention nødvendig
- Rollback ved fejl
- Zero-downtime deployments

## Performance Optimization

### 1. Caching

Implementer caching for ofte brugte data:

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_categories():
    return wp_client.get_categories()
```

### 2. Connection Pooling

Brug connection pooling for bedre performance:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=20)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 3. Async Operations

Overvej async for bedre concurrency:

```python
import asyncio
import aiohttp

async def generate_multiple_posts(topics):
    tasks = [generate_post(topic) for topic in topics]
    return await asyncio.gather(*tasks)
```

## Troubleshooting Deployment Issues

### Railway Issues

**Problem: Build fails**
- Tjek requirements.txt
- Verificer Python version
- Se build logs

**Problem: Server crashes**
- Tjek environment variables
- Se runtime logs
- Verificer memory limits

### Docker Issues

**Problem: Container exits immediately**
- Tjek Dockerfile CMD
- Verificer .env mounting
- Se container logs: `docker logs <container-id>`

### VPS Issues

**Problem: Service won't start**
- Tjek systemd status: `systemctl status wordpress-mcp`
- Se logs: `journalctl -u wordpress-mcp -n 50`
- Verificer file permissions

---

**God deployment! 🚀**

