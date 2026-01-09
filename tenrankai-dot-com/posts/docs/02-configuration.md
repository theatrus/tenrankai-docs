+++
title = "Configuration Guide"
summary = "Complete guide to configuring Tenrankai with role-based permissions and advanced features"
date = "2026-01-09"
+++

# Configuration Guide

Tenrankai is highly configurable, allowing you to tailor it to your specific needs. This guide covers all configuration options including the new role-based permission system.

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
base_url = "https://yourdomain.com"
# Optional: Enable authentication
# user_database = "users.toml"
```

- **name**: Display name for your gallery
- **log_level**: Logging verbosity (trace, debug, info, warn, error)
- **cookie_secret**: Secret key for signing session cookies (change in production!)
- **base_url**: Full URL of your site (used for OpenGraph meta tags and login emails)
- **user_database**: Optional path to user database file for authentication

## Template and Static Files Configuration

The `[templates]` and `[static_files]` sections support cascading directories for easy customization:

```toml
[templates]
# Single directory (backward compatible)
directory = "templates"

# Or cascading directories (files in first directory override later ones)
directories = ["templates-custom", "templates"]

[static_files]
# Single directory (backward compatible)
directory = "static"

# Or cascading directories for customization
directories = ["static-custom", "static"]
```

- **templates.directory/directories**: Path(s) to your Liquid template files
- **static_files.directory/directories**: Path(s) to static assets (CSS, JavaScript, fonts, images)
- Files in earlier directories take precedence over files in later directories
- Perfect for customizing themes without modifying core files

## Gallery Configuration

Tenrankai supports multiple independent galleries. Each gallery is configured in a `[[galleries]]` section.

### Basic Gallery Settings

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
copyright_holder = "Your Name"         # Per-gallery copyright watermark (NEW)
image_indexing = "filename"            # URL format: "filename", "sequence", or "unique_id" (NEW)

# Custom templates (optional)
gallery_template = "modules/gallery.html.liquid"
image_detail_template = "modules/image_detail.html.liquid"
```

### Role-Based Permissions (RBAC)

Tenrankai uses a role-based permission system that provides fine-grained control over gallery access.

#### Understanding the Permission System

The permission system is configured within each gallery's `[galleries.permissions]` section:

```toml
[galleries.permissions]
# Role assigned to unauthenticated visitors
public_role = "viewer"

# Role assigned to authenticated users by default
default_authenticated_role = "member"

# Define custom roles with specific permissions
[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true }

[galleries.permissions.roles.member]
name = "Member"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true
}

# Assign specific users to custom roles
[[galleries.permissions.user_roles]]
username = "photographer"
roles = ["admin"]

[[galleries.permissions.user_roles]]
username = "client"
roles = ["member"]
```

#### Available Permissions

**Viewing Permissions:**
- **can_view** - View images in the gallery (includes thumbnail and gallery size downloads)

**Privacy Permissions:**
- **can_see_exact_dates** - See exact capture dates (vs approximate month/year)
- **can_see_location** - See GPS coordinates and maps
- **can_see_technical_details** - See camera, lens, and EXIF data

**Download Permissions:**
- **can_download_medium** - Download medium resolution images
- **can_download_large** - Download large resolution images
- **can_download_original** - Download original files

Note: Thumbnail and gallery size downloads are automatically included with the `can_view` permission.

**Interactive Permissions:**
- **can_use_zoom** - Use zoom functionality for detailed viewing
- **can_read_metadata** - Read user-generated content (comments, picks, tags)

**Content Management:**
- **can_add_comments** - Add comments to images
- **can_edit_own_comments** - Edit your own comments
- **can_delete_own_comments** - Delete your own comments
- **can_set_picks** - Mark images as picks/favorites
- **can_add_tags** - Add tags to images

**Moderation:**
- **can_edit_any_comments** - Edit any user's comments (admin)
- **can_delete_any_comments** - Delete any user's comments (admin)

**Special:**
- **owner_access** - Full access to everything (overrides all other permissions)

#### Permission Examples

