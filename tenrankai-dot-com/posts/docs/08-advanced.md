+++
title = "Advanced Features"
summary = "Admin UI, S3 storage, AI image analysis, CLI tools, and power user features"
date = "2026-01-23"
+++

# Advanced Features

This guide covers Tenrankai's advanced features for power users and cloud deployments.

## Admin UI

Tenrankai includes a built-in web-based administration interface for managing users, viewing galleries, and configuring permissions without editing files.

### Accessing the Admin UI

The Admin UI is available at `/_admin/` and requires:
- Authentication (must be logged in)
- `owner_access` permission in any gallery

### Features

**User Management:**
- View all registered users
- Create new users
- Delete users
- Send login invitation emails (72-hour expiry)

**Gallery Viewer:**
- See all configured galleries
- View gallery permissions and role assignments
- See folder structures and image counts

**Role Viewer:**
- View built-in roles and their permissions
- See permission groups organized by category

### Admin API

The Admin UI communicates with a REST API that you can also use programmatically:

```bash
# List all sites
curl -H "Cookie: session=..." https://example.com/_admin/api/sites

# Get site configuration
curl -H "Cookie: session=..." https://example.com/_admin/api/sites/default

# List galleries for a site
curl -H "Cookie: session=..." https://example.com/_admin/api/sites/default/galleries

# Get/update permissions
curl -H "Cookie: session=..." https://example.com/_admin/api/sites/default/permissions

# Reload site configuration
curl -X POST -H "Cookie: session=..." https://example.com/_admin/api/sites/default/reload
```

See the [API Reference](/docs/09-api) for complete Admin API documentation.

## Theme Editor

The Admin UI includes a visual theme editor for customizing colors and fonts without editing CSS files.

### Accessing the Theme Editor

Navigate to `/_admin/theme` (requires admin access). The editor provides:

- **Dark/Light Mode Tabs**: Customize colors for each mode independently
- **Color Pickers**: Visual color selection with hex input
- **Font Selectors**: Choose from 42 curated Google Fonts
- **Force Color Scheme**: Lock users to dark or light mode
- **Reset to Defaults**: Restore original theme

### Customizable Colors

| Color Variable | Description |
|----------------|-------------|
| Background Primary | Main page background |
| Background Secondary | Alternate sections |
| Background Card | Card and panel backgrounds |
| Background Hover | Hover state backgrounds |
| Header Background | Site header |
| Text Primary | Main text color |
| Text Secondary | Secondary text |
| Text Muted | Subtle text, captions |
| Link Color | Link text |
| Link Hover | Link hover state |
| Border Color | Borders and dividers |
| Accent Color | Highlights and accents |
| Danger Button | Delete/destructive actions |

### Font Options

Three font categories can be customized:

- **Body Font**: Main content text
- **Heading Font**: Titles and headers
- **Monospace Font**: Code blocks and technical text

Fonts are organized by style: Sans-serif, Serif, Slab Serif, Display, Script, Rounded, and Monospace. The editor shows a live preview of each font before selection.

### Force Color Scheme

Override user preferences to lock the site to a specific theme:

- **User Choice** (default): Respects system preference and manual toggle
- **Always Dark**: Forces dark mode for all visitors
- **Always Light**: Forces light mode for all visitors

### How It Works

1. Changes are saved to the site's configuration storage
2. Site automatically reloads to apply changes
3. Theme CSS is generated dynamically at `/theme.css`
4. Cache-busting ensures browsers receive updated styles

### Theme API

```bash
# Get current theme
curl -H "Cookie: session=..." https://example.com/_admin/api/theme

# Update theme
curl -X PUT -H "Cookie: session=..." \
  -H "Content-Type: application/json" \
  -d '{"dark":{"bg_primary":"#1a1a2e"},"font_body":"Inter"}' \
  https://example.com/_admin/api/theme

# Reset to defaults
curl -X DELETE -H "Cookie: session=..." https://example.com/_admin/api/theme
```

### Manual CSS Override

For advanced customization beyond the theme editor, create `theme-override.css` in your static directory:

```css
:root {
  --custom-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

[data-theme="dark"] {
  --bg-primary: #0d1117;
}
```

The theme editor and manual overrides work together - editor changes are applied first, then `theme-override.css` additions.

## S3 Storage Support

Tenrankai supports Amazon S3 for storing galleries, caches, templates, and static files.

### S3 URL Format

Use S3 URLs anywhere a path is accepted:

```
s3://bucket-name/prefix?region=us-west-2
```

### Configuration Examples

