+++
title = "Core Concepts"
summary = "Understanding Tenrankai's file-based architecture and basic configuration"
date = "2026-01-13"
+++

# Core Concepts

Before diving into detailed configuration, it's important to understand how Tenrankai works. This guide covers the fundamental concepts that make Tenrankai unique.

## File-Based Philosophy

Tenrankai operates entirely on files and folders - no database required. This means:

- **Drop files to publish**: Add images to a folder, they appear in your gallery
- **Edit files to update**: Change a markdown file, your content updates
- **Delete files to remove**: Remove an image, it's gone from the gallery
- **Version control friendly**: Track all changes with git
- **Easy backups**: Just copy your folders

This approach works perfectly with file synchronization tools like [SyncThing](https://syncthing.net/), allowing you to edit content on any device and have it automatically deployed.

## Directory Structure

A typical Tenrankai site looks like this:

```
my-gallery/
├── config.toml              # Main configuration
├── users.toml               # User database (if authentication enabled)
├── templates/               # Liquid templates
│   ├── pages/              # Full page templates
│   ├── modules/            # Reusable components
│   └── partials/           # Shared fragments
├── static/                  # CSS, JavaScript, fonts, images
├── photos/                  # Your gallery images
│   ├── 2026/
│   │   ├── vacation/
│   │   │   ├── IMG_001.jpg
│   │   │   ├── IMG_001.jpg.md    # Optional metadata
│   │   │   └── _folder.md        # Folder description
│   │   └── portraits/
│   └── _folder.md
├── posts/                   # Markdown content
│   ├── blog/               # Blog posts
│   └── docs/               # Documentation
└── cache/                   # Generated images (auto-created)
```

## Configuration File

Tenrankai uses TOML format for configuration. By default, it looks for `config.toml` in the current directory:

```bash
# Use default config.toml
tenrankai serve

# Use a specific config file
tenrankai serve --config production.toml
```

### Minimal Configuration

Here's the simplest working configuration:

```toml
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Gallery"
cookie_secret = "change-this-to-a-random-string"

[templates]
directories = ["templates"]

[static_files]
directories = ["static"]

[[galleries]]
name = "photos"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache"
```

## Server Configuration

The `[server]` section controls network settings:

```toml
[server]
host = "127.0.0.1"  # IP address to bind to
port = 3000         # Port number
```

| Setting | Description | Common Values |
|---------|-------------|---------------|
| `host` | IP address to listen on | `127.0.0.1` (local only), `0.0.0.0` (all interfaces) |
| `port` | Port number | `3000` (dev), `8080` (behind proxy) |

For production, bind to `127.0.0.1` and use a reverse proxy (nginx, Caddy) for HTTPS.

## Application Configuration

The `[app]` section contains global settings:

```toml
[app]
name = "My Photo Gallery"
log_level = "info"
cookie_secret = "generate-with-openssl-rand-base64-32"
base_url = "https://photos.example.com"
user_database = "users.toml"  # Enables authentication
```

| Setting | Required | Description |
|---------|----------|-------------|
| `name` | Yes | Site name (appears in titles, emails) |
| `log_level` | No | `trace`, `debug`, `info`, `warn`, `error` (default: `info`) |
| `cookie_secret` | Yes | Secret for signing cookies (min 32 chars recommended) |
| `base_url` | No* | Full URL of your site (* Required for email login) |
| `user_database` | No | Path to user database file (enables authentication) |

### Generating a Cookie Secret

```bash
# Generate a secure random secret
openssl rand -base64 32
```

## Templates and Static Files

Templates and static files support cascading directories for easy customization:

```toml
[templates]
directories = ["templates-custom", "templates"]

[static_files]
directories = ["static-custom", "static"]
```

**How cascading works:**
1. Tenrankai looks for each file in directories left-to-right
2. First match wins
3. Override specific files without copying everything

This lets you customize individual templates or CSS files while keeping the defaults for everything else.

## Galleries

Galleries are the core of Tenrankai. Each gallery is an independent collection of images with its own URL, settings, and permissions.

```toml
[[galleries]]
name = "main"                    # Unique identifier
url_prefix = "/gallery"          # URL path
source_directory = "photos"      # Where images are stored
cache_directory = "cache/main"   # Where processed images go
```

You can have multiple galleries with different settings:

```toml
[[galleries]]
name = "portfolio"
url_prefix = "/"
source_directory = "portfolio"
cache_directory = "cache/portfolio"

[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "family-photos"
cache_directory = "cache/family"
```

See [Gallery Setup](/docs/03-galleries) for complete gallery configuration.

## Posts (Blog/Documentation)

Posts are markdown files that become pages on your site:

```toml
[[posts]]
name = "blog"
source_directory = "posts/blog"
url_prefix = "/blog"
posts_per_page = 10
refresh_interval_minutes = 30

[[posts]]
name = "docs"
source_directory = "posts/docs"
url_prefix = "/docs"
posts_per_page = 20
```

### Post Format

Posts use TOML frontmatter:

```markdown
+++
title = "My First Post"
summary = "A brief description"
date = "2026-01-15"
+++

# My First Post

Content goes here in **markdown** format.
```

Posts are sorted by date (newest first) and automatically paginated.

## Image Metadata

Tenrankai reads image metadata from multiple sources:

1. **Markdown sidecar files** (highest priority)
   - `IMG_001.jpg.md` or `IMG_001.md`
   - TOML frontmatter + markdown description

2. **XMP sidecar files**
   - `IMG_001.jpg.xmp`
   - Adobe Lightroom compatible

3. **EXIF data** (lowest priority)
   - Embedded in the image file
   - Camera, lens, GPS, timestamps

Example markdown sidecar (`vacation/beach.jpg.md`):

```markdown
+++
title = "Sunset at the Beach"
description = "Golden hour at Santa Monica"
tags = ["sunset", "beach", "california"]
+++

Extended description with **markdown** formatting.
```

## Folder Descriptions

Add `_folder.md` to any folder to provide a title and description:

```markdown
+++
title = "Summer Vacation 2026"
hidden = false
+++

Photos from our trip to California.
```

| Setting | Description |
|---------|-------------|
| `title` | Display name for the folder |
| `hidden` | If `true`, folder is accessible but not listed |
| `hide_technical_details` | If `true`, hides camera/EXIF info |
| `[permissions]` | Folder-specific access control |

## Caching

Tenrankai automatically caches processed images (resized, watermarked, converted). The cache:

- Is created automatically in the configured `cache_directory`
- Persists across restarts
- Can be pre-generated on startup
- Supports both local filesystem and S3 storage

You generally don't need to manage the cache manually, but CLI commands are available:

```bash
# View cache coverage report
tenrankai cache report -g photos

# Clean outdated cache files
tenrankai cache cleanup -g photos
```

## Next Steps

Now that you understand the basics:

1. [Gallery Setup](/docs/03-galleries) - Configure image processing, sizes, and formats
2. [Authentication](/docs/04-authentication) - Set up user accounts and login
3. [Permissions](/docs/05-permissions) - Control who can see what
