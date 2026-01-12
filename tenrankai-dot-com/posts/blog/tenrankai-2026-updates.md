+++
title = "Tenrankai 2026 Update: Professional Photography Workflows"
summary = "Announcing major updates including AI-powered image analysis, filmstrip navigation, enhanced metadata support, collaborative features, and advanced privacy controls"
date = "2026-01-12"
+++

# Tenrankai 2026 Update: Professional Photography Workflows

We're excited to announce a major update to Tenrankai that transforms it into a comprehensive platform for professional photography workflows. This release brings over 18 major new features focused on AI-powered analysis, collaboration, metadata management, and privacy control, including the highly requested area-specific commenting capability and AI-powered image analysis.

## AI-Powered Image Analysis

### OpenAI Vision Integration

Tenrankai now integrates with OpenAI's Vision API to automatically analyze your images:

- **Smart Keywords**: AI extracts relevant keywords from image content for better discoverability
- **Accessibility Alt-Text**: Automatically generate WCAG-compliant alt-text for screen readers
- **Batch Processing**: Analyze entire galleries with a single CLI command
- **Incremental Analysis**: Only processes images without existing keywords
- **Background Mode**: Optionally run analysis automatically on new images

### Getting Started with AI Analysis

```bash
# Analyze all images in a gallery
tenrankai analyze-images -g photos

# Preview what would be analyzed
tenrankai analyze-images -g photos --dry-run

# Analyze specific folder with limit
tenrankai analyze-images -g photos -f "2026-vacation" --limit 50

# Clear AI-generated data if needed
tenrankai clear-analysis -g photos
```

Configure in your `config.toml`:

```toml
[openai]
api_key = "sk-your-api-key"
model = "gpt-5.2"
rate_limit_ms = 1000
enable_background_analysis = true  # Auto-analyze new images
```

## Filmstrip Navigation

A new filmstrip-style thumbnail navigation has been added for desktop users:

- **Quick Browsing**: Scroll through thumbnails to jump to any image
- **Current Position**: Active image is highlighted in the strip
- **Keyboard Support**: Works alongside arrow key navigation
- **Desktop Only**: Mobile continues to use swipe gestures for optimal touch experience

## Enhanced Metadata System

### Multi-Source Metadata with Priority Cascade

Tenrankai now reads metadata from multiple sources with intelligent priority:

1. **Markdown frontmatter** (`.jpg.md` or `.md` files) - Highest priority
2. **XMP sidecar files** - Adobe Lightroom compatible
3. **EXIF data** - Lowest priority

This allows you to override incorrect EXIF data, add rich descriptions, and maintain metadata separate from image files. The system even supports specialized fields for astrophotography including telescope, mount, filters, and exposure hours.

### User Metadata Storage

Users with appropriate permissions can now add:
- **Comments** - Discuss images with clients or collaborators
- **Picks** (✓) - Mark favorite images
- **Highlights** (⭐) - Flag images for special attention
- **Tags** - Organize with custom categories

All user metadata is stored in `.toml` sidecar files alongside images, keeping your workflow file-based and version-control friendly.

## Gallery Filter System

The new filter bar allows users to quickly filter galleries by metadata type:
- Show only picked images
- Find images with comments
- Display highlighted selections
- Filter by tags

Filter selections persist in the URL, making it easy to share specific views with clients or team members.

## Area-Specific Comments

One of the most requested features is now here - the ability to comment on specific areas of images:

### Visual Area Selection
- **Click and drag** to select rectangular areas when adding comments
- **Touch support** for mobile devices and tablets
- **Edit capabilities** - add, change, or remove areas when editing comments
- **Visual previews** show highlighted areas in comment threads

### Professional Use Cases
- **Client feedback**: "Please brighten this corner" with exact area selection
- **Quality control**: Mark dust spots or areas needing retouching
- **Photo critique**: Highlight composition elements or technical issues
- **Collaborative editing**: Discuss specific details without ambiguity
- **Education**: Point out examples of good technique or areas for improvement

The area data is stored as percentage-based coordinates, ensuring responsive display across all devices.

## Platform-Optimized Zoom

Tenrankai now offers the best zoom experience for each platform:

### Desktop: Click-to-Zoom Loupe
- **Click and hold** to activate magnifying loupe
- **1.8x magnification** using medium-sized image
- **Tile-based option** (`can_use_tile_zoom`) for full resolution

