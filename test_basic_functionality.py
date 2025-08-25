#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Basic functionality test for Tenrankai marketing site
Tests core pages and endpoints with automatic server management
"""

import subprocess
import time
import requests
import sys
import os

# Colors for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'

def run_test():
    """Run basic functionality tests"""
    print(f"{YELLOW}=== Tenrankai Basic Functionality Test ==={NC}\n")
    
    # Build if needed
    if not os.path.exists("tenrankai/target/release/tenrankai"):
        print("Building Tenrankai...")
        result = subprocess.run(["cargo", "build", "--release"], cwd="tenrankai", capture_output=True)
        if result.returncode != 0:
            print(f"{RED}✗ Build failed{NC}")
            return False
    
    # Start server with quit-after for safety
    print("Starting server...")
    server = subprocess.Popen(
        ["../tenrankai/target/release/tenrankai", "--config", "config.toml", "--port", "3459"],
        cwd="tenrankai-dot-com",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for startup
    time.sleep(2)
    
    # Check if server is still running
    if server.poll() is not None:
        output = server.stdout.read()
        print(f"{RED}✗ Server failed to start{NC}")
        print(f"Output: {output}")
        return False
    
    # Test endpoints
    base_url = "http://localhost:3459"
    tests = [
        ("/", "Homepage"),
        ("/features", "Features page"),
        ("/about", "About page"),
        ("/gallery", "Gallery"),
        ("/docs", "Documentation"),
        ("/blog", "Blog"),
        ("/api/gallery/main/preview", "Gallery API"),
    ]
    
    all_passed = True
    for path, name in tests:
        try:
            response = requests.get(f"{base_url}{path}", timeout=5)
            if response.status_code == 200:
                print(f"{GREEN}✓ {name}: OK{NC}")
            else:
                print(f"{RED}✗ {name}: HTTP {response.status_code}{NC}")
                all_passed = False
        except Exception as e:
            print(f"{RED}✗ {name}: {e}{NC}")
            all_passed = False
    
    # Clean up
    server.terminate()
    try:
        server.wait(timeout=5)
    except:
        server.kill()
        server.wait()
    
    print(f"\n{YELLOW}=== Summary ==={NC}")
    if all_passed:
        print(f"{GREEN}All tests passed!{NC}")
        return True
    else:
        print(f"{RED}Some tests failed{NC}")
        return False

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)