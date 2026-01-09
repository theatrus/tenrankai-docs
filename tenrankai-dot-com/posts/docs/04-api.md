+++
title = "API Documentation"
summary = "REST API reference for integrating with Tenrankai programmatically"
date = "2026-01-09"
+++

# API Documentation

Tenrankai provides a RESTful API for programmatic access to galleries, images, and metadata. This guide covers all available endpoints and their usage.

## Base URL and Authentication

### Base URL

All API requests are made to:
```
http://your-domain.com/api/v1
```

### Authentication

The API uses the same authentication system as the web interface:

1. **Session-based**: Use cookies from web login
2. **HTTP Basic Auth**: Use configured password
3. **No auth**: For public galleries without authentication enabled

```bash
# Using HTTP Basic Auth
curl -u ":your-password" http://localhost:3000/api/v1/galleries

# Using session cookie
curl -b "session=your-session-cookie" http://localhost:3000/api/v1/galleries
```

## Content Types

### Request Format

- **Content-Type**: `application/json` for POST/PUT requests
- **Accept**: `application/json` for JSON responses

### Response Format

All responses are JSON with consistent structure:

```json
{
  "success": true,
  "data": { /* response data */ },
  "error": null,
  "timestamp": "2026-01-09T22:16:48Z"
}
```

Error responses:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "NOT_FOUND",
    "message": "Gallery not found"
  },
  "timestamp": "2026-01-09T22:16:48Z"
}
```

## Gallery Endpoints

### List Galleries

Get all configured galleries and their metadata.

**Endpoint**: `GET /api/v1/galleries`

**Response**:
```json
{
  "success": true,
  "data": {
    "galleries": [
      {
        "name": "main",
        "url_prefix": "/gallery",
        "description": "Main photo gallery",
        "image_count": 245,
        "folder_count": 12,
        "last_updated": "2026-01-09T20:30:15Z"
      }
    ]
  }
}
```

### Get Gallery Details

Get detailed information about a specific gallery.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}`

**Parameters**:
- `gallery_name`: Gallery identifier from configuration

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "main",
    "url_prefix": "/gallery",
    "description": "Main photo gallery",
    "source_directory": "photos",
    "image_count": 245,
    "folder_count": 12,
    "total_size_bytes": 2147483648,
    "last_updated": "2025-08-25T20:30:15Z",
    "supported_formats": ["jpg", "jpeg", "png", "webp", "tiff"]
  }
}
```

### List Gallery Contents

Get the contents of a gallery or folder within a gallery.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}/contents`

**Query Parameters**:
- `path` (optional): Folder path within gallery (default: root)
- `recursive` (optional): Include subfolders recursively (default: false)
- `limit` (optional): Maximum items to return (default: 100)
- `offset` (optional): Pagination offset (default: 0)
- `sort` (optional): Sort order - `name`, `date`, `size` (default: name)
- `order` (optional): `asc` or `desc` (default: asc)

**Response**:
```json
{
  "success": true,
  "data": {
    "path": "/vacation/2025",
    "folders": [
      {
        "name": "beach",
        "path": "/vacation/2025/beach",
        "image_count": 34,
        "description": "Beach photos from the trip",
        "created": "2026-01-09T10:00:00Z"
      }
    ],
    "images": [
      {
        "filename": "sunset.jpg",
        "path": "/vacation/2025/sunset.jpg",
        "caption": "Beautiful sunset over the ocean",
        "width": 4000,
        "height": 3000,
        "size_bytes": 2048576,
        "format": "JPEG",
        "created": "2026-01-09T18:30:22Z",
        "urls": {
          "original": "/gallery/vacation/2025/sunset.jpg",
          "large": "/gallery/vacation/2025/sunset.jpg?size=large",
          "medium": "/gallery/vacation/2025/sunset.jpg?size=medium",
          "thumbnail": "/gallery/vacation/2025/sunset.jpg?size=thumbnail"
        }
      }
    ],
    "total_items": 35,
    "has_more": false
  }
}
```

## Image Endpoints

### Get Image Details

