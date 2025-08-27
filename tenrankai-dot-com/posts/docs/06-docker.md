+++
title = "Docker Guide"
summary = "Deploy Tenrankai using Docker and Docker Compose"
date = "2025-08-26"
+++

# Docker Guide

Tenrankai provides official Docker images for easy deployment. This guide covers running Tenrankai with Docker and Docker Compose.

## Docker Image Features

The official Tenrankai Docker image includes:

- Multi-stage build for optimized size (~168 MB)
- Full AVIF support with HDR and gain maps
- WebP and JPEG fallback support
- Security hardening with non-root user (UID 1001)
- All required dependencies pre-installed

## Quick Start with Docker

### 1. Basic Docker Run

```bash
docker run -d \
  --name tenrankai \
  -p 3000:3000 \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v $(pwd)/photos:/photos:ro \
  -v tenrankai-cache:/cache \
  theatrus/tenrankai:latest
```

### 2. With Authentication

If using authentication, mount the users database:

```bash
docker run -d \
  --name tenrankai \
  -p 3000:3000 \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v $(pwd)/photos:/photos:ro \
  -v $(pwd)/users.toml:/users.toml:ro \
  -v tenrankai-cache:/cache \
  theatrus/tenrankai:latest
```

## Docker Compose Setup

### 1. Basic Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  tenrankai:
    image: theatrus/tenrankai:latest
    container_name: tenrankai
    ports:
      - "3000:3000"
    volumes:
      - ./config.toml:/config.toml:ro
      - ./photos:/photos:ro
      - cache_data:/cache
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp

volumes:
  cache_data:
```

### 2. Production Configuration

For production deployments with reverse proxy:

```yaml
version: '3.8'

services:
  tenrankai:
    image: theatrus/tenrankai:latest
    container_name: tenrankai
    volumes:
      - ./config.toml:/config.toml:ro
      - /path/to/photos:/photos:ro
      - ./users.toml:/users.toml:ro
      - cache_data:/cache
      - ./static:/static:ro
      - ./templates:/templates:ro
    restart: always
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - internal
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.tenrankai.rule=Host(`gallery.example.com`)"
      - "traefik.http.routers.tenrankai.tls=true"
      - "traefik.http.routers.tenrankai.tls.certresolver=letsencrypt"

  nginx:
    image: nginx:alpine
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    networks:
      - internal
      - external
    restart: always

networks:
  internal:
  external:

volumes:
  cache_data:
```

## Volume Mapping

### Required Volumes

| Container Path | Purpose | Access Mode |
|---------------|---------|-------------|
| `/config.toml` | Main configuration file | Read-only |
| `/photos` | Photo source directory | Read-only |
| `/cache` | Image cache directory | Read-write |

### Optional Volumes

| Container Path | Purpose | Access Mode |
|---------------|---------|-------------|
| `/users.toml` | User authentication database | Read-only |
| `/static` | Custom static assets | Read-only |
| `/templates` | Custom templates | Read-only |

## Configuration for Docker

### 1. Basic config.toml

```toml
[server]
host = "0.0.0.0"  # Listen on all interfaces in container
port = 3000

[app]
name = "My Gallery"
cookie_secret = "change-me-to-long-random-string"

[templates]
directory = "/templates"

[static_files]
directories = "/static"

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "/photos"
cache_directory = "/cache"
copyright_holder = "Your Name"
```

### 2. Environment Variable Overrides

You can override configuration using environment variables:

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    environment:
      - TENRANKAI_SERVER__HOST=0.0.0.0
      - TENRANKAI_SERVER__PORT=8080
      - TENRANKAI_APP__NAME=My Gallery
      - TENRANKAI_APP__COOKIE_SECRET=your-secret-here
```

Environment variable format:
- Prefix: `TENRANKAI_`
- Section separator: `__` (double underscore)
- Example: `TENRANKAI_SERVER__PORT=8080` sets `server.port = 8080`

## Building Custom Docker Image

### 1. Custom Dockerfile

Create a custom Dockerfile for modifications:

```dockerfile
FROM theatrus/tenrankai:latest

# Switch to root for customization
USER root

# Add custom fonts or assets
COPY custom-fonts/*.ttf /static/

# Install additional tools if needed
RUN apk add --no-cache imagemagick

# Switch back to tenrankai user
USER tenrankai
```

