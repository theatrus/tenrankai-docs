+++
title = "Configuration Guide"
summary = "Complete guide to configuring Tenrankai with role-based permissions and advanced features"
date = "2026-01-09"
+++

# Configuration Guide

Tenrankai is highly configurable, allowing you to tailor it to your specific needs. This guide covers all configuration options including role-based permissions, metadata storage, image protection features, and more.

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

The `[templates]` and `[static_files]` sections support cascading directories for easy customization. Both support local filesystem paths and S3 URLs:

```toml
[templates]
# Single directory (backward compatible)
directory = "templates"

# Or cascading directories (files in first directory override later ones)
directories = ["templates-custom", "templates"]

# Or with S3 fallback
directories = ["templates-local", "s3://my-bucket/templates?region=us-west-2"]

[static_files]
# Single directory (backward compatible)
directory = "static"

# Or cascading directories for customization
directories = ["static-custom", "static"]

# With S3 and signed URL redirects (reduces server bandwidth)
directories = ["s3://my-bucket/static?region=us-west-2"]
use_redirects = true
```

- **templates.directory/directories**: Path(s) to your Liquid template files
- **static_files.directory/directories**: Path(s) to static assets (CSS, JavaScript, fonts, images)
- **static_files.use_redirects**: When `true`, S3-backed files return 307 redirects to signed URLs
- Files in earlier directories take precedence over files in later directories
- Perfect for customizing themes without modifying core files

## S3 Storage Support

Tenrankai supports Amazon S3 for storing galleries, caches, templates, posts, and static files. This enables cloud-native deployments and hybrid configurations.

### S3 URL Format

Use S3 URLs anywhere a directory path is accepted:

```
s3://bucket-name/optional-prefix?region=us-west-2
```

- **bucket-name**: Your S3 bucket name
- **optional-prefix**: Path prefix within the bucket (optional)
- **region**: AWS region (optional, defaults to AWS SDK default)

### Configuration Examples

**S3 Cache with Local Source** (recommended for performance):
```toml
[[galleries]]
name = "photos"
source_directory = "photos"                              # Local for fast reads
cache_directory = "s3://my-bucket/cache?region=us-west-2" # S3 for persistence
```

**Full S3 Gallery**:
```toml
[[galleries]]
name = "archive"
source_directory = "s3://my-bucket/photos?region=us-west-2"
cache_directory = "s3://my-bucket/cache?region=us-west-2"
```

**Static Files with Signed URL Redirects**:
```toml
[static_files]
directories = ["s3://my-bucket/static?region=us-west-2"]
use_redirects = true  # Clients download directly from S3
```

**Templates with S3 Fallback**:
```toml
[templates]
directories = ["templates-local", "s3://my-bucket/templates?region=us-west-2"]
```

**Posts from S3**:
```toml
[[posts]]
name = "blog"
source_directory = "s3://my-bucket/posts/blog?region=us-west-2"
url_prefix = "/blog"
```

### AWS Credentials

Tenrankai uses the standard AWS SDK credential chain:

1. **Environment variables**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
2. **AWS credentials file**: `~/.aws/credentials`
3. **IAM role credentials**: EC2 instance profiles, ECS task roles, Lambda execution roles

For production on AWS infrastructure, IAM roles are recommended (no credentials in config).

### S3 Performance Tips

1. **Hybrid Configuration**: Keep source images local, use S3 for cache persistence
2. **Signed URL Redirects**: Enable `use_redirects` for static files to reduce server bandwidth
3. **Region Selection**: Choose a region close to your server for lower latency
4. **Pre-generation**: Use `tenrankai cache pregenerate` to warm the S3 cache before deployment

### Components with S3 Support

| Component | S3 Support | Notes |
|-----------|------------|-------|
| Gallery Source | ✅ | Source images from S3 |
| Gallery Cache | ✅ | Processed images and metadata |
| Static Files | ✅ | With optional signed URL redirects |
| Templates | ✅ | Multi-directory with precedence |
| Posts | ✅ | Markdown files from S3 |

