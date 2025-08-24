#!/usr/bin/env python3
# /// script
# dependencies = ["requests"]
# ///
"""
Quick test to verify Tenrankai can start with the marketing site config
"""

import subprocess
import time
import requests
import sys
import os

def test_server_start():
    """Test if server starts successfully"""
    print("Testing Tenrankai server startup...")
    
    # Change to site directory
    os.chdir("tenrankai-dot-com")
    
    # Start server with short quit timer
    cmd = ["../tenrankai/target/release/tenrankai", "--config", "config.toml", "--quit-after", "5"]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        print("\n--- STDOUT ---")
        print(result.stdout)
        
        if result.stderr:
            print("\n--- STDERR ---")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✓ Server started and stopped successfully")
            return True
        else:
            print(f"\n✗ Server exited with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n✗ Server timed out (hung)")
        return False
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def test_basic_endpoints():
    """Test basic endpoints while server is running"""
    print("\nTesting basic endpoints...")
    
    # Change back to root directory first
    os.chdir("..")
    
    # Get the absolute path to tenrankai binary
    tenrankai_bin = os.path.abspath("tenrankai/target/release/tenrankai")
    
    # Start server in background
    server = subprocess.Popen(
        [tenrankai_bin, "--config", "config.toml", "--port", "3460"],
        cwd="tenrankai-dot-com",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        # Wait for startup
        print("Waiting for server to start...")
        time.sleep(3)
        
        # Check if still running
        if server.poll() is not None:
            output = server.stdout.read()
            print(f"Server died. Output:\n{output}")
            return False
        
        # Test homepage directly (no health endpoint)
        try:
            response = requests.get("http://localhost:3460/", timeout=5)
            print(f"Homepage: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ Server is responding")
                
                if "Tenrankai" in response.text:
                    print("✓ Homepage contains 'Tenrankai'")
                else:
                    print("✗ Homepage missing expected content")
                    
                # Test gallery preview API
                response = requests.get("http://localhost:3460/api/gallery/main/preview", timeout=5)
                print(f"Gallery API: {response.status_code}")
                
                if response.status_code == 200:
                    print("✓ Gallery API working")
                    return True
                else:
                    print("✗ Gallery API failed")
                    return False
            else:
                print("✗ Homepage request failed")
                return False
                
        except Exception as e:
            print(f"✗ Request failed: {e}")
            return False
            
    finally:
        # Clean up
        server.terminate()
        try:
            server.wait(timeout=5)
        except:
            server.kill()
            server.wait()

if __name__ == "__main__":
    print("=== Tenrankai Quick Test ===\n")
    
    # Test 1: Can server start and stop cleanly?
    test1 = test_server_start()
    
    # Test 2: Can we connect to endpoints?
    test2 = test_basic_endpoints()
    
    print("\n=== Summary ===")
    print(f"Server startup test: {'PASS' if test1 else 'FAIL'}")
    print(f"Endpoint test: {'PASS' if test2 else 'FAIL'}")
    
    sys.exit(0 if (test1 and test2) else 1)