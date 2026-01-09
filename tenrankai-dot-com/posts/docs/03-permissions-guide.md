+++
title = "Permissions & Privacy Guide"
summary = "Understanding Tenrankai's role-based permission system"
date = "2026-01-09"
+++

# Permissions & Privacy Guide

Tenrankai features a powerful role-based access control (RBAC) system that gives you fine-grained control over who can see and do what in your galleries.

## Overview

The permission system allows you to:

- Define custom roles with specific permissions
- Assign users to roles
- Override permissions at the folder level
- Control privacy at a granular level

## Understanding Permissions

### Configuration Structure

Permissions are configured within each gallery's `[galleries.permissions]` section:

```toml
[[galleries]]
name = "family"

[galleries.permissions]
# Role for unauthenticated visitors
public_role = "viewer"

# Default role for authenticated users
default_authenticated_role = "member"

# Define custom roles
[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = { can_view = true }

[galleries.permissions.roles.member]
name = "Member"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true
}

# Assign users to specific roles
[[galleries.permissions.user_roles]]
username = "grandma"
roles = ["member"]
```

### Available Permissions

#### Viewing Permissions
- **`can_view`** - Basic permission to see images (automatically includes thumbnail and gallery size downloads)

#### Privacy Permissions
- **`can_see_exact_dates`** - See exact capture date/time vs approximate month/year
- **`can_see_location`** - View GPS coordinates and location maps
- **`can_see_technical_details`** - Access camera, lens, and EXIF data

#### Download Permissions
- **`can_download_medium`** - Download medium resolution images (1200px)

Note: Thumbnail and gallery size downloads are automatically included with the `can_view` permission.
- **`can_download_large`** - Download large resolution images (1600px)
- **`can_download_original`** - Access original, unmodified files

#### Interactive Permissions
- **`can_use_zoom`** - Use zoom functionality to view images in detail
- **`can_read_metadata`** - Read user-generated content (comments, picks, tags)

#### Content Management Permissions
- **`can_add_comments`** - Add comments to images
- **`can_edit_own_comments`** - Edit your own comments
- **`can_delete_own_comments`** - Delete your own comments
- **`can_set_picks`** - Mark images as picks/favorites
- **`can_add_tags`** - Add tags to images

#### Moderation Permissions
- **`can_edit_any_comments`** - Edit any user's comments
- **`can_delete_any_comments`** - Delete any user's comments

#### Special Permissions
- **`owner_access`** - Full access to everything (overrides all other permissions)

## Common Permission Patterns

### Public Portfolio

For a professional portfolio where you want to showcase your work:

```toml
[[galleries]]
name = "portfolio"

[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
# Show camera info for credibility
# No location data or high-res downloads
permissions = {
    can_view = true,
    can_see_technical_details = true
}
```

### Family Gallery

For family photos with privacy protection:

```toml
[[galleries]]
name = "family"

[galleries.permissions]
public_role = "limited"
default_authenticated_role = "family_member"

# Public sees limited info with approximate dates
[galleries.permissions.roles.limited]
name = "Limited Viewer"
# No exact dates - shows "October 2026" instead
# No location - protects home addresses
permissions = {
    can_view = true
}

# Family members see everything
[galleries.permissions.roles.family_member]
name = "Family Member"
permissions = {
    can_view = true,
    can_see_exact_dates = true,      # Full timestamps
    can_see_location = true,         # GPS data
    can_see_technical_details = true,
    can_download_medium = true,
    can_download_large = true,
    can_download_original = true,
    can_use_zoom = true,             # Zoom for detailed viewing
    can_read_metadata = true,        # Read comments and tags
    can_add_comments = true,         # Comment on family photos
    can_set_picks = true,            # Mark favorite photos
    can_add_tags = true              # Tag family members
}

# Assign family members
[[galleries.permissions.user_roles]]
username = "mom"
roles = ["family_member"]

[[galleries.permissions.user_roles]]
username = "dad"
roles = ["family_member"]
```

### Client Gallery

For professional client work:

```toml
[[galleries]]
name = "clients"

[galleries.permissions]
public_role = "preview"
default_authenticated_role = "preview"

# Minimal public access
[galleries.permissions.roles.preview]
name = "Preview"
permissions = { can_view = true }  # Can see images but not browse

# Client access with downloads
[galleries.permissions.roles.client]
name = "Client"
# No technical details or location
permissions = {
    can_view = true,
    can_download_medium = true,
    can_download_original = true
}

# Assign specific clients
[[galleries.permissions.user_roles]]
username = "client"
roles = ["client"]
```

### Private Gallery

For completely private galleries:

```toml
[[galleries]]
name = "private"

[galleries.permissions]
# No public_role = no public access at all
default_authenticated_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true
}
```

## Folder-Level Permissions

Override gallery-wide permissions for specific folders using `_folder.md` files:

### Hide Sensitive Folders

Create `photos/private/_folder.md`:
```markdown
+++
title = "Private Collection"

[permissions]
# Remove all public access
public_role = "none"

# Only family members can view
default_authenticated_role = "family"

[permissions.roles.family]
name = "Family"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true,
    can_download_original = true
}
+++

These photos are only for family members.
```