### 2. Build and Run

```bash
# Build custom image
docker build -t my-tenrankai .

# Run with custom image
docker run -d \
  --name my-tenrankai \
  -p 3000:3000 \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v $(pwd)/photos:/photos:ro \
  my-tenrankai
```

## Docker Security Best Practices

### 1. Read-Only Root Filesystem

The container runs with a read-only root filesystem by default:

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    read_only: true
    tmpfs:
      - /tmp  # Writable temp directory
```

### 2. Non-Root User

The container runs as user `tenrankai` (UID 1001):

```bash
# Ensure photo directory is readable by UID 1001
chmod -R g+rX photos/
chgrp -R 1001 photos/
```

### 3. Security Options

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    security_opt:
      - no-new-privileges:true
      - seccomp:unconfined  # If needed for image processing
    cap_drop:
      - ALL
    cap_add:
      - CHOWN  # For cache directory
      - SETUID
      - SETGID
```

## Performance Optimization

### 1. Cache Volume

Use a named volume for cache persistence:

```yaml
volumes:
  cache_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /fast-ssd/tenrankai-cache
```

### 2. Resource Limits

Set appropriate resource limits:

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 3. Health Check

Add health check configuration:

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Logging and Monitoring

### 1. Log Configuration

```yaml
services:
  tenrankai:
    image: theatrus/tenrankai:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 2. View Logs

```bash
# View logs
docker logs tenrankai

# Follow logs
docker logs -f tenrankai

# View last 100 lines
docker logs --tail 100 tenrankai
```

## Backup and Recovery

### 1. Backup Script

```bash
#!/bin/bash
# backup-docker.sh

BACKUP_DIR="/backups/tenrankai"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Stop container (optional for consistency)
docker stop tenrankai

# Backup volumes
docker run --rm \
  -v tenrankai_cache_data:/cache:ro \
  -v "$BACKUP_DIR/$DATE":/backup \
  alpine tar czf /backup/cache.tar.gz -C / cache

# Backup configuration
cp config.toml "$BACKUP_DIR/$DATE/"
cp users.toml "$BACKUP_DIR/$DATE/" 2>/dev/null || true

# Restart container
docker start tenrankai

echo "Backup completed: $BACKUP_DIR/$DATE"
```

### 2. Restore Process

```bash
# Stop container
docker stop tenrankai

# Restore cache volume
docker run --rm \
  -v tenrankai_cache_data:/cache \
  -v /backups/tenrankai/20250826_120000:/backup:ro \
  alpine sh -c "cd / && tar xzf /backup/cache.tar.gz"

# Restore configuration
cp /backups/tenrankai/20250826_120000/config.toml .

# Start container
docker start tenrankai
```

## Troubleshooting

### Common Issues

1. **Permission denied errors**:
   ```bash
   # Fix permissions for UID 1001
   docker exec tenrankai id  # Check user
   sudo chown -R 1001:1001 ./cache
   ```

2. **Container exits immediately**:
   ```bash
   # Check logs for errors
   docker logs tenrankai
   # Verify config file syntax
   docker run --rm -v $(pwd)/config.toml:/config.toml:ro \
     theatrus/tenrankai --check-config
   ```

3. **Cache not persisting**:
   ```bash
   # Ensure volume is properly mounted
   docker inspect tenrankai | grep -A 10 Mounts
   ```

### Debug Mode

Run container interactively for debugging:

```bash
docker run -it --rm \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v $(pwd)/photos:/photos:ro \
  --entrypoint sh \
  theatrus/tenrankai:latest
```

## Docker Swarm Deployment

For Docker Swarm deployments:

```yaml
version: '3.8'

services:
  tenrankai:
    image: theatrus/tenrankai:latest
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == worker
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    volumes:
      - config:/config:ro
      - photos:/photos:ro
      - cache:/cache
    networks:
      - traefik-public

volumes:
  config:
    driver: local
  photos:
    driver: local
  cache:
    driver: local

networks:
  traefik-public:
    external: true
```

## Next Steps

- [Configuration Reference](/docs/02-configuration) - Detailed configuration options
- [Deployment Guide](/docs/03-deployment) - Alternative deployment methods
- [Authentication Guide](/docs/07-authentication) - Set up WebAuthn and user access