## Gallery Configuration

Tenrankai supports multiple independent galleries. Each gallery is configured in a `[[galleries]]` section.

### Basic Gallery Settings

```toml
[[galleries]]
name = "main"                          # Unique identifier
url_prefix = "/gallery"                # URL path prefix
source_directory = "/path/to/photos"   # Local path or S3 URL
cache_directory = "cache/main"         # Local path or S3 URL
images_per_page = 50                   # Pagination setting
new_threshold_days = 7                 # Mark images as "NEW" if modified within X days
cache_refresh_interval_minutes = 60    # Auto-refresh interval
jpeg_quality = 85                      # JPEG compression (1-100)
webp_quality = 85.0                    # WebP compression (0.0-100.0)
copyright_holder = "Your Name"         # Per-gallery copyright watermark
image_indexing = "filename"            # URL format: "filename", "sequence", or "unique_id"

# Custom templates (optional)
gallery_template = "modules/gallery.html.liquid"
image_detail_template = "modules/image_detail.html.liquid"

# Pre-generation configuration (optional)
# [galleries.pregenerate]
# formats = { jpeg = true, webp = true, avif = false }
# sizes = { thumbnail = true, gallery = true, medium = true, large = false }
# tiles = false

# Tile configuration for enhanced zoom (optional)
# [galleries.tiles]
# tile_size = 1024
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
- **can_use_zoom** - Basic click-to-zoom loupe (uses medium image at 1.8x scale)
- **can_use_tile_zoom** - Enhanced high-resolution zoom using tiles (requires tiles config)
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

### Metadata Storage System

When users have appropriate permissions, they can add metadata (comments, picks, highlights, tags) to images. This metadata is stored in `.toml` sidecar files alongside the images:

```toml
# Example: IMG_1234.jpg.toml (created automatically)
[picks]
"user@example.com" = true

[highlights]
"user@example.com" = true

[tags]
"user@example.com" = ["sunset", "landscape", "california"]

[[comments]]
user = "user@example.com"
comment = "Beautiful sunset!"
timestamp = "2026-01-09T10:30:00Z"

# Comments can include area selections
[[comments]]
user = "photographer@example.com"
comment = "Great detail in the clouds here"
timestamp = "2026-01-09T11:45:00Z"
[comments.image_area]
x = 25.5      # Percentage from left
y = 10.2      # Percentage from top
width = 30.0  # Percentage width
height = 25.0 # Percentage height
```

The gallery view shows badges for images with metadata:
- ✓ (checkmark) - Image marked as pick
- ⭐ (star) - Image highlighted
- 💬 (speech bubble) - Has comments
- 🏷️ (tag) - Has tags

### Image Area Comments

Users can now select specific areas of an image when adding comments:

- **Visual Selection**: Click and drag to select rectangular areas
- **Touch Support**: Works on mobile devices with touch gestures
- **Edit Support**: Areas can be added, changed, or removed when editing comments
- **Visual Feedback**: Selected areas are highlighted when viewing comments
- **Percentage-Based**: Areas use percentage coordinates for responsive display

This feature is perfect for:
- **Client Feedback**: Point out specific details needing adjustment
- **Collaborative Review**: Discuss particular elements in an image
- **Education**: Highlight technical aspects or composition elements
- **Quality Control**: Mark areas with issues or exceptional quality

### Gallery Filter Bar

Users with `can_read_metadata` permission can filter galleries by metadata type:
- Picks (✓) - Show only images marked as picks
- Rejects (✗) - Show images marked as rejects
- Highlights (⭐) - Show highlighted images
- Comments (💬) - Show images with comments

Filter selections persist in the URL for easy sharing: `/gallery?filter=picks,comments`

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
provider = "ses"  # Options: "ses", "null"
from_address = "noreply@yourdomain.com"
from_name = "Your Gallery"  # Optional
reply_to = "support@yourdomain.com"  # Optional

# Amazon SES Configuration (for production)
# The AWS SDK uses a credential provider chain:
# 1. Explicit credentials in config (access_key_id, secret_access_key)
# 2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
# 3. AWS credentials file (~/.aws/credentials)
# 4. IAM role credentials (EC2, ECS, Lambda)
region = "us-east-1"  # Optional, defaults to AWS SDK default region
# access_key_id = "your-key"       # Optional - use IAM roles instead
# secret_access_key = "your-secret" # Optional - use IAM roles instead

# OR Null Provider (for development - logs emails instead of sending)
# provider = "null"
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

# Update user display name
tenrankai user update john.doe@example.com --display-name "John Smith"

# Remove a user
tenrankai user remove john.doe@example.com
```

