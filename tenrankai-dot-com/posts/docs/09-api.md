+++
title = "API Reference"
summary = "REST API for integrating with Tenrankai programmatically"
date = "2026-01-13"
+++

# API Reference

Tenrankai provides a RESTful API for programmatic access to galleries, images, and metadata.

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

## Response Format

All responses are JSON with consistent structure:

```json
{
  "success": true,
  "data": { /* response data */ },
  "error": null,
  "timestamp": "2026-01-13T22:16:48Z"
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
  "timestamp": "2026-01-13T22:16:48Z"
}
```

## Gallery Endpoints

### List Galleries

`GET /api/v1/galleries`

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
        "last_updated": "2026-01-13T20:30:15Z"
      }
    ]
  }
}
```

### Get Gallery Details

`GET /api/v1/galleries/{gallery_name}`

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
    "last_updated": "2026-01-13T20:30:15Z",
    "supported_formats": ["jpg", "jpeg", "png", "webp", "avif"]
  }
}
```

### List Gallery Contents

`GET /api/v1/galleries/{gallery_name}/contents`

**Query Parameters**:
| Parameter | Default | Description |
|-----------|---------|-------------|
| `path` | root | Folder path within gallery |
| `recursive` | false | Include subfolders recursively |
| `limit` | 100 | Maximum items to return |
| `offset` | 0 | Pagination offset |
| `sort` | name | Sort order: `name`, `date`, `size` |
| `order` | asc | `asc` or `desc` |