Get metadata for a specific image.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}/images`

**Query Parameters**:
- `path`: Full path to image within gallery

**Example**: `GET /api/v1/galleries/main/images?path=/vacation/2025/sunset.jpg`

**Response**:
```json
{
  "success": true,
  "data": {
    "filename": "sunset.jpg",
    "path": "/vacation/2025/sunset.jpg",
    "caption": "Beautiful sunset over the ocean",
    "width": 4000,
    "height": 3000,
    "size_bytes": 2048576,
    "format": "JPEG",
    "color_profile": "sRGB",
    "created": "2026-01-09T18:30:22Z",
    "modified": "2026-01-09T09:15:30Z",
    "exif": {
      "camera": "Canon EOS R5",
      "lens": "RF 24-70mm f/2.8L IS USM",
      "iso": 100,
      "aperture": "f/8.0",
      "shutter_speed": "1/125",
      "focal_length": "35mm",
      "gps": {
        "latitude": 34.0522,
        "longitude": -118.2437
      }
    },
    "urls": {
      "original": "/gallery/vacation/2025/sunset.jpg",
      "large": "/gallery/vacation/2025/sunset.jpg?size=large",
      "medium": "/gallery/vacation/2025/sunset.jpg?size=medium",
      "thumbnail": "/gallery/vacation/2025/sunset.jpg?size=thumbnail"
    }
  }
}
```

### Get Image Variants

Get URLs for different sizes of an image.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}/images/variants`

**Query Parameters**:
- `path`: Full path to image within gallery

**Response**:
```json
{
  "success": true,
  "data": {
    "original": {
      "url": "/gallery/vacation/2025/sunset.jpg",
      "width": 4000,
      "height": 3000,
      "size_bytes": 2048576
    },
    "large": {
      "url": "/gallery/vacation/2025/sunset.jpg?size=large",
      "width": 1920,
      "height": 1440,
      "size_bytes": 512000
    },
    "medium": {
      "url": "/gallery/vacation/2025/sunset.jpg?size=medium",
      "width": 800,
      "height": 600,
      "size_bytes": 128000
    },
    "thumbnail": {
      "url": "/gallery/vacation/2025/sunset.jpg?size=thumbnail",
      "width": 300,
      "height": 225,
      "size_bytes": 32000
    }
  }
}
```

## Search Endpoints

### Search Images

Search for images across galleries by filename, caption, or metadata.

**Endpoint**: `GET /api/v1/search/images`

**Query Parameters**:
- `q`: Search query string
- `gallery` (optional): Limit search to specific gallery
- `path` (optional): Limit search to specific folder
- `format` (optional): Filter by image format (jpg, png, etc.)
- `limit` (optional): Maximum results to return (default: 50)
- `offset` (optional): Pagination offset

**Example**: `GET /api/v1/search/images?q=sunset&gallery=main&limit=10`

**Response**:
```json
{
  "success": true,
  "data": {
    "query": "sunset",
    "results": [
      {
        "filename": "sunset.jpg",
        "path": "/vacation/2025/sunset.jpg",
        "gallery": "main",
        "caption": "Beautiful sunset over the ocean",
        "score": 0.95,
        "urls": {
          "thumbnail": "/gallery/vacation/2025/sunset.jpg?size=thumbnail",
          "medium": "/gallery/vacation/2025/sunset.jpg?size=medium"
        }
      }
    ],
    "total_results": 1,
    "search_time_ms": 23
  }
}
```

## Statistics Endpoints

### Gallery Statistics

