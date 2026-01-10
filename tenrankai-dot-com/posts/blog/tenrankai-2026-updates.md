+++
title = "Tenrankai 2026 Update: Professional Photography Workflows"
summary = "Announcing major updates including enhanced metadata support, collaborative features, and advanced privacy controls"
date = "2026-01-09"
+++

# Tenrankai 2026 Update: Professional Photography Workflows

We're excited to announce a major update to Tenrankai that transforms it into a comprehensive platform for professional photography workflows. This release brings over 16 major new features focused on collaboration, metadata management, and privacy control, including the highly requested area-specific commenting capability.

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

## Click-to-Zoom Loupe

Professional photographers can now examine fine details with the new click-to-zoom feature:
- **2x magnification** with click-and-hold
- **Smooth animations** for seamless exploration
- **Permission-based** - Control who can use zoom
- **Image protection** - Makes saving images harder

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
- `can_use_zoom` - Control zoom access
- `can_read_metadata` - View user-generated content
- `can_add_comments` - Leave feedback
- `can_set_picks` - Mark favorites
- `can_add_tags` - Organize images

## CLI Enhancements

New and improved command-line tools:
- `user update` - Change display names
- `avif-debug` - Analyze AVIF metadata
- Improved help and command structure

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