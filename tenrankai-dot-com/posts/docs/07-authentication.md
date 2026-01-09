+++
title = "Authentication Guide"
summary = "Configure user authentication, WebAuthn/Passkeys, and gallery access control"
date = "2026-01-09"
+++

# Authentication Guide

Tenrankai provides modern authentication with WebAuthn/Passkey support and fine-grained access control using a role-based permission system.

## Authentication Overview

Tenrankai supports:

- **Email-based Magic Links** - Passwordless authentication via email
- **WebAuthn/Passkeys** - Biometric and security key authentication
- **Role-Based Permissions** - Fine-grained access control with custom roles
- **Gallery Access Control** - Per-gallery permission configuration

## Enabling Authentication

### 1. Basic Setup

Enable authentication in your `config.toml`:

```toml
[app]
name = "My Gallery"
base_url = "https://yourdomain.com"  # Required for WebAuthn
user_database = "users.db"            # Enables authentication
cookie_secret = "your-32-character-secret-key-here"  # Generate with: openssl rand -base64 32
```

When `user_database` is set:
- Authentication system is enabled
- WebAuthn/Passkeys are automatically configured
- User profiles are accessible at `/_login/profile`

### 2. Email Configuration

Configure an email provider for magic link authentication:

```toml
[email]
# For development - logs emails to console
provider = "null"
from_address = "noreply@yourdomain.com"

# For production with Amazon SES
# provider = "ses"
# from_address = "noreply@yourdomain.com"
# from_name = "My Gallery"  # Optional
# region = "us-east-1"      # Optional, uses AWS credential chain
```

Note: SMTP provider is planned but not yet implemented.

### 3. Create Initial Admin User

Use the CLI to create your first admin user:

```bash
tenrankai user add admin@example.com --display-name "Admin User"
```

## WebAuthn/Passkey Setup

WebAuthn enables passwordless authentication using:

- **Biometric authentication** - Touch ID, Face ID, Windows Hello
- **Security keys** - YubiKey, Google Titan, etc.
- **Cross-device passkeys** - Synced via iCloud Keychain, Google Password Manager

### How It Works

1. WebAuthn is automatically enabled when `user_database` is configured
2. The system uses your `base_url` hostname as the Relying Party ID
3. Your `app.name` is used as the Relying Party name
4. No additional configuration needed!

### User Registration Flow

1. User requests login at `/_login`
2. Enters email address
3. Receives magic link via email
4. Clicks link to authenticate
5. Can then register passkeys at `/_login/profile`

### Managing Passkeys

Users can manage passkeys at `/_login/profile`:
- View all registered passkeys
- Register new passkeys (biometric or security key)
- Delete existing passkeys
- See last used timestamps

## Role-Based Permissions

Tenrankai uses a flexible role-based permission system instead of simple access lists.

### Understanding Roles

Each gallery can define custom roles with specific permissions:

```toml
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "photos/family"

[galleries.permissions]
# Define which role unauthenticated users get
public_role = "viewer"

# Define which role authenticated users get by default
default_authenticated_role = "family_member"

# Define custom roles with specific permissions
[galleries.permissions.roles.viewer]
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    "can_download_thumbnail"
]

[galleries.permissions.roles.family_member]
permissions = [
    "can_view",
    "can_browse_folders", 
    "can_see_metadata",
    "can_see_exact_dates",
    "can_see_location",
    "can_see_technical_details",
    "can_download_thumbnail",
    "can_download_gallery_size",
    "can_download_medium",
    "can_download_large",
    "can_download_original"
]
```

### Available Permissions

- **can_view** - View images in the gallery
- **can_browse_folders** - Navigate folder structure
- **can_see_metadata** - View basic image information
- **can_see_exact_dates** - See exact timestamps (vs approximate dates)
- **can_see_location** - View GPS coordinates and maps
- **can_see_technical_details** - See camera/EXIF data
- **can_download_thumbnail** - Download small images
- **can_download_gallery_size** - Download medium quality
- **can_download_medium** - Download larger images
- **can_download_large** - Download high resolution
- **can_download_original** - Access original files

### Assigning Users to Roles

Assign specific users to custom roles:

```toml
[[galleries.permissions.user_roles]]
email = "grandma@family.com"
role = "family_member"

[[galleries.permissions.user_roles]]
email = "friend@example.com"
role = "viewer"
```

## Gallery Access Patterns

### 1. Public Gallery

Anyone can view, but only see basic information:

```toml
[[galleries]]
name = "portfolio"

[galleries.permissions]
public_role = "viewer"
default_authenticated_role = "viewer"

[galleries.permissions.roles.viewer]
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    "can_see_technical_details",  # Show camera info
    "can_download_thumbnail",
    "can_download_gallery_size"
]
```

