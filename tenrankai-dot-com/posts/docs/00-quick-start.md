+++
title = "Quick Start Guide"
summary = "Get Tenrankai up and running in 5 minutes"
date = "2026-01-09"
+++

# Quick Start Guide

Want to get Tenrankai running quickly? This guide will have you up and running in just a few minutes.

## Prerequisites

- Rust installed (the project will handle the version)
- Git

## 5-Minute Setup

### 1. Clone and Build

```bash
git clone https://github.com/theatrus/tenrankai.git
cd tenrankai
cargo build --release
```

### 2. Create Basic Configuration

Create a `config.toml` file:

```toml
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Photo Gallery"
cookie_secret = "change-me-in-production"
base_url = "http://localhost:3000"

[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache"
images_per_page = 50
copyright_holder = "Your Name"

# Simple permissions for a public gallery
[[galleries.roles]]
name = "public"
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    "can_see_exact_dates",
    "can_see_location",
    "can_download_thumbnail",
    "can_download_gallery_size"
]
```

### 3. Set Up Directories

```bash
# Create directories
mkdir -p photos cache static

# Add the required font
wget https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.tar.bz2
tar -xjf dejavu-fonts-ttf-2.37.tar.bz2
cp dejavu-fonts-ttf-2.37/ttf/DejaVuSans.ttf static/
rm -rf dejavu-fonts-ttf-2.37*

# Add some test photos
cp ~/Pictures/*.jpg photos/  # Or copy from your photo collection
```

### 4. Run Tenrankai

```bash
./target/release/tenrankai
```

### 5. View Your Gallery

Open your browser to: `http://localhost:3000`

That's it! You now have a working photo gallery.

## What's Next?

### Add More Photos

Simply copy photos to the `photos` directory. Tenrankai will automatically:
- Generate thumbnails
- Extract metadata
- Create a responsive gallery

**Pro tip:** Use [SyncThing](https://syncthing.net/) to sync your photos folder between your devices and server. Edit on your phone or laptop, and your gallery updates automatically!

### Organize Your Photos

Create subdirectories for organization:

```bash
photos/
├── vacation-2026/
│   ├── beach-photos/
│   └── city-tour/
└── family-events/
    ├── birthday/
    └── holidays/
```

### Add Descriptions

Create `_folder.md` in any directory:

```markdown
# Summer Vacation 2026

Photos from our amazing trip to the coast. Perfect weather and great memories!
```

### Control Privacy

Want to hide dates and locations from public viewers? Easy:

```toml
[[galleries.roles]]
name = "public"
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    # Remove these lines to hide dates/location:
    # "can_see_exact_dates",  # Shows only month/year when removed
    # "can_see_location",     # Hides GPS data when removed
    "can_download_thumbnail"
]
```

### Enable Blog

Create a blog post in `posts/blog/`:

```markdown
+++
title = "Welcome to My Gallery"
summary = "Introduction to my photo collection"
date = "2026-01-01"
+++

# Welcome!

This gallery showcases my photography journey...
```

## Common Tasks

### Change Port

Edit `config.toml`:
```toml
[server]
port = 8080
```

### Enable Authentication

Add user database and configure email:
```toml
[app]
user_database = "users.toml"

[email]
provider = "null"  # Logs emails for development (NEW: null provider)
from_address = "noreply@yourdomain.com"

# WebAuthn/Passkeys are automatically enabled when user_database is set
# No additional configuration needed!
```

Then add users:
```bash
./target/release/tenrankai user add admin@example.com --display-name "Admin"
```

### Enable Debug Logging

```bash
./target/release/tenrankai --log-level debug
```

### Refresh Gallery

The gallery automatically refreshes every 60 minutes, or trigger manually:

```bash
curl -X POST http://localhost:3000/api/gallery/main/refresh
```

## Troubleshooting

**"Font file not found"**
- Ensure DejaVuSans.ttf is in the `static` directory

**"No images in gallery"**
- Check that your photos directory contains supported formats (JPEG, PNG)
- Verify the `source_directory` path in config.toml

**"Port already in use"**
- Change the port in config.toml or kill the process using the port

## Learn More

- [Full Installation Guide](/docs/01-installation)
- [Configuration Reference](/docs/02-configuration)
- [Features Overview](/features)