+++
title = "Introducing Tenrankai - A Modern Photo Gallery Server"
summary = "Announcing the release of Tenrankai, a high-performance web gallery server built with Rust and designed for photographers."
date = "2024-12-01"
+++

# Introducing Tenrankai - A Modern Photo Gallery Server

We're excited to announce the release of Tenrankai (展覧会), a high-performance photo gallery server that takes a radically simple approach: it's just files and folders.

## Why We Built Tenrankai

In the world of photo galleries, we found ourselves choosing between complex database-driven systems or limited static generators. Tenrankai takes a different path:

- **No database required** - Just drop files in folders and you're done
- **SyncThing ready** - Edit locally, sync globally, no deployment process
- **Lightning-fast performance** thanks to Rust and intelligent caching
- **Dynamic features** like automatic image resizing and metadata extraction
- **Production-ready capabilities** including watermarking and authentication

## The Power of Simplicity

Tenrankai is a gallery, CMS, and blog platform that relies on nothing more than folders and files. Simply drop files in, or even use [SyncThing](https://syncthing.net/) to keep your gallery or website up to date. No database migrations, no complex deployments - just organize your files and Tenrankai handles the rest.

## Key Features at Launch

### 🚀 Performance First

Built with Rust and the Axum web framework, Tenrankai handles thousands of images without breaking a sweat. Our multi-level caching system ensures that repeat visitors get instant load times.

### 📸 Smart Image Processing

Tenrankai automatically:
- Generates multiple image sizes (thumbnail, gallery, medium, large)
- Creates @2x variants for retina displays
- Preserves ICC color profiles (Display P3, Adobe RGB)
- Serves WebP to supported browsers with JPEG fallback

### 🎨 Beautiful Galleries

The responsive masonry layout adapts perfectly to any screen size. Add descriptions to folders and captions to images using simple markdown files.

### 🔧 Highly Configurable

Run multiple independent galleries from a single instance, each with its own:
- URL prefix and routing
- Source directories
- Quality settings
- Custom templates

## Getting Started

Getting up and running is simple:

```bash
# Clone and build
git clone https://github.com/theatrus/tenrankai.git
cd tenrankai
cargo build --release

# Create basic config
cat > config.toml << EOF
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Gallery"

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache"
EOF

# Run it!
./target/release/tenrankai
```

Visit `http://localhost:3000` and you're ready to go!

## What's Next

We have exciting plans for Tenrankai:

- **Video support** - Handle video files alongside photos
- **Advanced search** - Find images by metadata, tags, or content
- **Plugin system** - Extend functionality with custom plugins
- **Mobile apps** - Native apps for iOS and Android

## Join the Community

Tenrankai is open source under the Apache 2.0 license. We welcome contributions, bug reports, and feature requests!

- **GitHub**: [github.com/theatrus/tenrankai](https://github.com/theatrus/tenrankai)
- **Documentation**: [View our docs](/docs)
- **Issues**: [Report bugs or request features](https://github.com/theatrus/tenrankai/issues)

## Technical Details

For the curious, here's what powers Tenrankai:

- **Language**: Rust 1.89+
- **Web Framework**: Axum
- **Image Processing**: image-rs with custom optimizations
- **Template Engine**: Liquid
- **Async Runtime**: Tokio

## Try It Today

Whether you're a photographer looking to showcase your portfolio, or an organization managing image collections, Tenrankai is ready to serve your needs.

[Get Started with Tenrankai →](/docs/00-quick-start)

---

*Tenrankai is developed by the open source community and is available under the Apache 2.0 license.*