Users can:
- Manage their passkeys at `/_login/profile`
- Add multiple passkeys for different devices
- Use passwordless WebAuthn authentication

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

### Enhanced Metadata Sources

Tenrankai reads metadata from multiple sources with the following priority:

1. **Markdown files** (`IMAGE.jpg.md` or `IMAGE.md`)
   ```markdown
   +++
   title = "Sunset at Big Sur"
   description = "Golden hour magic"
   tags = ["sunset", "landscape"]
   
   # Astronomy-specific fields
   telescope = "Celestron NexStar 8SE"
   mount = "EQ6-R Pro"
   filters = "Ha, OIII, SII"
   total_exposure_hours = 12.5
   ra = "05:34:31.94"
   dec = "+22:00:52.2"
   additional_details = "7nm narrowband filters, Bortle 3 site"
   +++
   
   Extended description in markdown format...
   ```

2. **XMP sidecar files** (`IMAGE.jpg.xmp`)
   - Automatically parsed for standard metadata
   - Supports Adobe Lightroom and other XMP-compatible tools

3. **EXIF data** (embedded in image)
   - Camera settings, GPS, timestamps
   - Lowest priority, can be overridden

This allows you to:
- Override incorrect EXIF data
- Add rich descriptions and context
- Support specialized workflows (e.g., astrophotography)
- Maintain metadata separate from image files

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

### Zoom Features

Tenrankai offers different zoom experiences for desktop and mobile, controlled by permissions:

**Desktop: Click-to-Zoom Loupe** (`can_use_zoom`):
- Click and hold to activate magnifying loupe
- Uses medium-sized image at 1.8x scale
- Custom cursor indicates zoom availability
- Image protection via CSS background-image

**Desktop: Tile-Based Loupe** (`can_use_tile_zoom`):
- Enhanced loupe using high-resolution tiles
- Full detail inspection for large images
- Requires `[galleries.tiles]` configuration

**Mobile: Pinch-to-Zoom** (`can_use_zoom`):
- Native pinch gesture to zoom in/out
- Double-tap to quick zoom at tap location
- Pan gesture to navigate when zoomed
- Fullscreen modal with zoom level indicator
- Automatically loads high-res tiles when zoom > 1.5x
- Swipe navigation disabled while zoomed

Both platforms feature smooth animations and image protection.

### Hide Technical Details

Control visibility of camera and technical information per folder:

```markdown
# In _folder.md
+++
title = "Client Portfolio"
hide_technical_details = true  # Hides camera, lens, EXIF data
+++
```

When enabled:
- Removes camera make/model, lens information
- Hides technical settings (ISO, aperture, shutter speed)
- Removes GPS coordinates
- Keeps title, description, and navigation
- Perfect for professional portfolios


### Cache Pre-Generation

Configure which image variants to pre-generate on server startup:

```toml
[galleries.pregenerate]
# Which formats to pre-generate
formats = { jpeg = true, webp = true, avif = false }

# Which sizes to pre-generate
sizes = { thumbnail = true, gallery = true, medium = true, large = false }

# Whether to pre-generate tiles (requires tiles config)
tiles = false
```