**Hybrid: Local Source, S3 Cache** (Recommended):
```toml
[[galleries]]
name = "photos"
source_directory = "photos"
cache_directory = "s3://my-bucket/cache?region=us-west-2"
```

**Full S3 Gallery**:
```toml
[[galleries]]
name = "archive"
source_directory = "s3://my-bucket/photos?region=us-west-2"
cache_directory = "s3://my-bucket/cache?region=us-west-2"
```

**Static Files with Redirects**:
```toml
[static_files]
directories = ["s3://my-bucket/static?region=us-west-2"]
use_redirects = true  # Clients download directly from S3
```

**Templates with S3 Fallback**:
```toml
[templates]
directories = ["templates-local", "s3://my-bucket/templates"]
```

### AWS Credentials

Tenrankai uses the standard AWS credential chain:

1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. AWS credentials file (`~/.aws/credentials`)
3. IAM role (EC2, ECS, Lambda)

For production on AWS, use IAM roles.

### S3 Components

| Component | S3 Support | Notes |
|-----------|------------|-------|
| Gallery Source | ✅ | Images from S3 |
| Gallery Cache | ✅ | Processed images |
| Static Files | ✅ | With signed URL redirects |
| Templates | ✅ | Multi-directory support |
| Posts | ✅ | Markdown from S3 |

### Performance Tips

1. **Use hybrid config**: Local source + S3 cache
2. **Enable redirects**: Reduces server bandwidth for static files
3. **Pre-generate cache**: Warm S3 cache before deployment
4. **Choose nearby region**: Lower latency

## Multi-Site Virtual Hosting

Run multiple independent sites from a single Tenrankai instance, each with its own domain, templates, galleries, and settings.

### Overview

Virtual hosting allows:
- **Multiple domains**: Serve different sites on different hostnames
- **Per-site isolation**: Each site has its own templates, static files, galleries, and posts
- **Hot reload**: Update configuration without downtime (SIGHUP)
- **Wildcard subdomains**: Match patterns like `*.clients.example.com`

### Basic Multi-Site Configuration

```toml
[server]
host = "0.0.0.0"
port = 3000

[app]
name = "Multi-Site Gallery"
cookie_secret = "your-secret-here"

# Default site (catch-all for unmatched hostnames)
[sites.default]
hostnames = ["*"]

[sites.default.templates]
directories = ["templates"]

[sites.default.static_files]
directories = ["static"]

[[sites.default.galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache/default/main"

# Photography portfolio site
[sites.photos]
hostnames = ["photos.example.com"]

[sites.photos.templates]
directories = ["templates-photos", "templates"]

[[sites.photos.galleries]]
name = "portfolio"
url_prefix = "/"
source_directory = "portfolio"
cache_directory = "cache/photos"
image_indexing = "unique_id"

# Blog-only site
[sites.blog]
hostnames = ["blog.example.com"]

[sites.blog.templates]
directories = ["templates-blog", "templates"]

[[sites.blog.posts]]
name = "articles"
url_prefix = "/"
source_directory = "blog-posts"
```

### Hostname Matching

Hostnames are matched in priority order:

1. **Exact match** (highest): `photos.example.com`
2. **Glob pattern**: `*.clients.example.com`
3. **Default catch-all**: `*`

```toml
# Exact hostname
[sites.main]
hostnames = ["example.com", "www.example.com"]

# Wildcard subdomain
[sites.clients]
hostnames = ["*.clients.example.com"]

# Catch-all default
[sites.default]
hostnames = ["*"]
```

### Per-Site User Databases

Each site can have its own user authentication:

```toml
[sites.photos]
hostnames = ["photos.example.com"]
user_database = "users-photos.toml"

[sites.clients]
hostnames = ["*.clients.example.com"]
user_database = "users-clients.toml"
```

### Client Delivery Example

Serve client galleries on wildcard subdomains with authentication:

```toml
[sites.clients]
hostnames = ["*.clients.example.com"]
user_database = "users-clients.toml"

[sites.clients.templates]
directories = ["templates-clients", "templates"]

[[sites.clients.galleries]]
name = "delivery"
url_prefix = "/"
source_directory = "clients"
cache_directory = "cache/clients"

[sites.clients.galleries.permissions]
public_role = "none"
default_authenticated_role = "viewer"

[sites.clients.galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true, can_download_large = true }
```

### Hot Reloading

Update configuration without restarting:

```bash
# Send SIGHUP to reload config
kill -HUP $(pgrep tenrankai)
```

What can be hot-reloaded:
- Add/remove sites
- Modify site hostnames
- Add/remove galleries or posts
- Change templates or static files
- Update gallery settings

What requires restart:
- Server host/port changes

