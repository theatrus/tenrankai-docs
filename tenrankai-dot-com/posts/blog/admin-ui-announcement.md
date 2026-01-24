+++
title = "Introducing the Admin UI and ConfigStorage"
summary = "Manage your Tenrankai galleries with a modern web interface and flexible configuration system"
date = "2026-01-23"
+++

# Introducing the Admin UI and ConfigStorage

We're excited to announce two major features that make managing Tenrankai galleries easier than ever: the Admin UI and ConfigStorage system.

## Admin UI: Visual Gallery Management

Tenrankai now includes a built-in web administration interface at `/_admin/`. This React-based dashboard lets you manage your galleries without touching configuration files.

### User Management

The Admin UI provides complete user management capabilities:

- **View all users**: See registered accounts with their display names and email addresses
- **Create new users**: Add users directly from the interface
- **Send invitations**: Generate login invitation emails with 72-hour expiry
- **Delete users**: Remove accounts when needed

### Gallery & Permission Viewer

Get a clear overview of your gallery configurations:

- See all configured galleries and their settings
- View role assignments and permission configurations
- Understand who has access to what
- Browse permission groups organized by category (viewing, downloads, metadata, etc.)

### Access Requirements

To use the Admin UI, you need:
1. An authenticated session
2. `owner_access` permission in any gallery

Simply navigate to `/_admin/` after logging in with an admin account.

## ConfigStorage: Flexible Configuration

The new ConfigStorage system separates your configuration into a directory-based structure that's easier to manage and version control.

### Two-Tier Configuration

Tenrankai now uses a two-tier approach:

1. **Bootstrap config** (`config.toml`): Server settings, email configuration, OpenAI integration
2. **ConfigStorage** (`config.d/`): Site-specific settings managed via CLI or Admin API

### Directory Structure

```
config.d/
  sites/
    default/
      site.toml              # Site settings
      permissions.toml       # Roles and access control
      galleries/
        main.toml            # Gallery configuration
        portfolio.toml
      posts/
        blog.toml            # Posts configuration
```

### CLI Configuration Commands

New commands make setup fast:

```bash
# Initialize ConfigStorage
tenrankai config init config.d

# Add a gallery
tenrankai config add-gallery photos --site default \
  --source photos --url-prefix /gallery

# Add a blog
tenrankai config add-posts blog --site default \
  --source posts/blog --url-prefix /blog
```

### Benefits

- **Version control friendly**: Track configuration changes in git
- **Multi-site support**: Each site has its own configuration namespace
- **Hot reloading**: Update configuration without restarting the server
- **API-driven**: Manage configuration programmatically via the Admin API

## Backward Compatibility

Your existing single-file `config.toml` configurations continue to work. Tenrankai automatically converts them to the internal format. Migrate at your own pace.

## Getting Started

1. Update to the latest Tenrankai release
2. Initialize ConfigStorage: `tenrankai config init config.d`
3. Update your `config.toml` to reference it: `config_storage = "config.d"`
4. Create an admin user with `owner_access` permission
5. Access the Admin UI at `/_admin/`

Check out the updated [Core Concepts](/docs/02-core-concepts) and [Advanced Features](/docs/08-advanced) documentation for complete details.

## What's Next

We're continuing to expand the Admin UI with more features:
- Gallery configuration editing
- Role management interface
- Permission assignment UI
- Site configuration management

Stay tuned for more updates!
