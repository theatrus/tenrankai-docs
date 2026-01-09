+++
title = "Installation Guide"
summary = "Learn how to install and set up Tenrankai on your server"
date = "2026-01-09"
+++

# Installation Guide

Getting Tenrankai up and running is straightforward. This guide will walk you through the installation process step by step.

## Prerequisites

Before installing Tenrankai, ensure you have the following:

- **Rust 1.89.0 or later** - The project includes a `rust-toolchain.toml` file that will automatically download the correct version
- **Git** - For cloning the repository
- **DejaVuSans.ttf font file** - Required for copyright watermarking (place in the `static` directory)

## Installation Methods

### Building from Source (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/theatrus/tenrankai.git
   cd tenrankai
   ```

2. **Build the project:**
   ```bash
   cargo build --release
   ```
   
   The build process will:
   - Download Rust 1.89.0 if not already installed (via rust-toolchain.toml)
   - Compile all dependencies
   - Create an optimized binary in `target/release/tenrankai`

3. **Copy the binary to your preferred location:**
   ```bash
   sudo cp target/release/tenrankai /usr/local/bin/
   ```

### Using Cargo Install

You can also install directly from the repository:

```bash
cargo install --git https://github.com/theatrus/tenrankai.git
```

## Initial Setup

### 1. Create Configuration File

Create a `config.toml` file based on the example:

```bash
cp config.example.toml config.toml
```

Edit the configuration to match your setup:

```toml
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Gallery"
cookie_secret = "change-me-in-production"
base_url = "https://yourdomain.com"

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "/path/to/your/photos"
cache_directory = "cache/main"
images_per_page = 50
copyright_holder = "Your Name"
```

### 2. Create Required Directories

```bash
# Create cache directories
mkdir -p cache/main

# Create static directory for fonts
mkdir -p static

# Create photo directories (if not existing)
mkdir -p photos
```

### 3. Add DejaVuSans Font

Download and place the DejaVuSans.ttf font in the static directory:

```bash
# On Ubuntu/Debian
cp /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf static/

# Or download directly
wget https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2
tar -xjf dejavu-fonts-ttf-2.37.tar.bz2
cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf static/
```

## Running Tenrankai

### Basic Usage

Start the server with default configuration:

```bash
tenrankai
```

### With Custom Options

```bash
# Use a different config file
tenrankai --config /path/to/config.toml

# Override host and port
tenrankai --host 0.0.0.0 --port 8080

# Enable debug logging
tenrankai --log-level debug

# Auto-shutdown after testing
tenrankai --quit-after 10
```

### Running as a Service

For production deployments, it's recommended to run Tenrankai as a systemd service.

Create `/etc/systemd/system/tenrankai.service`:

```ini
[Unit]
Description=Tenrankai Photo Gallery Server
After=network.target

[Service]
Type=simple
User=tenrankai
WorkingDirectory=/opt/tenrankai
ExecStart=/usr/local/bin/tenrankai --config /opt/tenrankai/config.toml
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/tenrankai/cache

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable tenrankai
sudo systemctl start tenrankai
```

## Verifying Installation

1. **Check server status:**
   ```bash
   curl http://localhost:3000/api/health
   ```

2. **Visit the web interface:**
   Open your browser to `http://localhost:3000`

3. **Check logs:**
   ```bash
   # If running directly
   tenrankai --log-level debug
   
   # If running as a service
   sudo journalctl -u tenrankai -f
   ```

## Docker Installation (Alternative)

While not officially provided, you can create a Dockerfile:

```dockerfile
FROM rust:1.89 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/tenrankai /usr/local/bin/
COPY static/DejaVuSans.ttf /app/static/
WORKDIR /app
EXPOSE 3000
CMD ["tenrankai"]
```

## Next Steps

- [Configuration Guide](/docs/02-configuration) - Learn about all configuration options
- [Deployment Guide](/docs/03-deployment) - Best practices for production deployment
- [Template Customization](/docs/05-templates) - Customize the look and feel

## Troubleshooting

### Common Issues

**Rust version mismatch:**
- The project will automatically use Rust 1.89.0 via rust-toolchain.toml
- If you have issues, run `rustup update`

**Missing font file:**
- Ensure DejaVuSans.ttf is in the static directory
- Watermarking will fail without this font

**Permission denied:**
- Check that the user has read access to photo directories
- Ensure write access to cache directories

**Port already in use:**
- Change the port in config.toml or use `--port` flag

For more help, visit our [GitHub Issues](https://github.com/theatrus/tenrankai/issues) page.