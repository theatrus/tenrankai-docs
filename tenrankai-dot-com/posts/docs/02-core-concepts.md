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
├── config.toml              # Bootstrap configuration (server, email)
├── config.d/                # Site configuration (ConfigStorage)
│   └── sites/
│       └── default/
│           ├── site.toml        # Site settings
│           ├── permissions.toml # Roles and access control
│           ├── galleries/
│           │   └── main.toml    # Gallery configurations
│           └── posts/
│               ├── blog.toml    # Blog configuration
│               └── docs.toml    # Documentation configuration
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

## Two-Tier Configuration

Tenrankai uses a two-tier configuration system:

1. **Bootstrap config** (`config.toml`): Server settings, email, OpenAI - static settings that rarely change
2. **ConfigStorage** (`config.d/`): Site-specific configuration (galleries, posts, permissions) that can be managed via CLI or Admin UI

```bash
# Use default config.toml
tenrankai serve

# Use a specific config file
tenrankai serve --config production.toml
```

### Quick Setup with CLI

The easiest way to get started is using the CLI:

```bash
# Initialize ConfigStorage directory with a default site
tenrankai config init config.d

# Add galleries and posts to your site
tenrankai config add-gallery photos --site default --source photos --url-prefix /gallery
tenrankai config add-posts blog --site default --source posts/blog --url-prefix /blog
```

### Bootstrap Configuration (config.toml)

The bootstrap config contains server-level settings:

```toml
[server]
host = "127.0.0.1"
port = 3000

[app]
name = "My Gallery"
config_storage = "config.d"  # Path to ConfigStorage directory

# Optional: Email for authentication
# [email]
# provider = "null"
# from_address = "noreply@example.com"
```

### Site Configuration (ConfigStorage)

Site-specific configuration lives in `config.d/sites/default/`:

**site.toml** - Site settings:
```toml
hostnames = ["localhost", "photos.example.com"]
templates = ["templates"]
static_files = ["static"]
base_url = "https://photos.example.com"
cookie_secret = "generate-with-openssl-rand-base64-32"
# user_database = "users.toml"  # Enables authentication
```

**galleries/main.toml** - Gallery configuration:
```toml
name = "main"
url_prefix = "/gallery"
source_directory = "photos"
cache_directory = "cache/main"
```

**permissions.toml** - Roles and access control:
```toml
public_role = "viewer"
[roles.viewer]
permissions = { can_view = true }
```

### Legacy Single-File Configuration

For simpler deployments, you can still use a single config.toml with everything inline:

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

This format continues to work and is automatically converted to a default site internally.

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

The `[app]` section in the bootstrap config contains global settings:

```toml
[app]
name = "My Photo Gallery"
log_level = "info"
config_storage = "config.d"  # Path to ConfigStorage directory
```

| Setting | Required | Description |
|---------|----------|-------------|
| `name` | Yes | Site name (appears in titles, emails) |
| `log_level` | No | `trace`, `debug`, `info`, `warn`, `error` (default: `info`) |
| `config_storage` | No | Path to ConfigStorage directory (recommended) |

Site-specific settings like `cookie_secret`, `base_url`, and `user_database` are configured in `config.d/sites/default/site.toml`.

### Generating a Cookie Secret

```bash
# Generate a secure random secret
openssl rand -base64 32
```

### CLI Configuration Commands

Manage your configuration without editing files:

```bash
# Initialize ConfigStorage
tenrankai config init config.d

# List and manage sites
tenrankai config list-sites
tenrankai config add-site photos --hostname photos.example.com

# Manage galleries
tenrankai config list-galleries default
tenrankai config add-gallery portfolio --site default --source portfolio --url-prefix /portfolio

# Manage posts
tenrankai config list-posts default
tenrankai config add-posts blog --site default --source posts/blog --url-prefix /blog
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

## Admin UI

Tenrankai includes a built-in administration interface at `/_admin/` for managing your site without editing configuration files.

**Features:**
- **User Management**: Create, delete, and invite users
- **Gallery Viewer**: See gallery configurations and permissions
- **Role Viewer**: View built-in roles and their permissions
- **Site Configuration**: Manage site settings via API

**Access Requirements:**
- Must be authenticated
- Must have `owner_access` permission in any gallery

The Admin UI is a React-based single-page application that communicates with the Admin API.

## Next Steps

Now that you understand the basics:

1. [Gallery Setup](/docs/03-galleries) - Configure image processing, sizes, and formats
2. [Authentication](/docs/04-authentication) - Set up user accounts and login
3. [Permissions](/docs/05-permissions) - Control who can see what
4. [Advanced Features](/docs/08-advanced) - Admin UI, S3 storage, multi-site hosting
