+++
title = "Authentication Guide"
summary = "Configure user authentication, WebAuthn/Passkeys, and gallery access control"
date = "2025-08-26"
+++

# Authentication Guide

Tenrankai provides multiple authentication methods including traditional passwords, modern WebAuthn/Passkeys, and fine-grained gallery access control.

## Authentication Overview

Tenrankai supports:

- **Password Authentication** - Traditional username/password login
- **WebAuthn/Passkeys** - Passwordless authentication using biometrics or security keys
- **Gallery Access Control** - Restrict galleries to specific users
- **Folder-Level Permissions** - Control access to individual folders

## Enabling Authentication

### 1. Basic Setup

Enable authentication in your `config.toml`:

```toml
[app]
name = "My Gallery"
user_database = "users.toml"  # Enable authentication
cookie_secret = "your-32-character-secret-key-here"
```

### 2. Create Users Database

Create `users.toml` with initial users:

```toml
[[users]]
username = "admin"
password_hash = "$argon2id$v=19$m=19456,t=2,p=1$..."  # Generated hash
email = "admin@example.com"
is_admin = true

[[users]]
username = "family"
password_hash = "$argon2id$v=19$m=19456,t=2,p=1$..."
email = "family@example.com"
is_admin = false
```

### 3. Generate Password Hashes

Use the built-in password hasher:

```bash
tenrankai hash-password
# Enter password when prompted
# Copy the generated hash to users.toml
```

## WebAuthn/Passkey Setup

WebAuthn enables passwordless authentication using:

- **Biometric authentication** - Fingerprint, Face ID, Windows Hello
- **Security keys** - YubiKey, Google Titan, etc.
- **Platform authenticators** - Built-in device authentication

### 1. Enable WebAuthn

WebAuthn is automatically enabled when authentication is configured. Users can register passkeys from their profile page.

### 2. User Registration Flow

1. User logs in with password initially
2. Navigates to profile page (`/_login/profile`)
3. Clicks "Register New Passkey"
4. Follows browser prompts for biometric or security key
5. Passkey is saved to their account

### 3. Login with Passkey

Once registered, users can:

1. Click "Sign in with Passkey" on login page
2. Browser prompts for biometric or security key
3. User is authenticated without password

### 4. Security Considerations

- Passkeys are tied to the domain (origin)
- Each passkey is unique per device
- Users should register multiple passkeys as backup
- Passkeys cannot be phished or reused

## Gallery Access Control

### 1. Public Galleries

By default, galleries are public:

```toml
[[galleries]]
name = "public"
url_prefix = "/gallery"
source_directory = "photos/public"
# No user_access_list = public access
```

### 2. Restricted Galleries

Limit gallery access to specific users:

```toml
[[galleries]]
name = "family"
url_prefix = "/family"
source_directory = "photos/family"
user_access_list = ["admin@example.com", "family@example.com"]
```

### 3. Admin-Only Galleries

Create admin-only galleries:

```toml
[[galleries]]
name = "admin"
url_prefix = "/admin-gallery"
source_directory = "photos/admin"
user_access_list = ["admin@example.com"]
```

## User Management

### 1. User Profile Structure

Users in `users.toml` have these fields:

```toml
[[users]]
username = "johndoe"                    # Login username
password_hash = "$argon2id$..."         # Argon2 password hash
email = "john@example.com"              # Email (used for access lists)
is_admin = false                        # Admin privileges
webauthn_credentials = []               # Registered passkeys (auto-managed)
```

### 2. Adding Users

```bash
# Generate password hash
tenrankai hash-password

# Add to users.toml
[[users]]
username = "newuser"
password_hash = "paste-generated-hash-here"
email = "newuser@example.com"
is_admin = false
```

### 3. Modifying Users

Edit `users.toml` directly:

- Change `is_admin` to grant/revoke admin access
- Update `email` to change gallery access
- Remove `[[users]]` block to delete user
- Clear `webauthn_credentials = []` to reset passkeys

### 4. User Self-Service

Users can manage their own accounts at `/_login/profile`:

- View registered passkeys
- Register new passkeys
- Remove existing passkeys
- View account information

## Authentication Flow

### 1. Login Process

1. User visits protected resource
2. Redirected to `/_login`
3. Enters username/password or uses passkey
4. Session cookie created
5. Redirected back to original resource

### 2. Session Management

