# Tenrankai Marketing and Documentation Website Project

## Project Overview

This project creates a marketing and documentation website for Tenrankai - a high-performance web-based photo gallery server written in Rust. The website is built using Tenrankai itself and the content is placed in the tenrankai-dot-com directory.

## Current Status: COMPLETED ✅

The website has been successfully transformed from a personal photography site (theatr.us) to a professional marketing and documentation site for Tenrankai. All content has been updated to prominently feature Tenrankai's file-based architecture and SyncThing integration as key selling points.

## What Was Accomplished

### 1. Marketing Pages
- **Homepage**: Professional landing page with hero section, feature grid highlighting file-based architecture and SyncThing support, live gallery demo, and CTAs
- **About Page**: Comprehensive overview emphasizing Tenrankai's "just files and folders" philosophy and SyncThing workflow benefits
- **Features Page**: Detailed feature documentation with "File-Based Architecture" as the primary category, highlighting SyncThing integration and simple deployment
- **Get Involved Page** (formerly Contact): Community engagement with links to GitHub, documentation, and contribution guidelines

### 2. Documentation System
Created a posts-based documentation system at `/docs` with:
- **Quick Start Guide** (`00-quick-start.md`): 5-minute setup guide with SyncThing tips for automatic deployment
- **Installation Guide** (`01-installation.md`): Comprehensive installation instructions
- **Configuration Guide** (`02-configuration.md`): Complete configuration reference including new `approximate_dates_for_public` privacy setting

### 3. Blog System
- Transformed example post into "Introducing Tenrankai" announcement emphasizing the file-based architecture and SyncThing benefits
- Renamed file to `introducing-tenrankai.md`
- Blog accessible at `/blog`

### 4. Branding Updates
- Site title changed from "theatr.us" to "Tenrankai"
- Navigation updated: Features, Demo (Gallery), Docs, Blog, About, Get Involved, GitHub
- Footer updated to reflect open source project with Apache 2.0 license
- Professional dark theme with gradient effects on homepage

### 5. Configuration Files
Created three configuration files:
- **`config.toml`**: Default configuration for the marketing site
- **`config.production.toml`**: Production-optimized with security notes and nginx examples
- **`config.dev.toml`**: Minimal development configuration
- **`README.md`**: Complete setup and deployment guide

## Technical Implementation

### Directory Structure
```
tenrankai-dot-com/
├── config.toml              # Main configuration
├── config.production.toml   # Production example
├── config.dev.toml         # Development config
├── README.md               # Setup guide
├── photos/                 # Demo gallery images
├── posts/
│   ├── blog/              # Blog posts
│   │   └── introducing-tenrankai.md
│   └── docs/              # Documentation
│       ├── 00-quick-start.md
│       ├── 01-installation.md
│       └── 02-configuration.md
├── static/                 # CSS, fonts, etc.
└── templates/
    ├── modules/           # Gallery, posts templates
    ├── pages/            # Page templates
    │   ├── index.html.liquid    # Homepage
    │   ├── about.html.liquid    # About
    │   ├── features.html.liquid # Features (new)
    │   └── contact.html.liquid  # Get Involved
    └── partials/          # Header, footer, etc.
```

### Key Configuration Settings
- **Domain**: tenrankai.com
- **Galleries**: Main demo gallery at `/gallery`
- **Posts Systems**: 
  - Documentation at `/docs` (30-min refresh)
  - Blog at `/blog` (60-min refresh)
- **Pre-generation**: Enabled for demo gallery

### CSS Enhancements
Added to `home.css`:
- Hero section with gradient title effect
- Feature grid with cards
- Responsive button styles
- CTA sections
- Mobile-responsive breakpoints

## Deployment Notes

For production deployment:
1. Use `config.production.toml` as template
2. Generate secure passwords: `openssl rand -base64 32`
3. Set up systemd service
4. Configure nginx reverse proxy
5. Ensure DejaVuSans.ttf is in static directory

## Future Enhancements

Potential additions:
- More documentation guides (API, Templates, Deployment)
- Additional blog posts
- Example showcase galleries
- Performance benchmarks page
- Community contributions section
- Search functionality
- Video tutorials

## Running the Site

From the tenrankai-dot-com directory:
```bash
# Build Tenrankai (from parent directory)
cd ../tenrankai && cargo build --release

# Run the marketing site
cd ../tenrankai-dot-com
../tenrankai/target/release/tenrankai

# Visit http://localhost:3000
```