Pre-generation benefits:
- **Parallel processing**: Uses all CPU cores for faster generation
- **Memory-safe**: Limits concurrent operations to prevent memory exhaustion
- **Incremental**: Only generates missing cache entries
- **Cancellation support**: Graceful shutdown on Ctrl+C
- **Progress logging**: See detailed progress in server logs

### Tile-Based High-Resolution Zoom

Enable high-resolution tiled zoom for detailed image exploration:

```toml
[galleries.tiles]
tile_size = 1024  # Size of each tile in pixels

[galleries.permissions.roles.contributor]
permissions = {
    can_use_zoom = true,       # Basic zoom (medium image)
    can_use_tile_zoom = true   # Enhanced tile-based zoom
}
```

To pre-generate tiles, enable in the pregenerate section:
```toml
[galleries.pregenerate]
tiles = true  # Requires [galleries.tiles] to be configured
```

### Cache Management CLI

Tenrankai provides CLI commands for cache management:

```bash
# Generate a format coverage report for a gallery
tenrankai cache report -g photos

# Clean up outdated cache files
tenrankai cache cleanup -g photos

# Invalidate specific cache entries (force regeneration)
tenrankai cache invalidate -g photos -t composite -p "2026-01-vacation"
tenrankai cache invalidate -g photos -t image -p "IMG_1234.jpg"

# List cached composite images
tenrankai cache list-composites -g photos
```

The cache report shows which image sizes and formats have been generated, helping you verify pre-generation coverage.

## AI-Powered Image Analysis

Tenrankai integrates with OpenAI's Vision API to automatically generate keywords and alt-text for images.

### OpenAI Configuration

```toml
[openai]
api_key = "sk-your-openai-api-key"  # Required
model = "gpt-5.2"                    # Default model
rate_limit_ms = 1000                 # Delay between API calls
max_tokens = 300                     # Max response tokens

# Background processing (optional)
enable_background_analysis = false   # Enable automatic analysis
background_interval_minutes = 60     # How often to run
background_batch_size = 50           # Max images per run
```

### Analysis CLI Commands

```bash
# Analyze all images in a gallery
tenrankai analyze-images -g photos

# Analyze a specific folder
tenrankai analyze-images -g photos -f "2026-01-vacation"

# Limit number of images analyzed
tenrankai analyze-images -g photos --limit 100

# Force re-analysis of already analyzed images
tenrankai analyze-images -g photos --force

# Dry run - see what would be analyzed
tenrankai analyze-images -g photos --dry-run

# Clear AI analysis data
tenrankai clear-analysis -g photos
tenrankai clear-analysis -g photos -f "2026-01-vacation" --dry-run
```

### What Gets Generated

For each image, the AI generates:
- **Keywords**: Descriptive tags for the image content
- **Alt-text**: Accessibility description for screen readers

This data is stored in the image's metadata sidecar file (`.toml`) and displayed in the image detail view.

### Cascading Directories

Override default assets without modifying core files:

```toml
[static_files]
# Files in first directory override later ones
directories = ["static-custom", "static-theme", "static"]

[templates]
directories = ["templates-brand", "templates"]
```

## CSS Theming and Customization

Tenrankai supports custom themes through CSS variable overrides, allowing you to completely customize the look and feel without modifying core files.

### Quick Theme Setup

1. Create a custom static directory (e.g., `static-custom/`)
2. Copy `static/theme-override.css` to your custom directory
3. Configure cascading directories in `config.toml`:
   ```toml
   [static_files]
   directories = ["static-custom", "static"]
   ```
4. Edit your `theme-override.css` to customize colors, fonts, and styles
5. Restart the server

### CSS Variables Reference

Tenrankai uses CSS custom properties (variables) that can be overridden. Key variables include:

**Background Colors:**
| Variable | Description |
|----------|-------------|
| `--bg-primary` | Main background |
| `--bg-secondary` | Secondary background (containers) |
| `--bg-card` | Card/panel backgrounds |
| `--bg-hover` | Hover state backgrounds |
| `--header-bg` | Header background |

