+++
title = "Configuration Guide"
summary = "Complete guide to configuring Tenrankai for your needs"
date = "2024-12-02"
+++

# Configuration Guide

Tenrankai is highly configurable, allowing you to tailor it to your specific needs. This guide covers all configuration options in detail.

## Configuration File

Tenrankai uses TOML format for configuration. By default, it looks for `config.toml` in the current directory, but you can specify a different file using the `--config` flag.

## Server Configuration

The `[server]` section controls how Tenrankai listens for connections:

```toml
[server]
host = "127.0.0.1"  # IP address to bind to
port = 3000         # Port number
```

- **host**: Use `"127.0.0.1"` for local-only access, `"0.0.0.0"` to listen on all interfaces
- **port**: Any available port number (default: 3000)

## Application Configuration

The `[app]` section contains general application settings:

```toml
[app]
name = "My Gallery"
log_level = "info"  # Options: trace, debug, info, warn, error
download_secret = "change-me-in-production"
download_password = "secure-password-here"
copyright_holder = "Your Name"
base_url = "https://yourdomain.com"

[templates]
directory = "templates"  # Path to Liquid templates

[static_files]
directory = "static"     # Path to static files (CSS, JS, fonts)
```

- **name**: Display name for your gallery
- **log_level**: Logging verbosity (trace, debug, info, warn, error)
- **download_secret**: Secret key for generating download tokens (change in production!)
- **download_password**: Password required for downloading large images
- **copyright_holder**: Name to display in copyright watermarks
- **base_url**: Full URL of your site (used for OpenGraph meta tags)

## Template and Static Files Configuration

The `[templates]` and `[static_files]` sections are required:

- **templates.directory**: Path to your Liquid template files
- **static_files.directory**: Path to static assets (CSS, JavaScript, fonts, images)

## Gallery Configuration

Tenrankai supports multiple independent galleries. Each gallery is configured in a `[[galleries]]` section:

```toml
[[galleries]]
name = "main"                          # Unique identifier
url_prefix = "/gallery"                # URL path prefix
source_directory = "/path/to/photos"   # Where your photos are stored
cache_directory = "cache/main"         # Where to store processed images
images_per_page = 50                   # Pagination setting
new_threshold_days = 7                 # Mark images as "NEW" if modified within X days
pregenerate_cache = false              # Pre-generate all sizes on startup
cache_refresh_interval_minutes = 60    # Auto-refresh interval
jpeg_quality = 85                      # JPEG compression (1-100)
webp_quality = 85.0                    # WebP compression (0.0-100.0)
approximate_dates_for_public = false   # Show only month/year to non-authenticated users

# Custom templates (optional)
gallery_template = "modules/gallery.html.liquid"
image_detail_template = "modules/image_detail.html.liquid"
```

### Image Size Configuration

Each gallery can define custom image sizes:

```toml
[galleries.thumbnail]
width = 300
height = 300

[galleries.gallery_size]
width = 800
height = 800

[galleries.medium]
width = 1200
height = 1200

[galleries.large]
width = 1600
height = 1600
```

### Gallery Preview Configuration

Control how gallery previews are generated:

```toml
[galleries.preview]
max_images = 6      # Number of images to show
max_depth = 3       # How deep to traverse folders
max_per_folder = 2  # Max images from each folder
```

## Multiple Gallery Example

Here's a complete example with multiple galleries:

```toml
# Main portfolio gallery
[[galleries]]
name = "portfolio"
url_prefix = "/portfolio"
source_directory = "/var/photos/portfolio"
cache_directory = "cache/portfolio"
images_per_page = 20
jpeg_quality = 90
webp_quality = 90.0
pregenerate_cache = true

[galleries.thumbnail]
width = 400
height = 400

[galleries.gallery_size]
width = 1000
height = 1000

# Family photos gallery
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "/var/photos/family"
cache_directory = "cache/family"
images_per_page = 100
new_threshold_days = 30

# Client galleries
[[galleries]]
name = "clients"
url_prefix = "/clients"
source_directory = "/var/photos/clients"
cache_directory = "cache/clients"
images_per_page = 50
```

## Posts Configuration

Configure multiple blog/posts systems:

```toml
[[posts]]
name = "blog"
source_directory = "posts/blog"
url_prefix = "/blog"
posts_per_page = 10
refresh_interval_minutes = 30

# Custom templates (optional)
posts_index_template = "modules/posts_index.html.liquid"
post_detail_template = "modules/post_detail.html.liquid"

[[posts]]
name = "docs"
source_directory = "posts/docs"
url_prefix = "/docs"
posts_per_page = 20
```

## Advanced Configuration Options

### Performance Tuning

```toml
[[galleries]]
name = "main"
# ... other settings ...

# Pre-generate all image sizes on startup
pregenerate_cache = true

# Refresh cache every 30 minutes
cache_refresh_interval_minutes = 30

# Process 4 images concurrently
concurrent_processing = 4
```

### Security Settings

```toml
[app]
# Strong passwords for production
download_password = "use-a-long-random-password"
download_secret = "another-long-random-string"

# Optional: Restrict download authentication duration
download_token_lifetime_minutes = 60
```

### Privacy Settings

The `approximate_dates_for_public` option helps protect privacy by showing only approximate capture dates to non-authenticated users:

```toml
[[galleries]]
name = "family"
# ... other settings ...

# Show only "Month Year" to public visitors
# Authenticated users see full date/time
approximate_dates_for_public = true
```

When enabled:
- Public visitors see: "October 2024"
- Authenticated users see: "October 15, 2024 at 3:45 PM"

This is useful for:
- Family photo galleries where exact timestamps reveal personal schedules
- Event galleries where you want to show the month but not specific dates
- Any situation where temporal privacy is a concern

### Hidden Folders

Create a `_folder.md` file in any gallery folder with TOML frontmatter:

```markdown
+++
hidden = true
title = "Private Collection"
+++

This folder won't appear in listings but can be accessed directly.
```

## Environment Variables

Some settings can be overridden using environment variables:

```bash
# Override log level
RUST_LOG=debug tenrankai

# Override server settings
TENRANKAI_HOST=0.0.0.0 TENRANKAI_PORT=8080 tenrankai
```

## Configuration Best Practices

1. **Security**:
   - Always change default passwords and secrets
   - Use strong, random values for production
   - Keep config files secure (chmod 600)

2. **Performance**:
   - Enable `pregenerate_cache` for galleries with stable content
   - Adjust `images_per_page` based on your needs
   - Use appropriate JPEG/WebP quality settings

3. **Organization**:
   - Use meaningful gallery names
   - Keep source and cache directories organized
   - Use consistent URL prefixes

4. **Maintenance**:
   - Regular cache refresh intervals for dynamic galleries
   - Monitor disk usage in cache directories
   - Keep backups of your configuration

## Validation

Tenrankai validates configuration on startup. Common errors:

- **Missing directories**: Source directories must exist
- **Invalid URL prefixes**: Must start with `/`
- **Duplicate names**: Gallery and post names must be unique
- **Invalid quality values**: JPEG (1-100), WebP (0.0-100.0)

## Next Steps

- [Deployment Guide](/docs/03-deployment) - Production deployment best practices
- [Template Customization](/docs/05-templates) - Customize appearance
- [API Documentation](/docs/04-api) - REST API reference