Get statistical information about a gallery.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}/stats`

**Response**:
```json
{
  "success": true,
  "data": {
    "gallery": "main",
    "statistics": {
      "total_images": 245,
      "total_folders": 12,
      "total_size_bytes": 2147483648,
      "formats": {
        "JPEG": 198,
        "PNG": 35,
        "WEBP": 12
      },
      "cache_statistics": {
        "cached_variants": 1225,
        "cache_size_bytes": 536870912,
        "cache_hit_rate": 0.87
      },
      "recent_activity": {
        "images_added_last_week": 8,
        "images_modified_last_week": 3
      }
    }
  }
}
```

### System Statistics

Get overall system statistics (requires authentication).

**Endpoint**: `GET /api/v1/stats/system`

**Response**:
```json
{
  "success": true,
  "data": {
    "version": "1.0.0",
    "uptime_seconds": 86400,
    "galleries": {
      "total_galleries": 3,
      "total_images": 1024,
      "total_size_bytes": 8589934592
    },
    "cache": {
      "total_cached_variants": 5120,
      "cache_size_bytes": 2147483648,
      "cache_hit_rate": 0.89
    },
    "performance": {
      "requests_per_second": 45.2,
      "average_response_time_ms": 127,
      "memory_usage_bytes": 134217728
    }
  }
}
```

## Configuration Endpoints

### Get Configuration

Get current server configuration (requires authentication).

**Endpoint**: `GET /api/v1/config`

**Response**:
```json
{
  "success": true,
  "data": {
    "server": {
      "host": "127.0.0.1",
      "port": 3000
    },
    "app": {
      "name": "My Gallery"
    },
    "galleries": [
      {
        "name": "main",
        "url_prefix": "/gallery",
        "source_directory": "photos"
      }
    ],
    "version": "1.0.0",
    "build_date": "2026-01-09T12:00:00Z"
  }
}
```

## Cache Management Endpoints

### Cache Status

Get cache status for a gallery.

**Endpoint**: `GET /api/v1/galleries/{gallery_name}/cache/status`

**Response**:
```json
{
  "success": true,
  "data": {
    "gallery": "main",
    "cache_enabled": true,
    "total_cached_variants": 1225,
    "cache_size_bytes": 536870912,
    "cache_directory": "/var/cache/tenrankai/main",
    "last_cleanup": "2026-01-09T06:00:00Z",
    "pre_generation_status": {
      "enabled": true,
      "progress": {
        "total_images": 245,
        "processed_images": 245,
        "percentage": 100.0,
        "status": "completed"
      }
    }
  }
}
```

### Clear Cache

Clear cache for a gallery (requires authentication).

**Endpoint**: `DELETE /api/v1/galleries/{gallery_name}/cache`

**Query Parameters**:
- `variants` (optional): Comma-separated list of variants to clear (thumbnail, medium, large)
- `path` (optional): Clear cache only for specific path

**Response**:
```json
{
  "success": true,
  "data": {
    "gallery": "main",
    "cleared_variants": ["thumbnail", "medium", "large"],
    "freed_space_bytes": 134217728,
    "message": "Cache cleared successfully"
  }
}
```

## Webhook Endpoints

### File System Events

Get recent file system events for galleries.

**Endpoint**: `GET /api/v1/events/filesystem`

**Query Parameters**:
- `gallery` (optional): Filter events for specific gallery
- `since` (optional): ISO timestamp to get events since
- `limit` (optional): Maximum events to return (default: 100)

**Response**:
```json
{
  "success": true,
  "data": {
    "events": [
      {
        "id": "evt_123456789",
        "gallery": "main",
        "type": "image_added",
        "path": "/new-photos/image001.jpg",
        "timestamp": "2026-01-09T20:30:15Z",
        "metadata": {
          "filename": "image001.jpg",
          "size_bytes": 1048576
        }
      },
      {
        "id": "evt_123456790",
        "gallery": "main", 
        "type": "folder_created",
        "path": "/new-photos",
        "timestamp": "2026-01-09T20:29:45Z"
      }
    ],
    "has_more": false
  }
}
```

## Error Codes

### HTTP Status Codes

- `200 OK` - Request successful
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### API Error Codes

```json
{
  "INVALID_GALLERY": "Gallery name not found",
  "INVALID_PATH": "Image or folder path not found", 
  "INVALID_FORMAT": "Unsupported image format",
  "CACHE_ERROR": "Cache operation failed",
  "RATE_LIMIT": "Too many requests",
  "AUTH_REQUIRED": "Authentication required",
  "CONFIG_ERROR": "Configuration error",
  "SEARCH_ERROR": "Search query failed"
}
```

## Rate Limiting

### Default Limits

- **Authenticated users**: 1000 requests per hour
- **Unauthenticated users**: 100 requests per hour
- **Search endpoints**: 50 requests per hour per IP

### Rate Limit Headers

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1629876543
```

## Example Integrations

### JavaScript/Node.js

```javascript
const TenrankaiAPI = class {
    constructor(baseUrl, password = null) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.password = password;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}/api/v1${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };
        
        if (this.password) {
            headers['Authorization'] = `Basic ${btoa(':' + this.password)}`;
        }
        
        const response = await fetch(url, {
            ...options,
            headers: { ...headers, ...options.headers }
        });
        
        return await response.json();
    }
    
    async getGalleries() {
        return this.request('/galleries');
    }
    
    async getGalleryContents(gallery, path = '') {
        const params = new URLSearchParams();
        if (path) params.set('path', path);
        return this.request(`/galleries/${gallery}/contents?${params}`);
    }
    
    async searchImages(query, gallery = null) {
        const params = new URLSearchParams({ q: query });
        if (gallery) params.set('gallery', gallery);
        return this.request(`/search/images?${params}`);
    }
};

// Usage
const api = new TenrankaiAPI('http://localhost:3000', 'your-password');
const galleries = await api.getGalleries();
console.log(galleries.data);
```

