#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Comprehensive test suite for Tenrankai marketing site
Tests all pages, static files, and API endpoints
"""

import subprocess
import time
import requests
import sys
import os
import json

# Colors
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

class ComprehensiveTester:
    def __init__(self):
        self.port = 3460
        self.base_url = f"http://localhost:{self.port}"
        self.passed = 0
        self.failed = 0
        
    def print_header(self, text):
        print(f"\n{YELLOW}{text}{NC}")
        print("=" * len(text))
        
    def test_endpoint(self, path, name, expected_status=200, expected_content=None):
        """Test a single endpoint"""
        url = f"{self.base_url}{path}"
        
        try:
            response = requests.get(url, timeout=5)
            
            # Check status
            if response.status_code == expected_status:
                status_ok = True
            else:
                print(f"{RED}✗ {name}: Expected {expected_status}, got {response.status_code}{NC}")
                self.failed += 1
                return False
                
            # Check content if specified
            if expected_content and expected_content not in response.text:
                print(f"{RED}✗ {name}: Missing expected content '{expected_content}'{NC}")
                self.failed += 1
                return False
                
            print(f"{GREEN}✓ {name}: OK{NC}")
            self.passed += 1
            return True
            
        except Exception as e:
            print(f"{RED}✗ {name}: {e}{NC}")
            self.failed += 1
            return False
    
    def test_with_server(self, test_name, test_func):
        """Run a test function with a temporary server"""
        self.print_header(test_name)
        
        # Start server
        server = subprocess.Popen(
            ["../tenrankai/target/release/tenrankai", "--config", "config.toml", 
             "--port", str(self.port), "--quit-after", "30"],
            cwd="tenrankai-dot-com",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # Wait for startup
        time.sleep(2)
        
        # Check if running
        if server.poll() is not None:
            print(f"{RED}✗ Server failed to start{NC}")
            output = server.stdout.read()
            print(f"Output: {output}")
            self.failed += 1
            return
        
        # Run the test
        try:
            test_func()
        finally:
            # Clean up
            server.terminate()
            try:
                server.wait(timeout=5)
            except:
                server.kill()
                server.wait()
    
    def test_pages(self):
        """Test all main pages"""
        tests = [
            ("/", "Homepage", 200, "<h1>Tenrankai</h1>"),
            ("/features", "Features page", 200, "File-Based Architecture"),
            ("/about", "About page", 200, "About Tenrankai"),
            ("/contact", "Get Involved page", 200, "Get Involved"),
            ("/gallery", "Gallery", 200, None),
            ("/docs", "Documentation", 200, "Quick Start Guide"),
            ("/blog", "Blog", 200, "Introducing Tenrankai"),
        ]
        
        for path, name, status, content in tests:
            self.test_endpoint(path, name, status, content)
    
    def test_documentation(self):
        """Test documentation pages"""
        tests = [
            ("/docs/00-quick-start", "Quick Start guide", 200, "5-Minute Setup"),
            ("/docs/01-installation", "Installation guide", 200, "Installation Guide"),
            ("/docs/02-core-concepts", "Core Concepts guide", 200, "Core Concepts"),
        ]
        
        for path, name, status, content in tests:
            self.test_endpoint(path, name, status, content)
    
    def test_blog_posts(self):
        """Test blog posts"""
        self.test_endpoint("/blog/introducing-tenrankai", "Blog post", 200, 
                          "high-performance photo gallery")
    
    def test_static_files(self):
        """Test static file serving"""
        tests = [
            ("/static/style.css", "Main CSS", 200, "font-family"),
            ("/static/home.css", "Home CSS", 200, None),
            ("/static/DejaVuSans.ttf", "Font file", 200, None),
            ("/favicon.ico", "Favicon", 200, None),
            ("/robots.txt", "Robots.txt", 200, None),
        ]
        
        for path, name, status, content in tests:
            self.test_endpoint(path, name, status, content)
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        # Gallery preview API
        try:
            response = requests.get(f"{self.base_url}/api/gallery/main/preview", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and "images" in data and isinstance(data["images"], list):
                    print(f"{GREEN}✓ Gallery API: Returns {len(data['images'])} images{NC}")
                    self.passed += 1
                else:
                    print(f"{RED}✗ Gallery API: Invalid response format{NC}")
                    self.failed += 1
            else:
                print(f"{RED}✗ Gallery API: HTTP {response.status_code}{NC}")
                self.failed += 1
        except Exception as e:
            print(f"{RED}✗ Gallery API: {e}{NC}")
            self.failed += 1
    
    def test_error_pages(self):
        """Test error handling"""
        self.test_endpoint("/nonexistent", "404 page", 404, None)
        self.test_endpoint("/gallery/nonexistent", "Gallery 404", 404, None)
    
    def run_all_tests(self):
        """Run all test suites"""
        print(f"{YELLOW}=== Tenrankai Comprehensive Test Suite ==={NC}")
        
        # Build if needed
        if not os.path.exists("tenrankai/target/release/tenrankai"):
            print("\nBuilding Tenrankai...")
            result = subprocess.run(["cargo", "build", "--release"], 
                                  cwd="tenrankai", capture_output=True)
            if result.returncode != 0:
                print(f"{RED}✗ Build failed{NC}")
                return False
        
        # Run test suites
        self.test_with_server("Main Pages", self.test_pages)
        self.test_with_server("Documentation", self.test_documentation)
        self.test_with_server("Blog Posts", self.test_blog_posts)
        self.test_with_server("Static Files", self.test_static_files)
        self.test_with_server("API Endpoints", self.test_api_endpoints)
        self.test_with_server("Error Handling", self.test_error_pages)
        
        # Summary
        self.print_header("Test Summary")
        total = self.passed + self.failed
        print(f"Total tests: {total}")
        print(f"{GREEN}Passed: {self.passed}{NC}")
        if self.failed > 0:
            print(f"{RED}Failed: {self.failed}{NC}")
            return False
        else:
            print(f"\n{GREEN}All tests passed!{NC}")
            return True

if __name__ == "__main__":
    tester = ComprehensiveTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)