+++
title = "Gallery Setup"
summary = "Configure galleries, image processing, sizes, and formats"
date = "2026-01-13"
+++

# Gallery Setup

Galleries are the heart of Tenrankai. This guide covers everything you need to configure your image galleries.

## Basic Gallery Configuration

Each gallery is defined in a `[[galleries]]` section:

```toml
[[galleries]]
name = "main"                          # Unique identifier
url_prefix = "/gallery"                # URL path prefix
source_directory = "photos"            # Where your images are
cache_directory = "cache/main"         # Where processed images go
images_per_page = 50                   # Images per page
new_threshold_days = 7                 # Days to mark images as "NEW"
cache_refresh_interval_minutes = 60    # Background refresh interval
```

| Setting | Required | Description |
|---------|----------|-------------|
| `name` | Yes | Unique identifier for the gallery |
| `url_prefix` | Yes | URL path (must start with `/`) |
| `source_directory` | Yes | Path to source images |
| `cache_directory` | Yes | Path for processed images |
| `images_per_page` | No | Pagination (default: 50) |
| `new_threshold_days` | No | Mark recently modified images as NEW |
| `cache_refresh_interval_minutes` | No | Background metadata refresh |

## Image Sizes

Configure the dimensions for each image size:

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

**Size purposes:**
- **thumbnail**: Gallery grid previews
- **gallery_size**: Standard viewing in gallery
- **medium**: Detail view, optional watermarking
- **large**: High-resolution downloads (requires permission)

All sizes automatically generate @2x variants for retina displays.

## Image Quality

Control compression quality per format:

```toml
[[galleries]]
name = "main"
jpeg_quality = 85    # JPEG quality: 1-100 (default: 85)
webp_quality = 85.0  # WebP quality: 0.0-100.0 (default: 85.0)
```

Higher values = better quality but larger files. 85 is a good balance.

## Image Format Support

Tenrankai automatically handles format conversion:

| Source Format | Output Formats | Notes |
|---------------|----------------|-------|
| JPEG | JPEG, WebP | WebP for supported browsers |
| PNG | PNG | Preserves transparency |
| AVIF | AVIF, WebP, JPEG | Full HDR support with gain maps |

**Content negotiation**: Browsers that support WebP receive WebP; others get JPEG. AVIF sources are served as AVIF to capable browsers, with fallback to WebP/JPEG.

### HDR and Color Profiles

Tenrankai preserves color accuracy:

- **ICC profiles**: Maintained through all processing
- **Display P3**: Wide gamut colors preserved
- **HDR AVIF**: Gain maps preserved for tone mapping
- **10-bit encoding**: HDR content encoded at proper bit depth

## Copyright Watermarking

Add watermarks to medium-sized images:

```toml
[[galleries]]
name = "portfolio"
copyright_holder = "Jane Photographer"
```

When set:
- Watermark appears on medium-sized images only
- Text color automatically adjusts for background (black or white)
- Color profiles preserved through watermarking
- Requires `DejaVuSans.ttf` in your static directory

## Image URL Modes

Control how images are referenced in URLs:

```toml
[[galleries]]
name = "main"
image_indexing = "filename"  # Options: filename, sequence, unique_id
```

| Mode | Example URL | Use Case |
|------|-------------|----------|
| `filename` | `/gallery/image/IMG_1234.jpg` | SEO-friendly, debugging |
| `sequence` | `/gallery/image/1` | Clean URLs, portfolios |
| `unique_id` | `/gallery/image/a3k2x` | Privacy, client galleries |

**unique_id** generates 6-character IDs that can't be guessed, preventing URL enumeration.

## Gallery Preview

Configure how gallery previews are generated (for homepage widgets, etc.):

```toml
[galleries.preview]
max_images = 6       # Total images to show
max_depth = 3        # How deep to traverse folders
max_per_folder = 2   # Max images from each folder
```

## Custom Templates

Override default templates per gallery:

```toml
[[galleries]]
name = "main"
gallery_template = "modules/gallery.html.liquid"
image_detail_template = "modules/image_detail.html.liquid"
```

## Cache Pre-Generation

