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
- Node.js (for building the React frontend)

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
[galleries.permissions]
public_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = {
    can_view = true,             # Includes thumbnail & gallery size downloads
    can_see_exact_dates = true,
    can_see_location = true,
    can_see_technical_details = true,
    can_use_zoom = true,         # Enable click-to-zoom loupe
    can_read_metadata = true     # See comments, picks, and tags
}
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
- Extract metadata from EXIF, XMP sidecar files, and markdown frontmatter
- Create a responsive gallery with masonry layout
- Build the React frontend for modern image viewing

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
+++
title = "Summer Vacation 2026"
hide_technical_details = false  # Show camera info
+++

# Summer Vacation 2026

Photos from our amazing trip to the coast. Perfect weather and great memories!
```

Or add metadata to individual images with `IMAGE.jpg.md`:

```markdown
+++
title = "Sunset at the Beach"
description = "Golden hour magic captured at Big Sur"
tags = ["sunset", "landscape", "california"]
+++

This was taken during our last evening at the coast.
```

### Control Privacy

Want to hide dates and locations from public viewers? Easy:

```toml
[galleries.permissions.roles.viewer]
name = "Viewer"
# Remove these lines to hide dates/location:
# can_see_exact_dates = true,  # Shows only month/year when removed
# can_see_location = true,     # Hides GPS data when removed
permissions = {
    can_view = true,             # Includes thumbnail & gallery size downloads
    can_use_zoom = true          # Keep zoom for better viewing
}
```

For maximum privacy, use non-guessable URLs:

```toml
[[galleries]]
name = "main"
image_indexing = "unique_id"  # URLs like /gallery/image/a3k2x
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
provider = "null"  # Logs emails for development
from_address = "noreply@yourdomain.com"

# WebAuthn/Passkeys are automatically enabled when user_database is set
# No additional configuration needed!
```

Then add users:
```bash
./target/release/tenrankai user add admin@example.com --display-name "Admin"
```

Enable user metadata (comments, picks, tags):
```toml
[galleries.permissions.roles.member]
name = "Member"
permissions = {
    can_view = true,
    can_add_comments = true,
    can_set_picks = true,
    can_add_tags = true
}
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
- Check that your photos directory contains supported formats (JPEG, PNG, WebP, AVIF)
- Verify the `source_directory` path in config.toml

**"Port already in use"**
- Change the port in config.toml or kill the process using the port

**"React build failed"**
- Ensure Node.js is installed
- Check npm error messages in the log output

## Learn More

- [Full Installation Guide](/docs/01-installation)
- [Configuration Reference](/docs/02-configuration)
- [Features Overview](/features)