#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Comprehensive test suite for Tenrankai marketing site
Tests that Tenrankai can serve the marketing/documentation content correctly
"""

import subprocess
import time
import requests
import sys
import os
import signal
import json
from typing import Optional, Dict, Any
import argparse

# ANSI color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class TenrankaiTester:
    def __init__(self, port: int = 3456, config: str = "config.toml", quit_after: Optional[int] = None):
        self.port = port
        self.config = config
        self.quit_after = quit_after
        self.base_url = f"http://localhost:{port}"
        self.server_process: Optional[subprocess.Popen] = None
        self.tenrankai_dir = "tenrankai"
        self.site_dir = "tenrankai-dot-com"
        
    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{YELLOW}{text}{NC}")
        print("=" * len(text))
        
    def print_success(self, text: str):
        """Print success message"""
        print(f"{GREEN}✓ {text}{NC}")
        
    def print_error(self, text: str):
        """Print error message"""
        print(f"{RED}✗ {text}{NC}")
        
    def print_info(self, text: str):
        """Print info message"""
        print(f"{BLUE}ℹ {text}{NC}")
        
    def build_tenrankai(self) -> bool:
        """Build Tenrankai from source"""
        self.print_header("Building Tenrankai")
        try:
            result = subprocess.run(
                ["cargo", "build", "--release"],
                cwd=self.tenrankai_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.print_success("Build successful")
                return True
            else:
                self.print_error(f"Build failed: {result.stderr}")
                return False
        except Exception as e:
            self.print_error(f"Build error: {e}")
            return False
    
    def start_server(self) -> bool:
        """Start the Tenrankai server"""
        self.print_header("Starting Tenrankai Server")
        
        tenrankai_bin = os.path.join("..", self.tenrankai_dir, "target", "release", "tenrankai")
        cmd = [tenrankai_bin, "serve", "--config", self.config, "--port", str(self.port)]
        if self.quit_after:
            cmd.extend(["--quit-after", str(self.quit_after)])
        
        try:
            self.server_process = subprocess.Popen(
                cmd,
                cwd=self.site_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Wait for server to start
            self.print_info(f"Waiting for server to start on port {self.port}...")
            
            # Try multiple times with shorter waits
            for attempt in range(10):  # 10 attempts, 0.5s each = 5s total
                time.sleep(0.5)
                
                # Check if process is still running
                if self.server_process.poll() is not None:
                    self.print_error("Server process died")
                    # Print last output
                    if self.server_process.stdout:
                        output = self.server_process.stdout.read()
                        print(f"Server output:\n{output}")
                    return False
                    
                # Try to connect to homepage (no health endpoint)
                try:
                    response = requests.get(f"{self.base_url}/", timeout=2)
                    if response.status_code == 200:
                        self.print_success(f"Server started successfully on port {self.port}")
                        return True
                except requests.exceptions.ConnectionError:
                    if attempt < 9:  # Not the last attempt
                        continue
                    else:
                        self.print_error("Could not connect to server after 5 seconds")
                        # Try to get server output
                        if self.server_process.stdout:
                            try:
                                output = self.server_process.stdout.read()
                                if output:
                                    print(f"Server output:\n{output}")
                            except:
                                pass
                        return False
                
        except Exception as e:
            self.print_error(f"Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the Tenrankai server"""
        if self.server_process:
            self.print_info("Stopping server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            self.print_success("Server stopped")
    
    def test_endpoint(self, path: str, description: str, 
                     expected_status: int = 200,
                     expected_content: Optional[str] = None,
                     expected_json: Optional[Dict[str, Any]] = None) -> bool:
        """Test a single endpoint"""
        url = f"{self.base_url}{path}"
        print(f"\n{BLUE}Testing: {description}{NC}")
        print(f"  URL: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            
            # Check status code
            if response.status_code == expected_status:
                self.print_success(f"HTTP {response.status_code}")
            else:
                self.print_error(f"Expected HTTP {expected_status}, got {response.status_code}")
                return False
            
            # Check content
            if expected_content:
                if expected_content in response.text:
                    self.print_success(f"Found expected content: '{expected_content}'")
                else:
                    self.print_error(f"Expected content not found: '{expected_content}'")
                    print(f"  Response preview: {response.text[:200]}...")
                    return False
            
            # Check JSON
            if expected_json:
                try:
                    json_data = response.json()
                    for key, value in expected_json.items():
                        if key in json_data and json_data[key] == value:
                            self.print_success(f"JSON key '{key}' has expected value")
                        else:
                            self.print_error(f"JSON key '{key}' mismatch")
                            return False
                except json.JSONDecodeError:
                    self.print_error("Response is not valid JSON")
                    return False
                    
            return True
            
        except requests.exceptions.RequestException as e:
            self.print_error(f"Request failed: {e}")
            return False
    
    def test_gallery_api(self) -> bool:
        """Test gallery API endpoints"""
        self.print_header("Testing Gallery API")
        
        # Test gallery preview API
        success = self.test_endpoint(
            "/api/gallery/main/preview?count=6",
            "Gallery preview API",
            expected_status=200
        )
        
        if success:
            # Check if response is valid JSON array
            try:
                response = requests.get(f"{self.base_url}/api/gallery/main/preview?count=6")
                data = response.json()
                if isinstance(data, dict) and 'images' in data and isinstance(data['images'], list):
                    self.print_success(f"Gallery preview returned {len(data['images'])} images")
                else:
                    self.print_error("Gallery preview should return an object with 'images' array")
                    success = False
            except:
                success = False
                
        return success
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        self.print_header("Tenrankai Marketing Site Test Suite")
        
        # Check directories
        if not os.path.exists(self.tenrankai_dir):
            self.print_error(f"Tenrankai directory not found: {self.tenrankai_dir}")
            return False
        if not os.path.exists(self.site_dir):
            self.print_error(f"Site directory not found: {self.site_dir}")
            return False
            
        # Build Tenrankai
        if not self.build_tenrankai():
            return False
            
        # Start server
        if not self.start_server():
            return False
            
        # Run tests
        all_passed = True
        
        # Test pages
        tests = [
            ("/", "Homepage", 200, "<h1>Tenrankai</h1>"),
            ("/features", "Features page", 200, "Features"),
            ("/about", "About page", 200, "About Tenrankai"),
            ("/contact", "Contact page", 200, "Get Involved"),
            ("/gallery", "Gallery", 200, None),
            ("/docs", "Documentation", 200, "Quick Start Guide"),
            ("/blog", "Blog", 200, "Introducing Tenrankai"),
            ("/docs/00-quick-start", "Quick Start doc", 200, "5-Minute Setup"),
            ("/docs/01-installation", "Installation doc", 200, "Installation Guide"),
            ("/docs/02-configuration", "Configuration doc", 200, "Configuration Guide"),
            ("/blog/introducing-tenrankai", "Blog post", 200, "high-performance photo gallery"),
        ]
        
        for path, desc, status, content in tests:
            if not self.test_endpoint(path, desc, status, content):
                all_passed = False
                
        # Test static files
        static_tests = [
            ("/static/style.css", "Main CSS", 200, "font-family"),
            ("/static/home.css", "Home CSS", 200, "hero-section"),
            ("/static/DejaVuSans.ttf", "Font file", 200, None),
        ]
        
        for path, desc, status, content in static_tests:
            if not self.test_endpoint(path, desc, status, content):
                all_passed = False
                
        # Test gallery API
        if not self.test_gallery_api():
            all_passed = False
            
        # Test 404
        if not self.test_endpoint("/nonexistent", "404 page", 404):
            all_passed = False
            
        return all_passed
    
    def print_summary(self, success: bool):
        """Print test summary"""
        self.print_header("Test Summary")
        if success:
            self.print_success("All tests passed!")
        else:
            self.print_error("Some tests failed")
            
        # Print server logs
        if self.server_process and self.server_process.stdout:
            print(f"\n{YELLOW}Recent server logs:{NC}")
            # Read last few lines from process stdout
            try:
                self.server_process.stdout.flush()
                output = self.server_process.stdout.read()
                if output:
                    lines = output.strip().split('\n')[-10:]
                    for line in lines:
                        print(f"  {line}")
            except:
                pass

def main():
    parser = argparse.ArgumentParser(description='Test Tenrankai marketing site')
    parser.add_argument('--port', type=int, default=3456, help='Port to run server on')
    parser.add_argument('--config', default='config.toml', help='Config file to use')
    parser.add_argument('--keep-running', action='store_true', 
                       help='Keep server running after tests')
    parser.add_argument('--quit-after', type=int, default=None,
                       help='Auto-quit server after N seconds (useful for CI)')
    
    args = parser.parse_args()
    
    tester = TenrankaiTester(port=args.port, config=args.config, quit_after=args.quit_after)
    
    try:
        success = tester.run_all_tests()
        tester.print_summary(success)
        
        if args.keep_running and success:
            print(f"\n{YELLOW}Server is running at http://localhost:{args.port}{NC}")
            print("Press Ctrl+C to stop...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down...")
        
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 1
    finally:
        if not args.keep_running:
            tester.stop_server()

if __name__ == "__main__":
    sys.exit(main())