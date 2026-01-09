# Tenrankai Marketing & Documentation Website

This directory contains the content and configuration for the official Tenrankai marketing and documentation website.

## Directory Structure

```
tenrankai-dot-com/
├── config.toml              # Default configuration
├── config.dev.toml          # Development configuration
├── config.production.toml   # Production configuration example
├── photos/                  # Demo gallery images
├── posts/
│   ├── blog/               # Blog posts about Tenrankai
│   └── docs/               # Documentation posts
├── static/                  # Static assets (CSS, fonts, etc.)
└── templates/               # Liquid templates
    ├── modules/            # Module-specific templates
    ├── pages/              # Page templates
    └── partials/           # Reusable components
```

## Quick Start

1. **Install Tenrankai** (from the parent directory):
   ```bash
   cd ../tenrankai
   cargo build --release
   ```

2. **Run the website**:
   ```bash
   # From this directory (tenrankai-dot-com)
   ../tenrankai/target/release/tenrankai
   
   # Or with a specific config
   ../tenrankai/target/release/tenrankai --config config.dev.toml
   ```

3. **Visit the site**: Open http://localhost:3000

## Configuration Files

### `config.toml` (Default)
Standard configuration for the marketing site with:
- Demo gallery at `/gallery`
- Documentation at `/docs`
- Blog at `/blog`
- Pre-generation enabled for better performance

### `config.dev.toml` (Development)
Minimal configuration for quick development:
- Reduced image quality for faster processing
- Simplified settings
- No pre-generation

### `config.production.toml` (Production Example)
Production-ready configuration with:
- Absolute paths for file locations
- Security reminders
- Multiple showcase galleries
- Nginx configuration examples
- Systemd service hints

## Deployment

For production deployment:

1. Copy `config.production.toml` to `config.toml`
2. Update all paths to match your server
3. Generate secure cookie secret:
   ```bash
   openssl rand -base64 32  # For cookie_secret
   ```
4. Update `base_url` to your domain
5. Set up as a systemd service (see config.production.toml comments)
6. Configure nginx as reverse proxy

## Adding Content

### Gallery Images
Place images in subdirectories under `photos/`:
```bash
photos/
├── landscapes/
│   ├── _folder.md      # Folder description
│   └── sunset.jpg
└── portraits/
    └── portrait.jpg
```

### Documentation
Create markdown files in `posts/docs/` with TOML frontmatter:
```markdown
+++
title = "Your Guide Title"
summary = "Brief description"
date = "2026-01-09"
+++

# Your Guide Title

Content here...
```

### Blog Posts
Similar to docs, but in `posts/blog/`:
```markdown
+++
title = "Announcing Feature X"
summary = "We've added amazing new capabilities"
date = "2026-01-09"
+++

Content here...
```

## Customization

### Templates
- Edit templates in `templates/` to change layout
- Page templates are in `templates/pages/`
- Reusable components in `templates/partials/`

### Styling
- Main styles: `static/style.css`
- Page-specific styles: `static/home.css`, etc.
- Dark theme with CSS variables for easy customization

### Navigation
Edit `templates/partials/_header.html.liquid` to modify navigation

## Development Tips

1. **Live Reload**: Posts and galleries refresh automatically based on config intervals
2. **Debug Mode**: Run with `--log-level debug` for detailed logging
3. **Quick Test**: Use `--quit-after 10` to auto-shutdown after 10 seconds

## Support

- GitHub Issues: https://github.com/theatrus/tenrankai/issues
- Documentation: http://localhost:3000/docs (when running)