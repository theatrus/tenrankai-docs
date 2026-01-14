+++
title = "Installation"
summary = "Install Tenrankai from source, binary, or Docker"
date = "2026-01-13"
+++

# Installation

This guide covers all the ways to install and run Tenrankai.

## Quick Install Options

| Method | Best For | Time |
|--------|----------|------|
| [Docker](#docker) | Production, quick start | 5 min |
| [Pre-built Binary](#pre-built-binary) | Simple deployments | 5 min |
| [From Source](#from-source) | Development, customization | 15 min |

## Docker

The easiest way to run Tenrankai in production.

### Quick Start

```bash
# Create a minimal config.toml
cat > config.toml << 'EOF'
[server]
host = "0.0.0.0"
port = 3000

[app]
name = "My Gallery"
cookie_secret = "change-me-to-a-random-string"

[templates]
directories = ["/app/templates"]

[static_files]
directories = ["/app/static"]

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "/photos"
cache_directory = "/cache"
EOF

# Run with Docker
docker run -d \
  --name tenrankai \
  -p 3000:3000 \
  -v $(pwd)/config.toml:/config.toml:ro \
  -v /path/to/photos:/photos:ro \
  -v tenrankai-cache:/cache \
  ghcr.io/theatrus/tenrankai:latest
```

### Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  tenrankai:
    image: ghcr.io/theatrus/tenrankai:latest
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
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  cache_data:
```

Run with:

```bash
docker-compose up -d
```

### Docker Image Features

- **Optimized size**: ~168 MB multi-stage build
- **Full AVIF support**: HDR and gain maps
- **Security hardened**: Runs as non-root user (UID 1001)
- **All dependencies included**: No additional setup needed

### Volume Mapping

| Path | Purpose | Mode |
|------|---------|------|
| `/config.toml` | Configuration | Read-only |
| `/photos` | Source images | Read-only |
| `/cache` | Processed images | Read-write |
| `/users.toml` | User database (optional) | Read-only |
| `/templates` | Custom templates (optional) | Read-only |
| `/static` | Custom static files (optional) | Read-only |

## Pre-built Binary

Download and run directly on Linux.

### Download

```bash
# Download latest release
curl -LO https://github.com/theatrus/tenrankai/releases/latest/download/tenrankai-linux-amd64

# Make executable
chmod +x tenrankai-linux-amd64

# Move to PATH
sudo mv tenrankai-linux-amd64 /usr/local/bin/tenrankai
```

### Run

```bash
# With config in current directory
tenrankai serve

# With custom config
tenrankai serve --config /path/to/config.toml
```

## From Source

Build from source for development or customization.

### Prerequisites

- **Rust 1.89+** (auto-installed via rust-toolchain.toml)
- **Node.js 18+** and npm (for frontend build)
- **Git**

### Build

```bash
# Clone repository
git clone https://github.com/theatrus/tenrankai.git
cd tenrankai

# Build (includes frontend)
cargo build --release

# Binary is at target/release/tenrankai
```

The build automatically:
- Downloads correct Rust version
- Installs npm dependencies
- Builds React frontend
- Compiles optimized binary

### Build Options

```bash
# Without AVIF support (faster build, smaller binary)
cargo build --release --no-default-features

# Development build (faster, debug symbols)
cargo build

# Skip frontend build
TENRANKAI_SKIP_FRONTEND=1 cargo build --release
```

### Install

```bash
# Copy to system path
sudo cp target/release/tenrankai /usr/local/bin/

# Or install via cargo
cargo install --path .
```

## Initial Setup

After installation, you need to set up your site.

### 1. Create Directory Structure

```bash
mkdir -p my-gallery/{photos,cache,static,templates}
cd my-gallery
```

### 2. Create Configuration

Create `config.toml`:

```toml
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Gallery"
cookie_secret = "$(openssl rand -base64 32)"
base_url = "https://photos.example.com"

[templates]
directories = ["templates"]

[static_files]
directories = ["static"]

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache"
```

### 3. Add Font for Watermarks

If using copyright watermarks, add the DejaVuSans font:

```bash
# Ubuntu/Debian
cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf static/

# Or download
curl -LO https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2
tar -xjf dejavu-fonts-ttf-2.37.tar.bz2
cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf static/
```

### 4. Add Images

Copy or symlink your photos:

```bash
cp -r /path/to/your/photos/* photos/
# or
ln -s /path/to/your/photos photos
```

### 5. Run

```bash
tenrankai serve
```

Visit `http://localhost:3000` to see your gallery.

## Verify Installation

```bash
# Check health endpoint
curl http://localhost:3000/api/health

# Check version
tenrankai --version

# Test with auto-shutdown
tenrankai serve --quit-after 5
```

## Running as a Service

### systemd (Linux)

Create `/etc/systemd/system/tenrankai.service`:

```ini
[Unit]
Description=Tenrankai Photo Gallery
After=network.target

[Service]
Type=simple
User=tenrankai
WorkingDirectory=/opt/tenrankai
ExecStart=/usr/local/bin/tenrankai serve
Restart=on-failure
RestartSec=5

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ReadWritePaths=/opt/tenrankai/cache

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tenrankai
sudo systemctl start tenrankai
sudo systemctl status tenrankai
```

## Troubleshooting

### Permission Denied

```bash
# Check directory permissions
ls -la photos/ cache/

# Fix ownership (for Docker, UID 1001)
sudo chown -R 1001:1001 cache/
```

### Port Already in Use

```bash
# Use different port
tenrankai serve --port 8080

# Or check what's using the port
lsof -i :3000
```

### Build Fails

```bash
# Update Rust
rustup update

# Clean and rebuild
cargo clean
cargo build --release

# Check Node.js
node --version  # Should be 18+
npm --version
```

### No Images Displayed

- Check `source_directory` path exists
- Ensure images are JPEG, PNG, WebP, or AVIF
- Check file permissions
- Look at logs: `tenrankai serve --log-level debug`

## Next Steps

- [Core Concepts](/docs/02-core-concepts) - Understand how Tenrankai works
- [Gallery Setup](/docs/03-galleries) - Configure your galleries
- [Deployment](/docs/06-deployment) - Production deployment guide
