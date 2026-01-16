+++
title = "Authentication"
summary = "Set up user accounts, email login, and WebAuthn passkeys"
date = "2026-01-13"
+++

# Authentication

Tenrankai supports modern passwordless authentication with email magic links and WebAuthn passkeys.

## Enabling Authentication

Add these settings to enable authentication:

```toml
[app]
name = "My Gallery"
base_url = "https://photos.example.com"  # Required for login links
user_database = "users.toml"              # Enables authentication
cookie_secret = "generate-with-openssl-rand-base64-32"
```

## User Storage Backends

Tenrankai supports multiple storage backends for user data. Configure via URL-style paths:

### TOML File (Default)

Simple file-based storage, perfect for single-server deployments:

```toml
[app]
user_database = "users.toml"
```

### SQLite

Local database with better concurrency. Ideal for medium deployments:

```toml
[app]
user_database = "sqlite:///var/data/users.db"
# Or relative path
user_database = "sqlite://users.db"
```

### PostgreSQL

For production deployments with existing database infrastructure:

```toml
[app]
user_database = "postgresql://user:password@localhost/tenrankai"
```

### DynamoDB

Serverless option for AWS deployments:

```toml
[app]
user_database = "dynamodb://users-table?region=us-east-1"
```

### Multi-Site Isolation

SQL and DynamoDB backends automatically scope users by site ID, enabling secure multi-tenant deployments where each site has isolated user accounts.

### Migration Between Backends

Export and import users between backends:

```bash
# Export from TOML
tenrankai user export --database users.toml --output users.json

# Import to SQLite
tenrankai user import --database sqlite://users.db --input users.json
```

## Email Configuration

Configure an email provider to send login links:

### Development (Null Provider)

For testing, use the null provider which logs emails to console:

```toml
[email]
provider = "null"
from_address = "noreply@example.com"
```

### Production (Amazon SES)

For production, use Amazon SES:

```toml
[email]
provider = "ses"
from_address = "noreply@photos.example.com"
from_name = "Photo Gallery"
region = "us-east-1"  # Optional
```

AWS credentials are discovered automatically via:
1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. AWS credentials file (`~/.aws/credentials`)
3. IAM role (EC2, ECS, Lambda)

## User Management

### Adding Users

Use the CLI to create users:

```bash
# Add a user
tenrankai user add jane@example.com --display-name "Jane Smith"

# List all users
tenrankai user list

# Update display name
tenrankai user update jane@example.com --display-name "Jane Doe"

# Remove a user
tenrankai user remove jane@example.com
```

### User Database Format

Users are stored in `users.toml`:

```toml
[users.jane]
username = "jane@example.com"
email = "jane@example.com"
display_name = "Jane Smith"
created = "2026-01-15T10:00:00Z"

[[users.jane.passkeys]]
id = "..."
public_key = "..."
created = "2026-01-15T10:05:00Z"
name = "iPhone"
```

## Login Flow

### Email Magic Links

1. User visits `/_login`
2. Enters their email address
3. Receives email with login link
4. Clicks link to authenticate
5. Session cookie is created (7-day expiry)

### WebAuthn/Passkeys

After email login, users can register passkeys:

1. User logs in via email
2. System prompts to register a passkey
3. User authenticates with biometrics/security key
4. Passkey is stored for future logins

Supported methods:
- **Touch ID / Face ID** (macOS, iOS)
- **Windows Hello** (Windows)
- **Fingerprint sensors** (Android, laptops)
- **Hardware security keys** (YubiKey, etc.)

### Managing Passkeys

Users manage passkeys at `/_login/profile`:
- View registered passkeys
- Remove passkeys
- Add new passkeys
- See creation dates

## Security Features

### Rate Limiting

Login attempts are rate-limited:
- 5 attempts per email per 5 minutes
- Prevents brute force attacks
- Automatic cleanup of old rate limits

### Token Expiration

- Login email tokens: 10 minutes
- Session cookies: 7 days
- Tokens are single-use

### Session Security

- HTTPOnly cookies (not accessible to JavaScript)
- Signed cookies (tamper-proof)
- Secure flag in production (HTTPS only)

## WebAuthn Configuration

WebAuthn is automatically configured from your app settings:

```toml
[app]
name = "My Photo Gallery"                  # RP Name shown during registration
base_url = "https://photos.example.com"    # RP ID = hostname (photos.example.com)
user_database = "users.toml"
```

Requirements:
- `base_url` must be HTTPS (or localhost for development)
- Hostname becomes the Relying Party ID
- Works on any subdomain of the RP ID

## Integration with Permissions

Authentication enables the permission system:

```toml
[galleries.permissions]
public_role = "viewer"                    # Unauthenticated users
default_authenticated_role = "member"      # Logged-in users

[[galleries.permissions.user_roles]]
username = "jane@example.com"
roles = ["admin"]
```

See [Permissions](/docs/05-permissions) for complete access control documentation.

## Troubleshooting

### Login Links Not Arriving

1. Check email provider configuration
2. Verify `from_address` is authorized in SES
3. Check spam folder
4. For development, check console output (null provider)

### WebAuthn Not Working

1. Ensure `base_url` uses HTTPS
2. Check browser supports WebAuthn
3. Verify domain matches `base_url`
4. Check browser console for errors

### Session Expired

- Default session is 7 days
- Users can re-login via email or passkey
- Consider implementing "remember me" for longer sessions

## Next Steps

- [Permissions](/docs/05-permissions) - Configure role-based access control
- [Deployment](/docs/06-deployment) - Production security best practices