### 2. Private Gallery

No public access, authenticated users only:

```toml
[[galleries]]
name = "private"

[galleries.permissions]
# No public_role defined = no public access
default_authenticated_role = "member"

[galleries.permissions.roles.member]
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    "can_see_exact_dates",
    "can_see_location",
    "can_download_thumbnail",
    "can_download_gallery_size",
    "can_download_original"
]
```

### 3. Client Gallery

Limited public preview, full access for clients:

```toml
[[galleries]]
name = "clients"

[galleries.permissions]
public_role = "preview"
default_authenticated_role = "preview"

[galleries.permissions.roles.preview]
permissions = ["can_view"]  # View only, no downloads

[galleries.permissions.roles.client]
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata",
    "can_download_thumbnail",
    "can_download_gallery_size",
    "can_download_medium",
    "can_download_original"
]

# Assign specific client
[[galleries.permissions.user_roles]]
email = "client@company.com"
role = "client"
```

## User Management

### CLI Commands

```bash
# Add a new user
tenrankai user add user@example.com --display-name "User Name"

# List all users
tenrankai user list

# Remove a user
tenrankai user remove user@example.com
```

### User Database Structure

Users are stored in the SQLite database specified by `user_database`. The system manages:
- User ID and email
- Display name
- Authentication timestamps
- WebAuthn credentials
- Role assignments

## Authentication Flow

### 1. Email Login Flow

1. User visits `/_login`
2. Enters email address
3. System sends magic link
4. User clicks link in email
5. Session created, redirected to original destination

### 2. Passkey Login Flow

1. User visits `/_login`
2. Clicks "Sign in with Passkey"
3. Browser prompts for biometric/security key
4. Direct authentication without email
5. Session created, redirected

### 3. Session Management

Sessions are managed via secure cookies:
- Signed with `cookie_secret`
- HTTP-only and secure flags in production
- Expire on browser close by default

## Authentication Endpoints

Tenrankai provides these authentication endpoints:

- `/_login` - Login page
- `/_login/profile` - User profile and passkey management
- `/_login/logout` - Logout endpoint
- `/_login/verify` - Magic link verification
- `/_login/api/webauthn/*` - WebAuthn API endpoints

## Security Best Practices

### 1. Configuration Security

```toml
[app]
# Generate strong secret
cookie_secret = "use-output-from: openssl rand -base64 32"

# Use HTTPS in production (required for WebAuthn)
base_url = "https://yourdomain.com"
```

### 2. Permission Design

- Start with minimal permissions and add as needed
- Use role inheritance to avoid repetition
- Regularly audit user role assignments
- Consider privacy implications of each permission

### 3. WebAuthn Security

- Passkeys are phishing-resistant
- Private keys never leave the device
- Support for attestation (device verification)
- Users should register multiple passkeys as backup

## Troubleshooting

### Common Issues

1. **"WebAuthn not available"**:
   - Ensure HTTPS is enabled (required for WebAuthn)
   - Check browser supports WebAuthn
   - Verify `base_url` is correctly set

2. **"Email not sent"**:
   - Check email provider configuration
   - Verify `from_address` is valid
   - For development, use `provider = "null"` to log emails

3. **"Access denied"**:
   - Check user's role assignment
   - Verify permission configuration
   - Ensure user is authenticated

4. **"Invalid session"**:
   - Check `cookie_secret` hasn't changed
   - Verify cookies are enabled
   - Clear browser cookies and try again

### Debug Mode

Enable debug logging to troubleshoot:

```toml
[app]
log_level = "debug"
```

This will log:
- Authentication attempts
- Permission checks
- Email sending
- WebAuthn operations

## Migration Notes

### From Old Permission System

If you were using the old system with `hide_location_from_public` or `require_auth`:

**Old:**
```toml
hide_location_from_public = true
approximate_dates_for_public = true
```

**New:**
```toml
[galleries.permissions]
public_role = "viewer"

[galleries.permissions.roles.viewer]
permissions = [
    "can_view",
    "can_browse_folders",
    "can_see_metadata"
    # Note: No can_see_location or can_see_exact_dates
]
```

## API Authentication

The API recognizes authenticated sessions:

```bash
# Login and save cookies
curl -c cookies.txt -X POST http://localhost:3000/_login \
  -d "email=user@example.com"

# Use session for API calls
curl -b cookies.txt http://localhost:3000/api/galleries/main
```

## Next Steps

- [Configuration Reference](/docs/02-configuration) - Full configuration options
- [Permissions Guide](/docs/03-permissions-guide) - Detailed permission examples
- [API Documentation](/docs/04-api) - API authentication details