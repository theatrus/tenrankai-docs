+++
title = "Permissions"
summary = "Role-based access control for galleries and folders"
date = "2026-01-13"
+++

# Permissions

Tenrankai uses role-based access control (RBAC) to manage who can view, download, and interact with your galleries.

## Quick Start

Add permissions to any gallery:

```toml
[[galleries]]
name = "family"

[galleries.permissions]
public_role = "viewer"                    # Unauthenticated visitors
default_authenticated_role = "member"     # Logged-in users

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true }

[galleries.permissions.roles.member]
name = "Member"
permissions = { can_view = true, can_download_medium = true }
```

## How Permissions Work

1. **Roles** define sets of permissions
2. **Users** are assigned to roles
3. **Folders** can override gallery permissions
4. Permissions cascade: parent restrictions apply to children

## Available Permissions

### Viewing

| Permission | Description |
|------------|-------------|
| `can_view` | View images (includes thumbnails) |

### Privacy

| Permission | Description |
|------------|-------------|
| `can_see_exact_dates` | See exact dates (vs "January 2026") |
| `can_see_location` | See GPS coordinates and maps |
| `can_see_technical_details` | See camera, lens, EXIF data |

### Downloads

| Permission | Description |
|------------|-------------|
| `can_download_medium` | Download medium resolution |
| `can_download_large` | Download large resolution |
| `can_download_original` | Download original files |
| `can_download_raw` | Download associated RAW files |
| `can_download_gallery` | Download folders as ZIP archives |

Note: Thumbnails and gallery-size images are included with `can_view`.

**ZIP Downloads**: Users with `can_download_gallery` see a "Download All" button in gallery view. Downloads include all images in the folder (and subfolders) as a streaming ZIP archive.

**RAW Downloads**: Users with `can_download_raw` see a RAW download button when images have associated RAW files (.dng, .arw, .cr2, etc.).

### Interactive

| Permission | Description |
|------------|-------------|
| `can_use_zoom` | Click-to-zoom loupe (medium image) |
| `can_use_tile_zoom` | High-resolution tile zoom |
| `can_read_metadata` | See comments, picks, tags |
| `can_see_versions` | See and navigate to previous image versions |

**Image Versions**: Users with `can_see_versions` see a version picker when images have previous versions available.

### Content Management

| Permission | Description |
|------------|-------------|
| `can_add_comments` | Add comments to images |
| `can_edit_own_comments` | Edit your own comments |
| `can_delete_own_comments` | Delete your own comments |
| `can_set_picks` | Mark images as picks/favorites |
| `can_add_tags` | Add tags to images |
| `can_edit_content` | Edit folder and image descriptions |

**Inline Editing**: Users with `can_edit_content` can edit titles and descriptions directly in the gallery UI using a rich text editor.

### Image Management

| Permission | Description |
|------------|-------------|
| `can_manage_images` | Upload, move, copy, hide, and delete images |