**Example 1: Public Portfolio**
```toml
[[galleries]]
name = "portfolio"
copyright_holder = "Professional Photographer Inc."

[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
# Show camera info for credibility
# Allow detailed image viewing
# No location or exact dates for privacy
# No high-res downloads without permission
permissions = {
    can_view = true,
    can_see_technical_details = true,
    can_use_zoom = true
}
```

**Example 2: Family Gallery with Privacy**
```toml
[[galleries]]
name = "family"
copyright_holder = "The Smith Family"

[galleries.permissions]
public_role = "limited"
default_authenticated_role = "limited"

# Public sees limited info
[galleries.permissions.roles.limited]
name = "Limited Viewer"
# Approximate dates only (shows "October 2026" instead of exact date)
permissions = {
    can_view = true
}

# Family members see everything
[galleries.permissions.roles.family_member]
name = "Family Member"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true,
    can_see_technical_details = true,
    can_download_medium = true,
    can_download_large = true,
    can_download_original = true,
    can_use_zoom = true,
    can_read_metadata = true,
    can_add_comments = true,
    can_edit_own_comments = true,
    can_delete_own_comments = true,
    can_set_picks = true,
    can_add_tags = true
}

# Assign family members to their role
[[galleries.permissions.user_roles]]
username = "parent"
roles = ["family_member"]
```

### Folder-Level Permissions

You can override gallery permissions for specific folders by creating a `_folder.md` file within that folder:

**Example: Hide a folder from public view**

Create `photos/private/_folder.md`:
```markdown
+++
title = "Private Photos"

[permissions]
# Remove all public access to this folder
public_role = "none"

# Only specific users can access
default_authenticated_role = "family"

[permissions.roles.family]
name = "Family"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_download_original = true
}
+++

These photos are only visible to family members.
```

**Example: Limited access folder**

Create `photos/preview/_folder.md`:
```markdown
+++
title = "Client Preview"

[permissions]
public_role = "preview_only"

[permissions.roles.preview_only]
name = "Preview Only"
# No downloads or folder browsing allowed
permissions = { can_view = true }
+++

Preview images for client approval.
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

## Authentication Configuration

### Email Provider Configuration

Tenrankai supports multiple email providers for authentication:

```toml
[email]
provider = "ses"  # Options: "ses", "null" (SMTP not yet implemented)
from_address = "noreply@yourdomain.com"
from_name = "Your Gallery"  # Optional
reply_to = "support@yourdomain.com"  # Optional

# Amazon SES Configuration (for production)
# provider = "ses"
region = "us-east-1"  # Optional, uses AWS credential chain
access_key_id = "your-key"  # Optional, uses AWS credential chain
secret_access_key = "your-secret"  # Optional

# OR Null Provider (for development - logs emails instead of sending)
# provider = "null"

# Note: SMTP provider is planned but not yet implemented
```

### WebAuthn/Passkey Configuration

WebAuthn/Passkey support is automatically enabled when authentication is configured. No separate configuration is needed:

```toml
[app]
name = "My Photo Gallery"  # Used as the WebAuthn RP name
base_url = "https://yourdomain.com"  # Required - hostname used as RP ID
user_database = "users.db"  # Enables authentication and WebAuthn

# That's it! WebAuthn is now enabled with:
# - RP ID: yourdomain.com (from base_url hostname)
# - RP Name: "My Photo Gallery" (from app.name)
# - Origin: https://yourdomain.com (from base_url)
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

Users can manage their passkeys at `/_login/profile`.

## Posts Configuration

Configure multiple blog/documentation systems:

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
refresh_interval_minutes = 60
```

## Advanced Features

### Image Indexing Modes

Control how images are referenced in URLs:

1. **filename** (default): `/gallery/image/vacation/IMG_1234.jpg`
   - SEO-friendly, predictable URLs
   - Exposes file naming patterns

2. **sequence**: `/gallery/image/vacation/1`
   - Clean, ordered URLs
   - Good for portfolios and stories

3. **unique_id**: `/gallery/image/vacation/a3k2x`
   - Maximum privacy, prevents URL guessing
   - Best for client galleries


### Cascading Directories

Override default assets without modifying core files:

```toml
[static_files]
# Files in first directory override later ones
directories = ["static-custom", "static-theme", "static"]

