# Testing the Tenrankai Marketing Site

This directory contains test suites to verify that Tenrankai can correctly serve the marketing and documentation website.

## Quick Start

```bash
# Run all tests
make test

# Run the site for manual testing
make run

# Run with dev config
make run-dev
```

## Available Tests

### 1. Bash Test Script (`test-tenrankai-site.sh`)

A simple shell script that:
- Builds Tenrankai
- Starts the server
- Tests basic endpoints
- Performs cleanup

Run with:
```bash
./test-tenrankai-site.sh
# or
make test-quick
```

### 2. Python Test Suite (`test_tenrankai_site.py`)

A comprehensive test suite that:
- Builds Tenrankai
- Tests all pages and endpoints
- Validates API responses
- Checks static file serving
- Provides detailed error reporting

Run with:
```bash
uv run test_tenrankai_site.py

# Test with different config
uv run test_tenrankai_site.py --config config.dev.toml --port 3457

# Keep server running after tests
uv run test_tenrankai_site.py --keep-running
```

### 3. Makefile Commands

```bash
make help        # Show all available commands
make build       # Build Tenrankai
make test        # Run comprehensive tests
make test-quick  # Run quick bash tests
make test-dev    # Test with dev config
make test-prod   # Test production config parsing
make run         # Run the site
make run-dev     # Run with dev config
make clean       # Clean build artifacts
```

## What Gets Tested

### Pages
- Homepage (`/`)
- Features (`/features`)
- About (`/about`)
- Get Involved (`/contact`)
- Gallery Demo (`/gallery`)
- Documentation (`/docs`)
- Blog (`/blog`)

### Documentation Posts
- Quick Start Guide (`/docs/00-quick-start`)
- Installation Guide (`/docs/01-installation`)
- Core Concepts Guide (`/docs/02-core-concepts`)

### Blog Posts
- Introducing Tenrankai (`/blog/introducing-tenrankai`)

### Static Files
- CSS files (`/static/*.css`)
- Font file (`/static/DejaVuSans.ttf`)

### API Endpoints
- Health check (`/api/health`)
- Gallery preview (`/api/gallery/main/preview`)

### Error Handling
- 404 pages

## Configuration Files Tested

1. **`config.toml`** - Default marketing site configuration
2. **`config.dev.toml`** - Simplified development configuration
3. **`config.production.toml`** - Production configuration example

## CI/CD Integration

The `.github/workflows/test-site.yml` workflow automatically:
- Builds Tenrankai
- Runs the Python test suite
- Tests different configurations
- Validates TOML files
- Checks for required files

## Troubleshooting

### Port Already in Use
The tests use port 3456 by default. If this port is in use:
```bash
uv run test_tenrankai_site.py --port 3457
```

### Build Failures
Ensure Rust 1.89.0+ is installed:
```bash
rustup update
cd tenrankai && cargo build --release
```

### Missing Dependencies
The Python test script uses `uv` which automatically handles dependencies via inline script metadata:
```python
# /// script
# dependencies = ["requests"]
# ///
```

No manual installation needed!

### Server Won't Start
Check the server log:
```bash
cat tenrankai-dot-com/server.log
```

Common issues:
- Missing `DejaVuSans.ttf` font file
- Missing templates or static directories
- Invalid configuration