### Restrict Folder Access

Create `photos/client-review/_folder.md`:
```markdown
+++
title = "Client Review"

[permissions]
public_role = "none"
default_authenticated_role = "preview"

[permissions.roles.preview]
name = "Preview"
# No downloads until approved
permissions = {
    can_view = true
}

[permissions.roles.client]
name = "Client"
permissions = {
    can_view = true,
    can_download_original = true
}
+++

Images pending client approval.
```

## Privacy Features in Action

### Date Privacy

When `can_see_exact_dates` is **not** granted:
- Public sees: "October 2026"
- No specific dates or times shown
- Protects daily routines and schedules

When `can_see_exact_dates` is granted:
- Full timestamp: "October 15, 2026 at 3:45 PM"
- Sorting and chronological organization preserved

### Location Privacy

When `can_see_location` is **not** granted:
- No GPS coordinates displayed
- No maps shown
- Location metadata completely hidden
- Protects home addresses and frequently visited places

When `can_see_location` is granted:
- Full GPS coordinates available
- Interactive maps (if configured)
- Location-based organization possible

### Technical Details

When `can_see_technical_details` is **not** granted:
- No camera or lens information
- No exposure settings (ISO, aperture, shutter speed)
- No color profile or technical metadata

When `can_see_technical_details` is granted:
- Full EXIF data displayed
- Camera and lens models
- All technical photography information

## Best Practices

### 1. Start Restrictive

Begin with minimal permissions and add as needed:

```toml
[galleries.permissions.roles.public]
name = "Public"
permissions = { can_view = true }
```

### 2. Consider Privacy Implications
- **Dates**: Can reveal routines and schedules
- **Locations**: Can expose home addresses
- **Technical details**: May include sensitive metadata

### 3. Test Permission Combinations
- Log in as different users to verify access
- Check that public view shows appropriate information
- Ensure downloads work as expected

### 4. Document Your Choices

Add comments explaining your permission decisions:

```toml
[galleries.permissions.roles.public]
name = "Public"
# No exact dates - protects children's schedules
# No location - protects home address
permissions = {
    can_view = true
}
```

## Common Use Cases

### School Event Photos

```toml
[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "parent"

[galleries.permissions.roles.viewer]
name = "Viewer"
# No exact dates or location for child safety
permissions = {
    can_view = true
}

[galleries.permissions.roles.parent]
name = "Parent"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_download_original = true
}

[[galleries.permissions.user_roles]]
username = "parent"
roles = ["parent"]
```

### Wedding Photography

```toml
[galleries.permissions]
public_role = "guest"
default_authenticated_role = "guest"

# Guests can view
[galleries.permissions.roles.guest]
name = "Guest"
permissions = {
    can_view = true,
    can_see_exact_dates = true  # Event date is public
}

# Couple gets everything
[galleries.permissions.roles.client]
name = "Client"
permissions = {
    can_view = true,
    can_see_exact_dates = true,
    can_see_location = true,
    can_see_technical_details = true,
    can_download_medium = true,
    can_download_large = true,
    can_download_original = true
}

[[galleries.permissions.user_roles]]
username = "bride"
roles = ["client"]

[[galleries.permissions.user_roles]]
username = "groom"
roles = ["client"]
```

### Artist Portfolio

```toml
[galleries.permissions]
public_role = "visitor"

[galleries.permissions.roles.visitor]
name = "Visitor"
permissions = {
    can_view = true,
    can_see_technical_details = true  # Shows professional capability
}
```

And hide work-in-progress with `photos/drafts/_folder.md`:
```markdown
+++
title = "Work in Progress"

[permissions]
public_role = "none"  # Hidden from public
+++

Unfinished pieces.
```

## Migration from Old System

If you're upgrading from an older version of Tenrankai:

### Old Configuration
```toml
approximate_dates_for_public = true
hide_location_from_public = true
# In _folder.md:
hide_technical_details = true
```

### New Configuration
```toml
[galleries.permissions]
public_role = "viewer"

[galleries.permissions.roles.viewer]
name = "Viewer"
# Note: No can_see_exact_dates, can_see_location, or can_see_technical_details
permissions = {
    can_view = true
}
```

## Troubleshooting

### "Access Denied" Errors
1. Check role assignment for the user
2. Verify gallery and folder permissions
3. Ensure `can_view` is granted at minimum
4. Check permission inheritance

### Images Not Showing
- Verify `can_view` permission is granted
- Check folder-level overrides in `_folder.md`
- Ensure user is assigned to correct role

### Downloads Failing
- Check specific download permissions
- Verify size-specific permissions match request
- Ensure base `can_view` is also granted

### Dates Showing Wrong Format
- Check `can_see_exact_dates` permission
- Without it, only month/year is shown
- This is by design for privacy

## Next Steps

- [Configuration Guide](/docs/02-configuration) - Full configuration reference
- [Authentication Setup](/docs/07-authentication) - Setting up user accounts
- [Template Customization](/docs/05-templates) - Customize permission-based displays