[templates]
directories = ["templates-brand", "templates"]
```

## Migration Guide

### From Old Permission System

**Old configuration:**
```toml
approximate_dates_for_public = true
hide_location_from_public = true
hide_technical_details = true  # In _folder.md
```

**New configuration:**
```toml
[galleries.permissions]
public_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
# Note: No can_see_exact_dates, can_see_location, or can_see_technical_details
permissions = {
    can_view = true
}
```

### Copyright Holder

**Old:** Global in `[app]` section
**New:** Per-gallery in each `[[galleries]]` section

```toml
[[galleries]]
name = "main"
copyright_holder = "Your Name"  # Now here instead of [app]
```

## Complete Example

Here's a comprehensive configuration showing all features:

```toml
[server]
host = "0.0.0.0"
port = 8080

[app]
name = "Professional Photography"
log_level = "info"
cookie_secret = "use-openssl-rand-base64-32-output-here"
base_url = "https://photos.example.com"
user_database = "users.toml"

[templates]
directories = ["templates-custom", "templates"]

[static_files]
directories = ["static-custom", "static"]

[email]
provider = "ses"  # Use Amazon SES for production
from_address = "noreply@photos.example.com"
from_name = "Photo Gallery"
region = "us-east-1"
# Uses AWS credential chain for authentication

# WebAuthn is automatically configured based on app settings

# Public portfolio
[[galleries]]
name = "portfolio"
url_prefix = "/"
source_directory = "/srv/photos/portfolio"
cache_directory = "/srv/cache/portfolio"
copyright_holder = "Jane Photographer"
image_indexing = "sequence"
pregenerate_cache = true

[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = {
    can_view = true,
    can_see_technical_details = true,
    can_use_zoom = true
}

# Client gallery with restricted access
[[galleries]]
name = "clients"
url_prefix = "/clients"
source_directory = "/srv/photos/clients"
cache_directory = "/srv/cache/clients"
copyright_holder = "Studio Name"
image_indexing = "unique_id"  # Privacy

[galleries.permissions]
public_role = "preview"
default_authenticated_role = "preview"

# Very limited public access
[galleries.permissions.roles.preview]
name = "Preview"
permissions = { can_view = true }

# Client role with download rights
[galleries.permissions.roles.client]
name = "Client"
permissions = {
    can_view = true,
    can_download_medium = true,
    can_download_original = true,
    can_use_zoom = true,
    can_read_metadata = true,    # See comments and feedback
    can_add_comments = true      # Leave feedback on images
}

# Assign specific clients
[[galleries.permissions.user_roles]]
username = "client"
roles = ["client"]

# Note: Folder-specific permissions are configured via _folder.md files
# within the gallery directories, not in config.toml
```

## Best Practices

1. **Security**:
   - Use strong, random cookie secrets
   - Enable HTTPS in production
   - Use `unique_id` indexing for sensitive galleries
   - Carefully consider each permission

2. **Privacy**:
   - Omit `can_see_exact_dates` for public family photos
   - Omit `can_see_location` to protect home addresses
   - Use folder-level permissions to hide sensitive content

3. **Performance**:
   - Enable `pregenerate_cache` for stable galleries
   - Use appropriate JPEG/WebP quality settings
   - Set appropriate cache refresh intervals

4. **User Experience**:
   - Enable WebAuthn for easy passwordless login
   - Use role inheritance to avoid repetition
   - Provide appropriate download sizes for each audience

## Troubleshooting

Common issues:

- **"Permission denied" errors**: Check role assignments and inheritance
- **Missing images**: Verify folder permissions allow `can_view`
- **Dates showing incorrectly**: Check `can_see_exact_dates` permission
- **Downloads failing**: Ensure appropriate download permissions are set

## Next Steps

- [Deployment Guide](/docs/03-deployment) - Production deployment best practices
- [Template Customization](/docs/05-templates) - Customize appearance
- [API Documentation](/docs/04-api) - REST API reference