### Backward Compatibility

Existing single-site configurations continue to work. If no `[sites.*]` section exists, Tenrankai creates a default site from the top-level configuration:

```toml
# Old format (still works)
[[galleries]]
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
```

## AI Image Analysis

Tenrankai integrates with OpenAI Vision to automatically generate keywords and alt-text.

### Configuration

```toml
[openai]
api_key = "sk-your-openai-api-key"
model = "gpt-5.2"
rate_limit_ms = 1000      # Delay between API calls
max_tokens = 300          # Max response tokens

# Optional: Background processing
enable_background_analysis = true
background_interval_minutes = 60
background_batch_size = 50
```

### CLI Commands

```bash
# Analyze all images in a gallery
tenrankai analyze-images -g photos

# Analyze specific folder
tenrankai analyze-images -g photos -f "2026-vacation"

# Limit images per run
tenrankai analyze-images -g photos --limit 100

# Preview what would be analyzed
tenrankai analyze-images -g photos --dry-run

# Force re-analyze already processed images
tenrankai analyze-images -g photos --force

# Clear AI-generated data
tenrankai clear-analysis -g photos
tenrankai clear-analysis -g photos -f "folder" --dry-run
```

### What Gets Generated

- **Keywords**: Descriptive tags extracted from image content
- **Alt-text**: Accessibility descriptions for screen readers

Data is stored in image metadata sidecars and displayed in the gallery.

## CLI Tools

### Server Commands

```bash
# Start server
tenrankai serve
tenrankai serve --config custom.toml
tenrankai serve --port 8080 --host 0.0.0.0

# Auto-shutdown (for testing)
tenrankai serve --quit-after 10

# Debug logging
tenrankai serve --log-level debug
```

### User Management

```bash
# Add user
tenrankai user add jane@example.com --display-name "Jane Smith"

# List users
tenrankai user list

# Update user
tenrankai user update jane@example.com --display-name "Jane Doe"

# Remove user
tenrankai user remove jane@example.com
```

### Cache Management

```bash
# View cache coverage report
tenrankai cache report -g photos

# Clean outdated cache files
tenrankai cache cleanup -g photos

# Invalidate specific entries (force regeneration)
tenrankai cache invalidate -g photos -t image -p "IMG_001.jpg"
tenrankai cache invalidate -g photos -t composite -p "folder-path"

# Invalidate all images in a folder (useful after replacing photos)
tenrankai cache invalidate -g photos -t folder -p "2026-vacation"
tenrankai cache invalidate -g photos -t folder -p "2026-vacation" --dry-run

# List cached composite images
tenrankai cache list-composites -g photos
```

Cache invalidation types:
- `image`: Single image (all sizes/formats)
- `composite`: Folder preview composite image
- `folder`: All images in a folder (thumbnails, gallery, medium, large)

### AVIF Debugging

```bash
# Analyze AVIF metadata
tenrankai avif-debug image.avif

# Verbose output
tenrankai avif-debug image.avif --verbose
```

Shows:
- Dimensions and file size
- Color space properties
- HDR detection
- Gain map presence
- ICC profile info

## HEIC/HEIF Support

Tenrankai natively supports HEIC/HEIF images (iPhone photos) with full HDR pipeline:

- **Apple Photos**: Direct support for iPhone HEIC files
- **HDR Preservation**: Gain maps extracted and converted to AVIF format
- **Metadata**: Full EXIF extraction (camera, GPS, dates)
- **Color Profiles**: ICC profiles preserved through processing

HEIC images are automatically converted to web-friendly formats (WebP, AVIF, JPEG) while preserving HDR data when outputting to AVIF.

## Multi-File Image Support

Associate multiple files with a single gallery image for RAW workflows and version management.

### RAW File Association

Place RAW files alongside processed images:

```
photos/
├── IMG_0001.jpg      # Displayed in gallery
├── IMG_0001.dng      # Associated RAW (downloadable)
├── IMG_0002.arw      # Sony RAW
└── IMG_0002.jpg      # Processed version
```

Supported RAW formats: `.dng`, `.arw`, `.crw`, `.cr2`, `.cr3`, `.nef`, `.orf`, `.raf`, `.rw2`, `.pef`, `.srw`

Users with `can_download_raw` permission see a RAW download button.

### Image Versions

Track multiple versions using suffixes or a versions folder:

**Version Suffixes**:
```
photos/
├── IMG_0001.jpg       # Primary (displayed)
├── IMG_0001_v1.jpg    # Previous version
└── IMG_0001_v2.jpg    # Older version
```