```json
{
  "success": true,
  "data": {
    "path": "/vacation/2026",
    "folders": [
      {
        "name": "beach",
        "path": "/vacation/2026/beach",
        "image_count": 34,
        "description": "Beach photos from the trip"
      }
    ],
    "images": [
      {
        "filename": "sunset.jpg",
        "path": "/vacation/2026/sunset.jpg",
        "caption": "Beautiful sunset over the ocean",
        "width": 4000,
        "height": 3000,
        "size_bytes": 2048576,
        "format": "JPEG",
        "urls": {
          "original": "/gallery/vacation/2026/sunset.jpg",
          "large": "/gallery/vacation/2026/sunset.jpg?size=large",
          "medium": "/gallery/vacation/2026/sunset.jpg?size=medium",
          "thumbnail": "/gallery/vacation/2026/sunset.jpg?size=thumbnail"
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

`GET /api/v1/galleries/{gallery_name}/images?path=/path/to/image.jpg`

```json
{
  "success": true,
  "data": {
    "filename": "sunset.jpg",
    "path": "/vacation/2026/sunset.jpg",
    "caption": "Beautiful sunset over the ocean",
    "width": 4000,
    "height": 3000,
    "size_bytes": 2048576,
    "format": "JPEG",
    "color_profile": "sRGB",
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
      "original": "/gallery/vacation/2026/sunset.jpg",
      "large": "/gallery/vacation/2026/sunset.jpg?size=large",
      "medium": "/gallery/vacation/2026/sunset.jpg?size=medium",
      "thumbnail": "/gallery/vacation/2026/sunset.jpg?size=thumbnail"
    }
  }
}
```

### Get Image Variants

`GET /api/v1/galleries/{gallery_name}/images/variants?path=/path/to/image.jpg`

```json
{
  "success": true,
  "data": {
    "original": {
      "url": "/gallery/vacation/2026/sunset.jpg",
      "width": 4000,
      "height": 3000,
      "size_bytes": 2048576
    },
    "large": {
      "url": "/gallery/vacation/2026/sunset.jpg?size=large",
      "width": 1920,
      "height": 1440,
      "size_bytes": 512000
    },
    "medium": {
      "url": "/gallery/vacation/2026/sunset.jpg?size=medium",
      "width": 800,
      "height": 600,
      "size_bytes": 128000
    },
    "thumbnail": {
      "url": "/gallery/vacation/2026/sunset.jpg?size=thumbnail",
      "width": 300,
      "height": 225,
      "size_bytes": 32000
    }
  }
}
```

## Search Endpoints

### Search Images

`GET /api/v1/search/images`

**Query Parameters**:
| Parameter | Description |
|-----------|-------------|
| `q` | Search query string |
| `gallery` | Limit to specific gallery |
| `path` | Limit to specific folder |
| `format` | Filter by format (jpg, png, etc.) |
| `limit` | Maximum results (default: 50) |
| `offset` | Pagination offset |

```json
{
  "success": true,
  "data": {
    "query": "sunset",
    "results": [
      {
        "filename": "sunset.jpg",
        "path": "/vacation/2026/sunset.jpg",
        "gallery": "main",
        "caption": "Beautiful sunset over the ocean",
        "score": 0.95,
        "urls": {
          "thumbnail": "/gallery/vacation/2026/sunset.jpg?size=thumbnail",
          "medium": "/gallery/vacation/2026/sunset.jpg?size=medium"
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

`GET /api/v1/galleries/{gallery_name}/stats`

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
      }
    }
  }
}
```

### System Statistics

`GET /api/v1/stats/system` (requires authentication)

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

## Cache Management

### Cache Status

`GET /api/v1/galleries/{gallery_name}/cache/status`

```json
{
  "success": true,
  "data": {
    "gallery": "main",
    "cache_enabled": true,
    "total_cached_variants": 1225,
    "cache_size_bytes": 536870912,
    "cache_directory": "/var/cache/tenrankai/main",
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

`DELETE /api/v1/galleries/{gallery_name}/cache` (requires authentication)

**Query Parameters**:
- `variants`: Comma-separated list (thumbnail, medium, large)
- `path`: Clear cache only for specific path

## WebAuthn API

### Registration

**Start**: `POST /_login/passkey/register/start`

**Finish**: `POST /_login/passkey/register/finish`

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

### Authentication

**Start**: `POST /_login/passkey/authenticate/start`

**Finish**: `POST /_login/passkey/authenticate/finish`

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

## Error Codes

### HTTP Status Codes

| Status | Meaning |
|--------|---------|
| `200 OK` | Request successful |
| `400 Bad Request` | Invalid request parameters |
| `401 Unauthorized` | Authentication required |
| `403 Forbidden` | Access denied |
| `404 Not Found` | Resource not found |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Server error |

### API Error Codes

| Code | Description |
|------|-------------|
| `INVALID_GALLERY` | Gallery name not found |
| `INVALID_PATH` | Image or folder path not found |
| `INVALID_FORMAT` | Unsupported image format |
| `CACHE_ERROR` | Cache operation failed |
| `RATE_LIMIT` | Too many requests |
| `AUTH_REQUIRED` | Authentication required |

## Rate Limiting

**Default Limits:**
- Authenticated users: 1000 requests per hour
- Unauthenticated users: 100 requests per hour
- Search endpoints: 50 requests per hour per IP

**Rate Limit Headers:**
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1629876543
```

## Example Clients

### JavaScript

```javascript
class TenrankaiAPI {
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

        const response = await fetch(url, { ...options, headers });
        return await response.json();
    }

    getGalleries() {
        return this.request('/galleries');
    }

    getGalleryContents(gallery, path = '') {
        const params = new URLSearchParams();
        if (path) params.set('path', path);
        return this.request(`/galleries/${gallery}/contents?${params}`);
    }

    searchImages(query, gallery = null) {
        const params = new URLSearchParams({ q: query });
        if (gallery) params.set('gallery', gallery);
        return this.request(`/search/images?${params}`);
    }
}

// Usage
const api = new TenrankaiAPI('http://localhost:3000', 'your-password');
const galleries = await api.getGalleries();
```

### Python

```python
import requests
from typing import Optional

class TenrankaiAPI:
    def __init__(self, base_url: str, password: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        if password:
            self.session.auth = ('', password)

    def request(self, endpoint: str, method: str = 'GET', **kwargs):
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
```

### cURL

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
```

## OpenAPI Specification

Tenrankai provides an OpenAPI 3.0 specification at:

```
GET /api/v1/openapi.json
```

This can be used with Swagger UI, Postman, or code generators for automatic client generation.

## Next Steps

- [Authentication](/docs/04-authentication) - Configure API authentication
- [Permissions](/docs/05-permissions) - Set up access control
- [Deployment](/docs/06-deployment) - Deploy with API access