### Python

```python
import requests
from typing import Optional, Dict, Any

class TenrankaiAPI:
    def __init__(self, base_url: str, password: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        if password:
            self.session.auth = ('', password)
    
    def request(self, endpoint: str, method: str = 'GET', **kwargs) -> Dict[Any, Any]:
        url = f"{self.base_url}/api/v1{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def get_galleries(self):
        return self.request('/galleries')
    
    def get_gallery_contents(self, gallery: str, path: str = ''):
        params = {'path': path} if path else {}
        return self.request(f'/galleries/{gallery}/contents', params=params)
    
    def search_images(self, query: str, gallery: Optional[str] = None):
        params = {'q': query}
        if gallery:
            params['gallery'] = gallery
        return self.request('/search/images', params=params)

# Usage
api = TenrankaiAPI('http://localhost:3000', 'your-password')
galleries = api.get_galleries()
print(galleries['data'])
```

### cURL Examples

```bash
# Get all galleries
curl -X GET "http://localhost:3000/api/v1/galleries" \
     -H "Accept: application/json"

# Get gallery contents with authentication
curl -X GET "http://localhost:3000/api/v1/galleries/main/contents?path=/vacation" \
     -u ":your-password" \
     -H "Accept: application/json"

# Search for images
curl -X GET "http://localhost:3000/api/v1/search/images?q=sunset&limit=5" \
     -H "Accept: application/json"

# Get image details
curl -X GET "http://localhost:3000/api/v1/galleries/main/images?path=/vacation/sunset.jpg" \
     -H "Accept: application/json"
```

## Authentication API Endpoints

### WebAuthn Registration

Register a new passkey for the authenticated user.

**Endpoint**: `POST /_login/passkey/register/start`

**Response**:
```json
{
  "challenge": "base64-encoded-challenge",
  "rp": {
    "name": "Tenrankai",
    "id": "your-domain.com"
  },
  "user": {
    "id": "base64-encoded-user-id",
    "name": "username",
    "displayName": "User Display Name"
  },
  "pubKeyCredParams": [
    { "type": "public-key", "alg": -7 },
    { "type": "public-key", "alg": -257 }
  ],
  "authenticatorSelection": {
    "userVerification": "preferred"
  }
}
```

**Endpoint**: `POST /_login/passkey/register/finish`

**Request**:
```json
{
  "id": "credential-id",
  "rawId": "base64-encoded-raw-id",
  "response": {
    "clientDataJSON": "base64-encoded-client-data",
    "attestationObject": "base64-encoded-attestation"
  },
  "type": "public-key"
}
```

### WebAuthn Authentication

Authenticate using a registered passkey.

**Endpoint**: `POST /_login/passkey/authenticate/start`

**Response**:
```json
{
  "challenge": "base64-encoded-challenge",
  "allowCredentials": [
    {
      "type": "public-key",
      "id": "base64-encoded-credential-id"
    }
  ],
  "userVerification": "preferred"
}
```

**Endpoint**: `POST /_login/passkey/authenticate/finish`

**Request**:
```json
{
  "id": "credential-id",
  "rawId": "base64-encoded-raw-id",
  "response": {
    "clientDataJSON": "base64-encoded-client-data",
    "authenticatorData": "base64-encoded-authenticator-data",
    "signature": "base64-encoded-signature"
  },
  "type": "public-key"
}
```

### User Profile

Get authenticated user profile information.

**Endpoint**: `GET /_login/profile`

**Response**: HTML page with user profile and passkey management

## OpenAPI Specification

Tenrankai provides an OpenAPI 3.0 specification at:
```
GET /api/v1/openapi.json
```

This can be used with tools like Swagger UI, Postman, or code generators for automatic client generation.

## Next Steps

With the API, you can:

- Build custom gallery management interfaces
- Create mobile applications
- Integrate with other systems (DAM, CMS, etc.)
- Automate gallery operations
- Create custom search interfaces

For more information:

- [Configuration Reference](/docs/02-configuration) - Configure API settings
- [Template Customization](/docs/05-templates) - Build web interfaces
- [Deployment Guide](/docs/03-deployment) - Deploy with API access

The API is designed to be RESTful and follows standard conventions for easy integration with any programming language or framework.