**Versions Folder**:
```
photos/
├── IMG_0001.jpg           # Primary (displayed)
└── __versions/
    ├── IMG_0001.jpg       # Previous version (by mod time)
    └── IMG_0001_v1.jpg    # Explicit version
```

Users with `can_see_versions` permission see a version picker to navigate between versions.

### Hidden Folders

Folders prefixed with `__` are hidden from navigation but accessible for internal use:

```
photos/
├── vacation/          # Visible folder
└── __versions/        # Hidden (for version storage)
```

## Inline Content Editing

Edit folder and image descriptions directly in the gallery UI.

Users with `can_edit_content` permission see edit buttons to modify:
- **Folder descriptions**: Title and markdown description
- **Image descriptions**: Title and caption

The editor supports:
- Rich text mode with formatting toolbar
- Raw markdown editing mode
- Bold, italic, headings, lists, quotes, code, links

Changes are saved to the markdown sidecar files (`_folder.md` or `image.jpg.md`).

## Enhanced Metadata Sources

Tenrankai reads metadata from multiple sources with priority:

### 1. Markdown Sidecar (Highest Priority)

Create `IMG_001.jpg.md`:

```markdown
+++
title = "Sunset at Big Sur"
description = "Golden hour magic on the coast"
tags = ["sunset", "landscape", "california"]

# Astrophotography fields
telescope = "Celestron NexStar 8SE"
mount = "EQ6-R Pro"
filters = "Ha, OIII, SII"
total_exposure_hours = 12.5
ra = "05:34:31.94"
dec = "+22:00:52.2"
+++

Extended description with **markdown** formatting.
```

### 2. XMP Sidecar

Adobe Lightroom compatible. Create `IMG_001.jpg.xmp` with standard XMP metadata.

### 3. EXIF Data (Lowest Priority)

Embedded in image files. Automatically extracted for camera, lens, GPS, timestamps.

## Zoom Features

### Desktop: Click-to-Zoom Loupe

With `can_use_zoom` permission:
- Click and hold to activate
- 1.8x magnification using medium image
- Custom cursor indicates availability

With `can_use_tile_zoom` permission:
- Full resolution tile-based zoom
- Requires `[galleries.tiles]` configuration

### Mobile: Pinch-to-Zoom

With `can_use_zoom` permission:
- Native pinch gesture
- Double-tap to quick zoom
- Pan when zoomed
- Fullscreen modal with zoom indicator
- Automatic tile loading at high zoom levels

### Configuration

```toml
[galleries.tiles]
tile_size = 1024

[galleries.permissions.roles.member]
permissions = {
    can_use_zoom = true,       # Basic zoom
    can_use_tile_zoom = true   # Enhanced tile zoom
}

[galleries.pregenerate]
tiles = true  # Pre-generate tiles
```

## Cache Pre-Generation

Pre-generate cache on startup for instant loading:

```toml
[galleries.pregenerate]
formats = { jpeg = true, webp = true, avif = false }
sizes = { thumbnail = true, gallery = true, medium = true, large = false }
tiles = false
```

Features:
- **Parallel processing**: Uses all CPU cores
- **Memory-safe**: Limits concurrent operations
- **Incremental**: Only generates missing files
- **Graceful shutdown**: Clean exit on Ctrl+C
- **Progress logging**: Detailed server output

## Image URL Indexing

Control how images are referenced in URLs:

```toml
[[galleries]]
image_indexing = "filename"  # or "sequence" or "unique_id"
```

| Mode | Example | Use Case |
|------|---------|----------|
| `filename` | `/gallery/image/IMG_001.jpg` | SEO, debugging |
| `sequence` | `/gallery/image/1` | Clean portfolios |
| `unique_id` | `/gallery/image/a3k2x` | Privacy, clients |

`unique_id` generates non-guessable 6-character IDs.

## Hidden Folders

Hide folders from navigation while keeping them accessible:

```markdown
+++
title = "Private Preview"
hidden = true
+++
```

Hidden folders:
- Don't appear in folder listings
- Accessible via direct URL
- Perfect for sharing with select people

## Hide Technical Details

Remove camera/EXIF info per folder:

```markdown
+++
title = "Client Portfolio"
hide_technical_details = true
+++
```

Hides:
- Camera make/model
- Lens information
- Technical settings (ISO, aperture, shutter)
- GPS coordinates

## Image Preloading

Adjacent images are automatically preloaded:
- Next and previous images load in background
- Retina (@2x) versions included
- Navigation feels instant

No configuration required.

## Next Steps

- [API Reference](/docs/09-api) - Build custom integrations
- [Deployment](/docs/06-deployment) - Production best practices
