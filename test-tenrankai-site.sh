#!/bin/bash
# Test script for Tenrankai marketing site
# This script builds Tenrankai and tests that it can serve the marketing site content

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
TENRANKAI_DIR="tenrankai"
SITE_DIR="tenrankai-dot-com"
TEST_PORT=3456
TIMEOUT=10

echo -e "${YELLOW}Starting Tenrankai Marketing Site Tests${NC}"
echo "========================================"

# Function to cleanup background processes
cleanup() {
    if [ ! -z "$SERVER_PID" ]; then
        echo -e "\n${YELLOW}Cleaning up...${NC}"
        kill $SERVER_PID 2>/dev/null || true
        wait $SERVER_PID 2>/dev/null || true
    fi
}
trap cleanup EXIT

# Test if directories exist
echo -e "\n${YELLOW}1. Checking directories...${NC}"
if [ ! -d "$TENRANKAI_DIR" ]; then
    echo -e "${RED}✗ Tenrankai directory not found at $TENRANKAI_DIR${NC}"
    exit 1
fi
if [ ! -d "$SITE_DIR" ]; then
    echo -e "${RED}✗ Site directory not found at $SITE_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Directories found${NC}"

# Build Tenrankai
echo -e "\n${YELLOW}2. Building Tenrankai...${NC}"
cd "$TENRANKAI_DIR"
if cargo build --release; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
cd ..

# Check if required files exist
echo -e "\n${YELLOW}3. Checking required files...${NC}"
REQUIRED_FILES=(
    "$SITE_DIR/config.toml"
    "$SITE_DIR/static/DejaVuSans.ttf"
    "$SITE_DIR/templates/pages/index.html.liquid"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ Found: $file${NC}"
    else
        echo -e "${RED}✗ Missing: $file${NC}"
        exit 1
    fi
done

# Start the server
echo -e "\n${YELLOW}4. Starting Tenrankai server...${NC}"
cd "$SITE_DIR"
../$TENRANKAI_DIR/target/release/tenrankai --config config.toml --port $TEST_PORT > server.log 2>&1 &
SERVER_PID=$!
cd ..

# Wait for server to start
echo -e "${YELLOW}   Waiting for server to start...${NC}"
sleep 3

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${RED}✗ Server failed to start. Check $SITE_DIR/server.log for details${NC}"
    tail -20 "$SITE_DIR/server.log"
    exit 1
fi
echo -e "${GREEN}✓ Server started on port $TEST_PORT${NC}"

# Function to test endpoint
test_endpoint() {
    local url=$1
    local description=$2
    local expected_content=$3
    
    echo -e "\n${YELLOW}Testing: $description${NC}"
    echo "  URL: $url"
    
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    http_code=$(echo "$response" | tail -1)
    content=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "  ${GREEN}✓ HTTP $http_code${NC}"
        
        if [ ! -z "$expected_content" ]; then
            if echo "$content" | grep -q "$expected_content"; then
                echo -e "  ${GREEN}✓ Found expected content: '$expected_content'${NC}"
            else
                echo -e "  ${RED}✗ Expected content not found: '$expected_content'${NC}"
                return 1
            fi
        fi
    else
        echo -e "  ${RED}✗ HTTP $http_code${NC}"
        return 1
    fi
}

# Run tests
echo -e "\n${YELLOW}5. Running endpoint tests...${NC}"

# Test homepage
test_endpoint "http://localhost:$TEST_PORT/" "Homepage" "Tenrankai"

# Test features page
test_endpoint "http://localhost:$TEST_PORT/features" "Features page" "Features"

# Test about page
test_endpoint "http://localhost:$TEST_PORT/about" "About page" "About Tenrankai"

# Test gallery
test_endpoint "http://localhost:$TEST_PORT/gallery" "Gallery demo" ""

# Test documentation
test_endpoint "http://localhost:$TEST_PORT/docs" "Documentation" "Quick Start Guide"

# Test blog
test_endpoint "http://localhost:$TEST_PORT/blog" "Blog" "Introducing Tenrankai"

# Test static files
test_endpoint "http://localhost:$TEST_PORT/static/style.css" "CSS file" "font-family"

# Test API health
test_endpoint "http://localhost:$TEST_PORT/api/health" "API health check" ""

# Test 404
echo -e "\n${YELLOW}Testing: 404 page${NC}"
echo "  URL: http://localhost:$TEST_PORT/nonexistent"
response=$(curl -s -w "\n%{http_code}" "http://localhost:$TEST_PORT/nonexistent" 2>/dev/null)
http_code=$(echo "$response" | tail -1)
if [ "$http_code" = "404" ]; then
    echo -e "  ${GREEN}✓ HTTP 404 (as expected)${NC}"
else
    echo -e "  ${RED}✗ Expected 404 but got HTTP $http_code${NC}"
fi

# Summary
echo -e "\n${YELLOW}========================================"
echo -e "Test Summary${NC}"
echo -e "${GREEN}✓ All tests passed!${NC}"
echo -e "\nServer log tail:"
tail -10 "$SITE_DIR/server.log"

# Cleanup happens via trap