Pre-generate image cache on server startup for instant loading:

```toml
[galleries.pregenerate]
formats = { jpeg = true, webp = true, avif = false }
sizes = { thumbnail = true, gallery = true, medium = true, large = false }
tiles = false
```

**Benefits:**
- Parallel processing using all CPU cores
- Memory-safe with concurrency limits
- Incremental - only generates missing files
- Graceful shutdown on Ctrl+C

**When to use:**
- Production deployments with stable content
- After adding many new images
- Before launching a new gallery

## High-Resolution Tile Zoom

Enable tile-based zoom for detailed image exploration:

```toml
[galleries.tiles]
tile_size = 1024  # Pixels per tile

[galleries.pregenerate]
tiles = true  # Pre-generate tiles
```

Tiles allow users to zoom into full-resolution details without downloading the entire large image. Users need the `can_use_tile_zoom` permission.

## Multiple Galleries

Run multiple independent galleries from one Tenrankai instance:

```toml
# Public portfolio
[[galleries]]
name = "portfolio"
url_prefix = "/"
source_directory = "/srv/photos/portfolio"
cache_directory = "/srv/cache/portfolio"
copyright_holder = "Studio Name"
image_indexing = "sequence"

# Private client gallery
[[galleries]]
name = "clients"
url_prefix = "/clients"
source_directory = "/srv/photos/clients"
cache_directory = "/srv/cache/clients"
image_indexing = "unique_id"

# Family photos
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "/srv/photos/family"
cache_directory = "/srv/cache/family"
```

Each gallery has:
- Independent URL namespace
- Separate cache directories
- Individual permission settings
- Custom templates (optional)

## Folder Organization

Organize images in folders for navigation:

```
photos/
├── _folder.md              # Root folder description
├── 2026/
│   ├── _folder.md          # Year description
│   ├── january/
│   │   ├── _folder.md
│   │   ├── IMG_001.jpg
│   │   └── IMG_002.jpg
│   └── february/
└── portfolio/
    ├── _folder.md
    ├── headshots/
    └── landscapes/
```

### Folder Descriptions

Add `_folder.md` to customize folder display:

```markdown
+++
title = "Summer Vacation 2026"
hidden = false
hide_technical_details = false
+++

Photos from our amazing trip to the coast.
```

### Hidden Folders

Hide folders from navigation while keeping them accessible:

```markdown
+++
title = "Private Preview"
hidden = true
+++
```

Hidden folders:
- Don't appear in folder listings
- Are accessible via direct URL
- Can be shared with specific people

## Complete Gallery Example

```toml
[[galleries]]
name = "portfolio"
url_prefix = "/"
source_directory = "/srv/photos/portfolio"
cache_directory = "/srv/cache/portfolio"

# Display settings
images_per_page = 24
new_threshold_days = 30

# Quality settings
jpeg_quality = 90
webp_quality = 90.0
copyright_holder = "Professional Photography Inc."

# Privacy
image_indexing = "sequence"

# Templates
gallery_template = "modules/gallery.html.liquid"
image_detail_template = "modules/image_detail.html.liquid"

# Image sizes
[galleries.thumbnail]
width = 400
height = 400

[galleries.gallery_size]
width = 1000
height = 1000

[galleries.medium]
width = 1600
height = 1600

[galleries.large]
width = 2400
height = 2400

# Preview widget
[galleries.preview]
max_images = 8
max_depth = 2
max_per_folder = 3

# Pre-generation
[galleries.pregenerate]
formats = { jpeg = true, webp = true, avif = false }
sizes = { thumbnail = true, gallery = true, medium = true, large = false }
tiles = false

# Enhanced zoom
[galleries.tiles]
tile_size = 1024

# Permissions (see Permissions Guide for details)
[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "member"

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true, can_use_zoom = true }

[galleries.permissions.roles.member]
name = "Member"
permissions = { can_view = true, can_use_zoom = true, can_download_medium = true }
```

## Next Steps

- [Authentication](/docs/04-authentication) - Set up user accounts
- [Permissions](/docs/05-permissions) - Control gallery access
- [Advanced Features](/docs/08-advanced) - S3 storage, AI analysis
