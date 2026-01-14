+++
title = "Deployment"
summary = "Production deployment strategies and best practices"
date = "2026-01-13"
+++

# Deployment

This guide covers production deployment strategies for Tenrankai, including systemd services, reverse proxy configuration, and security best practices.

## Production Configuration

### Security Configuration

For production deployments, create a secure configuration file:

```toml
[server]
host = "127.0.0.1"  # Bind to localhost for reverse proxy
port = 3000

[app]
name = "Your Gallery"
base_url = "https://photos.example.com"
user_database = "users.toml"
cookie_secret = "your-32-character-session-secret"

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "/var/lib/tenrankai/photos"
cache_directory = "/var/cache/tenrankai"

[galleries.pregenerate]
formats = { jpeg = true, webp = true }
sizes = { thumbnail = true, gallery = true, medium = true }
```

**Security Notes:**
- Always bind to `127.0.0.1` and use a reverse proxy in production
- Generate secrets with: `openssl rand -base64 32`
- Enable pre-generation for better performance with large galleries

### Directory Structure

Create the recommended directory structure:

```bash
# Create system directories
sudo mkdir -p /opt/tenrankai
sudo mkdir -p /var/lib/tenrankai/photos
sudo mkdir -p /var/cache/tenrankai
sudo mkdir -p /etc/tenrankai

# Create tenrankai user
sudo useradd --system --home /opt/tenrankai --shell /bin/false tenrankai

# Set permissions
sudo chown -R tenrankai:tenrankai /opt/tenrankai
sudo chown -R tenrankai:tenrankai /var/lib/tenrankai
sudo chown -R tenrankai:tenrankai /var/cache/tenrankai
sudo chown -R tenrankai:tenrankai /etc/tenrankai
```

## Systemd Service

### Service Configuration

Create `/etc/systemd/system/tenrankai.service`:

```ini
[Unit]
Description=Tenrankai Photo Gallery Server
After=network.target
Wants=network.target

[Service]
Type=simple
User=tenrankai
Group=tenrankai
WorkingDirectory=/opt/tenrankai
ExecStart=/opt/tenrankai/tenrankai serve --config /etc/tenrankai/config.toml
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/tenrankai /var/cache/tenrankai

# Resource limits
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

### Enable and Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start on boot
sudo systemctl enable tenrankai

# Start the service
sudo systemctl start tenrankai

# Check status
sudo systemctl status tenrankai
```

### Service Management

```bash
# View logs
sudo journalctl -u tenrankai -f

# Restart service
sudo systemctl restart tenrankai

# Stop service
sudo systemctl stop tenrankai
```

## Reverse Proxy Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/tenrankai`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # Client max body size
    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for large image processing
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }

    # Serve static files directly (optional optimization)
    location /static/ {
        alias /opt/tenrankai/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/tenrankai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Apache Configuration

Create `/etc/apache2/sites-available/tenrankai.conf`:

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    Redirect permanent / https://your-domain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName your-domain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/cert.pem
    SSLCertificateKeyFile /path/to/your/key.pem

    # Security headers
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"

    # Proxy configuration
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/

    # Optional: Serve static files directly
    Alias /static /opt/tenrankai/static
    <Directory "/opt/tenrankai/static">
        Require all granted
        ExpiresActive On
        ExpiresDefault "access plus 1 year"
    </Directory>
</VirtualHost>
```

## SSL/TLS Configuration

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx  # For nginx
# OR
sudo apt install certbot python3-certbot-apache  # For apache

# Obtain certificate
sudo certbot --nginx -d your-domain.com  # For nginx
# OR
sudo certbot --apache -d your-domain.com  # For apache

# Auto-renewal is typically configured automatically
# Test renewal:
sudo certbot renew --dry-run
```

## Monitoring and Logging

### Log Rotation

Configure logrotate in `/etc/logrotate.d/tenrankai`:

```
/var/log/tenrankai/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 tenrankai tenrankai
    postrotate
        systemctl reload tenrankai
    endscript
}
```

### Health Check Script

Create `/opt/tenrankai/health-check.sh`:

```bash
#!/bin/bash
curl -f http://localhost:3000/api/health > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "Tenrankai is healthy"
    exit 0
else
    echo "Tenrankai is not responding"
    exit 1
fi
```

Add to crontab for monitoring:

```bash
# Check every 5 minutes
*/5 * * * * /opt/tenrankai/health-check.sh
```

## Performance Optimization

### System Tuning

```bash
# Increase file descriptor limits
echo "fs.file-max = 65536" >> /etc/sysctl.conf

# Optimize TCP settings for web serving
echo "net.core.somaxconn = 65536" >> /etc/sysctl.conf
echo "net.core.netdev_max_backlog = 5000" >> /etc/sysctl.conf

# Apply changes
sysctl -p
```

### Cache Strategy

- Enable pre-generation for large galleries
- Use SSD storage for cache directories
- Monitor disk usage and implement cache cleanup if needed

### Resource Allocation

- Allocate sufficient RAM for image processing
- Consider using multiple gallery instances with load balancing for high-traffic sites
- Monitor CPU usage during image pre-generation

## Backup and Recovery

### Backup Strategy

```bash
#!/bin/bash
# backup-tenrankai.sh

BACKUP_DIR="/backups/tenrankai"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$BACKUP_DIR/$DATE"

# Backup configuration
cp -r /etc/tenrankai "$BACKUP_DIR/$DATE/config"

# Backup photos (consider using rsync for incremental backups)
rsync -av /var/lib/tenrankai/photos "$BACKUP_DIR/$DATE/"

# Create archive
cd "$BACKUP_DIR"
tar -czf "tenrankai_backup_$DATE.tar.gz" "$DATE"
rm -rf "$DATE"

# Keep only last 30 backups
find "$BACKUP_DIR" -name "tenrankai_backup_*.tar.gz" -mtime +30 -delete
```

### Recovery Process

```bash
# Stop service
sudo systemctl stop tenrankai

# Restore from backup
cd /backups/tenrankai
tar -xzf tenrankai_backup_YYYYMMDD_HHMMSS.tar.gz

# Restore configuration
sudo cp -r YYYYMMDD_HHMMSS/config/* /etc/tenrankai/

# Restore photos
sudo rsync -av YYYYMMDD_HHMMSS/photos/ /var/lib/tenrankai/photos/

# Fix permissions
sudo chown -R tenrankai:tenrankai /etc/tenrankai /var/lib/tenrankai

# Clear cache (will be regenerated)
sudo rm -rf /var/cache/tenrankai/*

# Start service
sudo systemctl start tenrankai
```

## Troubleshooting

### Common Issues

1. **Service won't start**: Check permissions and configuration file syntax
2. **Images not loading**: Verify source directory permissions and cache directory writability
3. **High memory usage**: Monitor large image processing, consider reducing concurrent processing
4. **Slow performance**: Check if pre-generation is enabled, verify SSD usage for cache

### Useful Commands

```bash
# Check service status
sudo systemctl status tenrankai

# View recent logs
sudo journalctl -u tenrankai --since "1 hour ago"

# Test configuration
/opt/tenrankai/tenrankai serve --config /etc/tenrankai/config.toml --log-level debug

# Monitor resource usage
htop
iotop
df -h
```

## Next Steps

Once your Tenrankai instance is deployed:

- [Theming](/docs/07-theming) - Customize appearance
- [Advanced Features](/docs/08-advanced) - S3 storage, AI analysis
- [API Reference](/docs/09-api) - Build custom integrations