**Text Colors:**
| Variable | Description |
|----------|-------------|
| `--text-primary` | Main text |
| `--text-secondary` | Secondary/muted text |
| `--link-color` | Link color |
| `--link-hover` | Link hover color |

**Fonts:**
| Variable | Description |
|----------|-------------|
| `--font-body` | Body text font stack |
| `--font-heading` | Heading font stack |
| `--font-mono` | Monospace font stack |

**Spacing:**
| Variable | Default |
|----------|---------|
| `--spacing-xs` | `0.25rem` |
| `--spacing-sm` | `0.5rem` |
| `--spacing-md` | `1rem` |
| `--spacing-lg` | `1.5rem` |
| `--spacing-xl` | `2rem` |

### Example: Warm Sepia Theme

```css
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap');

:root[data-theme="light"],
:root:not([data-theme]) {
    --bg-primary: #faf8f5;
    --bg-secondary: #f5f0e8;
    --bg-card: #ffffff;
    --text-primary: #3d3d3d;
    --text-secondary: #6b6b6b;
    --link-color: #8b5a2b;
    --link-hover: #6b4423;
    --border-color: #e0d6c8;

    --font-body: 'Open Sans', sans-serif;
    --font-heading: 'Merriweather', Georgia, serif;
}

:root[data-theme="dark"] {
    --bg-primary: #1f1a15;
    --bg-secondary: #2a241d;
    --bg-card: #332b22;
    --text-primary: #e8e0d5;
    --text-secondary: #a89f94;
    --link-color: #d4a574;
    --link-hover: #e8c4a0;
    --border-color: #4a4035;
}
```

### Using Custom Fonts

**Google Fonts:**
```css
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');

:root,
:root[data-theme="dark"],
:root[data-theme="light"] {
    --font-heading: 'Playfair Display', Georgia, serif;
}
```

**Local Fonts:**
1. Place font files in your custom static directory (e.g., `static-custom/fonts/`)
2. Define `@font-face` rules in your theme-override.css:
```css
@font-face {
    font-family: 'CustomFont';
    src: url('/static/fonts/CustomFont-Regular.woff2') format('woff2');
    font-weight: 400;
    font-display: swap;
}

:root {
    --font-body: 'CustomFont', sans-serif;
}
```

### Safe Component Classes

These classes are intended for theme customization and are stable across versions:

| Class | Description |
|-------|-------------|
| `.gallery-grid` | Gallery image grid container |
| `.gallery-item` | Individual gallery item |
| `.card` | Card/panel component |
| `.navbar` | Navigation bar |
| `.container` | Main content container |
| `.image-detail-content` | Image detail page content |

### Theme Tips

1. **Dark/Light Support**: Always define both `:root[data-theme="light"]` and `:root[data-theme="dark"]` to work with the built-in theme toggle
2. **Auto Theme**: Include `:root:not([data-theme])` in your light theme selector for OS preference detection
3. **Test Both Modes**: After making changes, test both light and dark modes using the theme toggle
4. **Font Loading**: Use `font-display: swap` for custom fonts to prevent invisible text during loading

For the complete CSS variables reference and more example themes, see the [Theming Guide](https://github.com/theatrus/tenrankai/blob/main/docs/THEMING.md) in the repository.

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
   - Enable `hide_technical_details` for client portfolios

3. **Performance**:
   - Enable `pregenerate_cache` for stable galleries
   - Use appropriate JPEG/WebP quality settings
   - Set appropriate cache refresh intervals
   - React frontend builds automatically, no configuration needed

4. **User Experience**:
   - Enable WebAuthn for easy passwordless login
   - Use role inheritance to avoid repetition
   - Provide appropriate download sizes for each audience
   - Enable `can_use_zoom` for detailed image exploration
   - Use metadata features for collaborative workflows

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