### Mobile: Pinch-to-Zoom
- **Native pinch gesture** to zoom in/out smoothly
- **Double-tap** to quick zoom at tap location
- **Pan gesture** to navigate around zoomed image
- **Fullscreen modal** with zoom level percentage indicator
- **Automatic tile loading** when zoom exceeds 1.5x
- **Smart navigation** - swipe disabled while zoomed to prevent accidents

Both platforms include image protection features and smooth animations.

## Flexible Image Indexing

Three new URL modes provide different levels of privacy:

1. **Filename** (default): `/gallery/image/vacation/IMG_1234.jpg`
2. **Sequence**: `/gallery/image/vacation/1` - Clean, ordered URLs
3. **Unique ID**: `/gallery/image/vacation/a3k2x` - Non-guessable 6-character IDs

The unique ID mode is perfect for client galleries where you don't want URLs to be predictable.

## React Frontend with TypeScript

The image detail view is now a modern React SPA featuring:
- **Swipe navigation** on mobile devices
- **Keyboard shortcuts** for desktop
- **Smooth transitions** between images
- **Loading states** with 500ms delay
- **Retina support** with automatic 2x image loading

## Enhanced Privacy Controls

### Hide Technical Details

Control camera and technical information visibility per folder:

```markdown
# In _folder.md
+++
hide_technical_details = true
+++
```

Perfect for professional portfolios where you want to focus on the art, not the gear.

### Fine-Grained Permissions

The role-based permission system now includes:
- `can_use_zoom` - Basic loupe zoom (medium image)
- `can_use_tile_zoom` - Enhanced tile-based zoom (full resolution)
- `can_read_metadata` - View user-generated content
- `can_add_comments` - Leave feedback
- `can_set_picks` - Mark favorites
- `can_add_tags` - Organize images

## CLI Enhancements

New and improved command-line tools:
- `analyze-images -g <gallery>` - AI-powered image analysis for keywords and alt-text
- `clear-analysis -g <gallery>` - Remove AI-generated metadata
- `cache report -g <gallery>` - View format coverage analysis
- `cache cleanup -g <gallery>` - Clean up outdated cache files
- `cache invalidate -g <gallery>` - Force regeneration of specific entries
- `cache list-composites -g <gallery>` - List cached composite images
- `user update` - Change display names
- `avif-debug` - Analyze AVIF metadata
- Improved help and command structure

## Configurable Pre-Generation

The new pre-generation system gives you fine-grained control:

```toml
[galleries.pregenerate]
formats = { jpeg = true, webp = true, avif = false }
sizes = { thumbnail = true, gallery = true, medium = true, large = false }
tiles = false  # Requires [galleries.tiles] config
```

Pre-generation now features:
- **Parallel processing** using all CPU cores
- **Incremental generation** - only creates missing files
- **Graceful cancellation** on Ctrl+C
- **Progress logging** in server output

## AWS SES Improvements

SES email now supports the full AWS credential provider chain:
1. Explicit credentials in config
2. Environment variables (`AWS_ACCESS_KEY_ID`, etc.)
3. AWS credentials file (`~/.aws/credentials`)
4. IAM role credentials (EC2, ECS, Lambda)

This makes deployment on AWS infrastructure much simpler - no need to store credentials in config files.

## Developer Experience

- **TypeScript sources** restored in repository
- **Cross-platform npm** scripts for Windows
- **Better error messages** for permission denials
- **Comprehensive tests** for new features

## Performance Improvements

- **FNV hasher** for stable unique IDs
- **Quick-XML** for efficient XMP parsing
- **React Suspense** for better loading states
- **Optimized builds** in both dev and release modes

## Migration Notes

The new features are backwards compatible, but note:
- `copyright_holder` moved from `[app]` to per-gallery configuration
- Old permission fields (`approximate_dates_for_public`, etc.) are deprecated but still work
- New installations should use the role-based permission system

## Getting Started

Update your gallery configuration to enable the new features:

```toml
[[galleries]]
name = "portfolio"
image_indexing = "sequence"  # or "unique_id" for privacy

[galleries.permissions.roles.client]
permissions = {
    can_view = true,
    can_use_zoom = true,
    can_read_metadata = true,
    can_add_comments = true,
    can_set_picks = true
}
```

## Thank You

This release represents months of work focused on professional photography workflows. We're grateful to our community for the feedback and feature requests that shaped this update.

As always, Tenrankai remains committed to the file-based philosophy - no database required, just files and folders. Whether you're managing a personal portfolio or collaborating with clients, these new features make Tenrankai more powerful while keeping it simple.

[Get started with the new features](/docs) or [view the source on GitHub](https://github.com/theatrus/tenrankai).