**Web-Based Image Management**: Users with `can_manage_images` see a toolbar in gallery view with options to upload images, create folders, and perform batch operations on selected images (move, copy, hide, unhide, delete). See [Web-Based Image Management](#web-based-image-management) below.

### Moderation

| Permission | Description |
|------------|-------------|
| `can_edit_any_comments` | Edit any user's comments |
| `can_delete_any_comments` | Delete any user's comments |
| `owner_access` | Full access to everything |

## Defining Roles

### Basic Role

```toml
[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true }
```

### Role with Multiple Permissions

```toml
[galleries.permissions.roles.member]
name = "Member"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_download_medium = true,
    can_use_zoom = true,
    can_read_metadata = true
}
```

### Role Inheritance

Roles can inherit from other roles:

```toml
[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true, can_use_zoom = true }

[galleries.permissions.roles.member]
name = "Member"
inherits = "viewer"  # Gets all viewer permissions
permissions = { can_download_medium = true, can_add_comments = true }
```

## Assigning Users to Roles

```toml
[[galleries.permissions.user_roles]]
username = "jane@example.com"
roles = ["admin"]

[[galleries.permissions.user_roles]]
username = "client@company.com"
roles = ["client"]
```

Users can have multiple roles - permissions are combined.

## Common Patterns

### Public Portfolio

Show work publicly, hide personal details:

```toml
[galleries.permissions]
public_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = {
    can_view = true,
    can_see_technical_details = true,  # Show camera gear
    can_use_zoom = true
}
# Note: No can_see_exact_dates or can_see_location
```

### Family Gallery

Public sees limited info, family sees everything:

```toml
[galleries.permissions]
public_role = "limited"
default_authenticated_role = "limited"

[galleries.permissions.roles.limited]
name = "Limited"
permissions = { can_view = true }

[galleries.permissions.roles.family]
name = "Family"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true,
    can_download_original = true,
    can_add_comments = true,
    can_set_picks = true
}

[[galleries.permissions.user_roles]]
username = "mom@family.com"
roles = ["family"]

[[galleries.permissions.user_roles]]
username = "dad@family.com"
roles = ["family"]
```

### Client Review Gallery

Clients can view and comment, photographer has full access:

```toml
[galleries.permissions]
public_role = "none"  # No public access
default_authenticated_role = "client"

[galleries.permissions.roles.client]
name = "Client"
permissions = {
    can_view = true,
    can_use_zoom = true,
    can_read_metadata = true,
    can_add_comments = true,
    can_set_picks = true
}

[galleries.permissions.roles.photographer]
name = "Photographer"
permissions = { owner_access = true }

[[galleries.permissions.user_roles]]
username = "me@studio.com"
roles = ["photographer"]

[[galleries.permissions.user_roles]]
username = "client@company.com"
roles = ["client"]
```

## Folder-Level Permissions

Override gallery permissions for specific folders using `_folder.md`:

### Hide a Folder

```markdown
+++
title = "Private Photos"

[permissions]
public_role = "none"
+++
```

### Restrict to Specific Users

```markdown
+++
title = "VIP Preview"

[permissions]
public_role = "none"
default_authenticated_role = "none"

[permissions.roles.vip]
name = "VIP Client"
permissions = { can_view = true, can_download_large = true }

[[permissions.user_roles]]
username = "vip@company.com"
roles = ["vip"]
+++
```

### Remove Technical Details

```markdown
+++
title = "Client Portfolio"
hide_technical_details = true
+++

Professional photos without camera information.
```

## User Metadata

When users have appropriate permissions, they can add metadata to images:

### Picks and Highlights

- **Picks** (✓): Mark favorites
- **Highlights** (⭐): Flag for attention

### Comments

Users can comment on images, including selecting specific areas:

```toml
# Stored in IMG_001.jpg.toml
[[comments]]
user = "client@company.com"
comment = "Love the lighting here!"
timestamp = "2026-01-15T14:30:00Z"

# Area-specific comment
[[comments]]
user = "photographer@studio.com"
comment = "Need to fix this corner"
timestamp = "2026-01-15T15:00:00Z"
[comments.image_area]
x = 10.5      # Percentage from left
y = 80.2      # Percentage from top
width = 15.0
height = 10.0
```

### Gallery Badges

Images with metadata show badges in the gallery:
- ✓ Picked
- ⭐ Highlighted
- 💬 Has comments
- 🏷️ Has tags

### Filtering

Users with `can_read_metadata` can filter by:
- Picks only
- Highlighted only
- Has comments
- Has tags

Filters persist in URL: `/gallery?filter=picks,comments`

## Web-Based Image Management

Users with `can_manage_images` permission can manage gallery content directly through the web interface, providing an alternative to file-based management with SyncThing.

### Upload Images

Click the **+ New** button and select **Upload Images** to open the upload modal:

- **Drag and drop** files or click to browse
- **Resumable uploads** using the TUS protocol (survives network interruptions)
- **Large file support** up to 500MB per file
- **Smart sidecar handling**: Automatically associates `.xmp`, `.md`, and RAW files with their images
- **Progress tracking** with per-file and overall progress bars

Supported formats: JPEG, PNG, WebP, AVIF, HEIC/HEIF, plus RAW formats (DNG, ARW, CR2, CR3, NEF, ORF, RAF, RW2, PEF, SRW).

### Create Folders

Click **+ New** → **New Folder** to create a folder in the current location.

### Batch Operations

Select images by clicking the checkbox overlay, then use the management toolbar:

| Action | Description |
|--------|-------------|
| **Move** | Move selected images to another folder |
| **Copy** | Copy selected images to another folder |
| **Hide** | Hide selected images from gallery view |
| **Unhide** | Unhide previously hidden images |
| **Delete** | Permanently delete selected images |

The folder picker modal shows the gallery structure for Move and Copy operations.

### SyncThing vs Web Upload

Both approaches work well together:

| Feature | SyncThing | Web Upload |
|---------|-----------|------------|
| Bulk sync from desktop | ✅ Best choice | Limited |
| Quick upload from browser | Limited | ✅ Best choice |
| Auto-sync between devices | ✅ | — |
| Remote upload (no local access) | — | ✅ |
| Metadata editing | Via sidecar files | Via UI |
| Works offline | ✅ | — |

**Recommendation**: Use SyncThing for desktop workflows and bulk operations, web upload for quick additions and remote management.

## Troubleshooting

### "Permission Denied" Errors

1. Check role has required permission
2. Verify user is assigned to role
3. Check folder-level overrides
4. Ensure `can_view` is set (required for all access)

### Users Can't See Dates/Location

Add the appropriate permission:
```toml
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true
}
```

### Downloads Not Working

Check download permissions match requested size:
- Medium: `can_download_medium`
- Large: `can_download_large`
- Original: `can_download_original`

## Next Steps

- [Deployment](/docs/06-deployment) - Production security
- [Theming](/docs/07-theming) - Customize appearance
- [Advanced Features](/docs/08-advanced) - S3, AI analysis