```toml
[app]
# Session configuration
cookie_secret = "32-character-secret-key"
# Sessions expire after browser close by default
# Or configure explicit timeout (in seconds)
# session_timeout = 86400  # 24 hours
```

### 3. Logout

Users can logout by:
- Visiting `/_login/logout`
- Clearing browser cookies
- Session expiration

## Advanced Configuration

### 1. Email Providers

Configure email for notifications:

```toml
[email]
provider = "smtp"  # or "null" for development

[email.smtp]
server = "smtp.gmail.com"
port = 587
username = "your-email@gmail.com"
password = "your-app-password"
from = "Tenrankai <noreply@example.com>"
```

For development, use null provider:

```toml
[email]
provider = "null"  # Logs emails to console
```

### 2. Authentication Paths

Tenrankai uses these authentication endpoints:

- `/_login` - Login page
- `/_login/logout` - Logout endpoint
- `/_login/profile` - User profile and passkey management
- `/_login/passkey/register` - WebAuthn registration API
- `/_login/passkey/authenticate` - WebAuthn authentication API

### 3. Custom Login Page

Customize the login page by editing `templates/modules/login.html.liquid`:

```liquid
<div class="login-container">
    <h1>{{ app_name }} Login</h1>
    
    <!-- Password login form -->
    <form method="post" action="/_login">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Sign In</button>
    </form>
    
    <!-- WebAuthn login -->
    <div class="passkey-login">
        <button id="passkey-signin">Sign in with Passkey</button>
    </div>
</div>
```

## Security Best Practices

### 1. Password Requirements

While Tenrankai doesn't enforce password policies, consider:

- Minimum 12 characters
- Mix of letters, numbers, symbols
- Unique per user
- Regular rotation for high-security deployments

### 2. Session Security

```toml
[app]
# Use long, random secret
cookie_secret = "generated-32-character-random-string"

# Enable HTTPS-only cookies in production
# secure_cookies = true  # Set when using HTTPS
```

### 3. Access Control Patterns

**Least Privilege**:
```toml
# Default: no access
# Explicitly grant access per gallery
user_access_list = ["specific@user.com"]
```

**Role-Based Access**:
```toml
# Create galleries for different roles
[[galleries]]
name = "public"
# No user_access_list

[[galleries]]
name = "members"
user_access_list = ["member1@example.com", "member2@example.com"]

[[galleries]]
name = "premium"
user_access_list = ["premium1@example.com", "admin@example.com"]
```

### 4. WebAuthn Security

- Passkeys are cryptographically secure
- Private keys never leave the device
- Resistant to phishing attacks
- Support for attestation (device verification)

## Troubleshooting

### Common Issues

1. **"Invalid username or password"**:
   - Verify username exists in users.toml
   - Check password hash is correct
   - Ensure users.toml is readable

2. **WebAuthn registration fails**:
   - Ensure HTTPS is enabled (required for WebAuthn)
   - Check browser compatibility
   - Verify domain matches configuration

3. **Session expires immediately**:
   - Check cookie_secret is set
   - Verify system time is correct
   - Ensure cookies are enabled

4. **Gallery access denied**:
   - Verify user email in access list
   - Check email case sensitivity
   - Ensure user is logged in

### Debug Authentication

Enable debug logging:

```toml
[app]
log_level = "debug"
```

Check logs for:
- Authentication attempts
- Session creation/validation
- Access control decisions
- WebAuthn operations

## Migration Guide

### From Basic Auth

If migrating from HTTP Basic Auth:

1. Create users.toml with same usernames
2. Generate password hashes
3. Update nginx/apache configuration
4. Remove basic auth headers

### Adding Authentication to Existing Site

1. Create users.toml with admin user
2. Add `user_database = "users.toml"` to config
3. Restart Tenrankai
4. Login and add additional users
5. Configure gallery access lists as needed

## API Authentication

The REST API supports authentication via:

1. **Session cookies** - From web login
2. **HTTP Basic Auth** - Using password directly

```bash
# With session cookie
curl -b "session=cookie-value" http://localhost:3000/api/v1/galleries

# With Basic Auth  
curl -u "username:password" http://localhost:3000/api/v1/galleries
```

## Next Steps

- [Configuration Reference](/docs/02-configuration) - Full authentication options
- [API Documentation](/docs/04-api) - Authentication endpoints
- [Template Customization](/docs/05-templates) - Customize login pages