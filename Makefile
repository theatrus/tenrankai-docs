# Makefile for Tenrankai marketing site development and testing

.PHONY: help build test test-quick test-dev test-prod run run-dev clean

# Default target
help:
	@echo "Tenrankai Marketing Site - Available Commands:"
	@echo "============================================="
	@echo "  make build       - Build Tenrankai"
	@echo "  make test        - Run comprehensive test suite"
	@echo "  make test-quick  - Run quick bash test script"
	@echo "  make test-dev    - Test with dev config"
	@echo "  make test-prod   - Test with production config"
	@echo "  make run         - Run the site (default config)"
	@echo "  make run-dev     - Run the site (dev config)"
	@echo "  make clean       - Clean cache and build artifacts"

# Build Tenrankai
build:
	@echo "Building Tenrankai..."
	@cd tenrankai && cargo build --release

# Run comprehensive Python test suite
test: build
	@echo "Running comprehensive test suite..."
	@uv run test_tenrankai_site.py

# Run quick bash test script
test-quick: build
	@echo "Running quick test script..."
	@./test-tenrankai-site.sh

# Test with dev config
test-dev: build
	@echo "Testing with development config..."
	@uv run test_tenrankai_site.py --config config.dev.toml --port 3457

# Test with production config (will fail on paths but tests config parsing)
test-prod: build
	@echo "Testing with production config..."
	@cd tenrankai-dot-com && \
	../tenrankai/target/release/tenrankai --config config.production.toml --quit-after 2 || \
	echo "Expected failures due to production paths"

# Run the site with default config
run: build
	@echo "Starting Tenrankai marketing site..."
	@echo "Visit http://localhost:3000"
	@cd tenrankai-dot-com && ../tenrankai/target/release/tenrankai

# Run the site with dev config
run-dev: build
	@echo "Starting Tenrankai marketing site (dev config)..."
	@echo "Visit http://localhost:3000"
	@cd tenrankai-dot-com && ../tenrankai/target/release/tenrankai --config config.dev.toml

# Clean build artifacts and cache
clean:
	@echo "Cleaning build artifacts and cache..."
	@cd tenrankai && cargo clean
	@rm -rf tenrankai-dot-com/cache
	@rm -f tenrankai-dot-com/server.log
	@echo "Clean complete"

# Run site and keep it running for manual testing
run-keep: build
	@echo "Starting Tenrankai and keeping it running..."
	@uv run test_tenrankai_site.py --keep-running