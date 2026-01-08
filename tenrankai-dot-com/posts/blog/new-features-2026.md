+++
title = "Tenrankai's Latest Features: Enhanced Privacy, Security, and Flexibility"
date = "2026-01-08"
slug = "new-features-2026"
description = "Discover the latest features in Tenrankai including flexible image indexing, enhanced privacy controls, WebAuthn support, and more."
+++

We're excited to announce several powerful new features in Tenrankai that make it even more flexible, secure, and privacy-focused. These updates reflect our commitment to providing a photo gallery server that respects both photographers and viewers while maintaining the simplicity of our file-based approach.

## Image Indexing Modes: Control Your URLs

One of our most requested features is now available - flexible image indexing modes. You can now choose how your images are referenced in URLs:

### Three Indexing Modes

1. **Filename Mode** (default): Traditional URLs that expose actual filenames
   - Example: `/gallery/image/vacation/sunset.jpg`
   - Best for: Public galleries where filenames don't matter

2. **Sequence Mode**: URLs use sequential numbers within folders
   - Example: `/gallery/image/vacation/1`
   - Best for: Organized collections where order matters

3. **Unique ID Mode**: URLs use short base36 identifiers
   - Example: `/gallery/image/vacation/a3k2x`
   - Best for: Privacy-conscious galleries, preventing filename enumeration

Configure it per gallery in your `config.toml`:
```toml
[[galleries]]
image_indexing = "unique_id"  # or "filename" or "sequence"
```

## Enhanced Privacy Controls

### Hide Technical Details Per Folder

Sometimes you want to share photos without revealing technical metadata. Now you can hide camera information, GPS data, and other technical details on a per-folder basis.

In any `_folder.md` file:
```toml
+++
hide_technical_details = true
+++
```

This hides:
- Image metadata (dimensions, file size, capture date)
- Camera information (make, model, settings)
- Location data (GPS coordinates, maps)

### Approximate Dates for Public Viewers

Building on our existing `approximate_dates_for_public` feature, non-authenticated users see only month/year instead of exact capture dates, adding another layer of privacy for personal galleries.

## Modern Authentication with WebAuthn

Tenrankai now supports WebAuthn/Passkeys for passwordless authentication:

- **Biometric login**: Use fingerprint, face recognition, or hardware security keys
- **Cross-device sync**: Passkeys sync across your devices
- **Enhanced security**: No passwords to steal or phish
- **Multiple passkeys**: Register multiple devices per account

## Folder-Level Access Control

Control who can access specific folders with fine-grained permissions:

```toml
+++
require_auth = true
allowed_users = ["family@example.com", "friend@example.com"]
+++
```

Perfect for:
- Family photo albums
- Client galleries
- Private collections within public galleries

## Cascading Directories

Tenrankai now supports multiple template and static file directories, making it easier to customize your gallery without modifying core files:

```toml
[templates]
directories = ["templates-custom", "templates"]

[static_files]
directories = ["static-custom", "static"]
```

Files in the first directory take precedence, allowing clean customization and easier updates.

## AVIF with Smart Fallbacks

For those using AVIF images (with HDR and gain maps), Tenrankai now intelligently serves fallback formats:

- Original AVIF images are always served as AVIF (preserving HDR)
- Resized images automatically fall back to WebP or JPEG for incompatible browsers
- No configuration needed - it just works!

## React-Powered Gallery Interface

The gallery now uses a modern React + Vite frontend, providing:
- Faster navigation and image loading
- Smooth animations and transitions
- Better mobile experience
- Improved accessibility

## What's Next?

These features are just the beginning. We're continuing to focus on:
- Privacy-first features
- Performance improvements
- Better mobile experience
- Enhanced SyncThing integration

## Get Started

Update to the latest version of Tenrankai to access all these features:

```bash
git pull
cargo build --release
```

Check out our updated [configuration documentation](/docs/configuration) for detailed setup instructions.

---

Have feedback or feature requests? [Get involved](/contact) with the Tenrankai community!