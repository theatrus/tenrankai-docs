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
cookie_secret = "change-me-in-production-use-long-random-string"
download_secret = "change-me-in-production"
download_password = "secure-password-here"
copyright_holder = "Your Name"
base_url = "https://yourdomain.com"
# Optional: Enable authentication
# user_database = "users.toml"

[templates]
directory = "templates"  # Path to Liquid templates
# OR multiple directories for template overrides
# directories = ["templates-custom", "templates"]

[static_files]
# Single directory (backward compatible)
directories = "static"
# OR multiple directories with precedence (first overrides later)
# directories = ["static-custom", "static"]
```

- **name**: Display name for your gallery
- **log_level**: Logging verbosity (trace, debug, info, warn, error)
- **cookie_secret**: Secret key for signing session cookies (change in production!)
- **copyright_holder**: Name to display in copyright watermarks
- **base_url**: Full URL of your site (used for OpenGraph meta tags and login emails)
- **user_database**: Optional path to user database file for authentication

## Template and Static Files Configuration

The `[templates]` and `[static_files]` sections are required:

- **templates.directory**: Path to your Liquid template files
- **static_files.directories**: Path(s) to static assets (CSS, JavaScript, fonts, images)
  - Can be a single string: `directories = "static"`
  - Or an array for cascading directories: `directories = ["static-custom", "static"]`
  - Files in earlier directories override files in later directories

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

# User access control (optional)
# When user_access_list is set, only listed users can view this gallery
# user_access_list = ["admin@example.com", "family@example.com"]

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

# Family photos gallery (restricted access)
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "/var/photos/family"
cache_directory = "cache/family"
images_per_page = 100
new_threshold_days = 30
# Only family members can view this gallery
user_access_list = ["mom@family.com", "dad@family.com", "kids@family.com"]
approximate_dates_for_public = true  # Extra privacy

# Client galleries (restricted to specific clients)
[[galleries]]
name = "clients"
url_prefix = "/clients"
source_directory = "/var/photos/clients"
cache_directory = "cache/clients"
images_per_page = 50
# Each client can only see their own gallery
user_access_list = ["client@company1.com", "contact@agency2.com"]
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
index_template = "modules/posts_index.html.liquid"
post_template = "modules/post_detail.html.liquid"

[[posts]]
name = "docs"
source_directory = "posts/docs"
url_prefix = "/docs"
posts_per_page = 20
```

## Authentication Configuration

Tenrankai supports email-based authentication with optional WebAuthn/Passkey support:

```toml
[app]
user_database = "users.toml"  # Enable authentication

# Optional: Configure email provider for login emails
[email]
from_address = "noreply@yourdomain.com"
from_name = "Your Gallery"  # Optional
reply_to = "support@yourdomain.com"  # Optional
provider = "ses"  # Options: "ses" for production, "null" for development

# Amazon SES configuration (when provider = "ses")
# region = "us-east-1"  # Optional, defaults to AWS SDK default
# access_key_id = "your-key"  # Optional, uses AWS credential chain
# secret_access_key = "your-secret"  # Optional

# Null provider (when provider = "null")
# Logs emails to console instead of sending - perfect for development
```

### User Management

Create and manage users with the CLI:

```bash
# Add a new user
tenrankai user add john.doe@example.com --display-name "John Doe"

# List all users
tenrankai user list

# Remove a user
tenrankai user remove john.doe@example.com
```

### WebAuthn/Passkey Support

When authentication is enabled, users can register passkeys for passwordless login:
- Biometric authentication (fingerprint, face recognition)
- Hardware security keys (YubiKey, etc.)
- Cross-device synchronization via platform providers
- Automatic fallback to email login when unavailable

### Gallery Access Control

You can restrict gallery access to specific users by adding a `user_access_list`:

```toml
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "photos/family"
# Only these users can view this gallery
user_access_list = ["mom@example.com", "dad@example.com", "kids@example.com"]

[[galleries]]
name = "clients"
url_prefix = "/clients"
source_directory = "photos/clients"
# Different users for different galleries
user_access_list = ["client1@company.com", "client2@agency.com"]
```

When `user_access_list` is configured:
- Only authenticated users in the list can view the gallery
- Non-authenticated users receive a 404 error
- Users not in the list receive a 403 forbidden error
- Omit the field to make a gallery public

## Advanced Configuration Options

### Cascading Static Directories

Tenrankai supports multiple static file directories with precedence ordering. This is useful for:
- Overriding default assets with custom versions
- Theme customization without modifying originals
- A/B testing different designs
- Seasonal or event-specific customizations

```toml
[static_files]
# Files in "static-custom" override files in "static"
directories = ["static-custom", "static"]

# Example structure:
# static-custom/
#   style.css        # Overrides default style.css
#   logo.png         # Custom logo
# static/
#   style.css        # Default styles (overridden)
#   script.js        # Used as-is (no override)
#   logo.png         # Default logo (overridden)
```

The asset URL filter automatically handles cache busting:
```liquid
<!-- In templates -->
<link rel="stylesheet" href="{{ 'style.css' | asset_url }}">
<!-- Outputs: /static/style.css?v=1234567890 -->
```

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