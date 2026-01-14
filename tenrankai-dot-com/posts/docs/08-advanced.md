+++
title = "Advanced Features"
summary = "S3 storage, AI image analysis, CLI tools, and power user features"
date = "2026-01-13"
+++

# Advanced Features

This guide covers Tenrankai's advanced features for power users and cloud deployments.

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

# List cached composite images
tenrankai cache list-composites -g photos
```

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
