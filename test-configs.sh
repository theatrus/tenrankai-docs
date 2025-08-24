#!/bin/bash
# Test that all config files work with Tenrankai

set -e

echo "Testing Tenrankai configuration files"
echo "===================================="

# Test each config
for config in config.toml config.dev.toml; do
    echo -e "\nTesting $config..."
    cd tenrankai-dot-com
    ../tenrankai/target/release/tenrankai --config $config --quit-after 3 > test-$config.log 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✓ $config works"
        # Show key lines from log
        grep -E "(Starting|Server listening|All startup checks passed)" test-$config.log | head -5
    else
        echo "✗ $config failed"
        tail -20 test-$config.log
    fi
    
    cd ..
done

# Test production config (expect failures)
echo -e "\nTesting config.production.toml (expect path errors)..."
cd tenrankai-dot-com
../tenrankai/target/release/tenrankai --config config.production.toml --quit-after 1 > test-production.log 2>&1 || true
echo "Production config parse test:"
grep -E "(Configuration loaded|missing|does not exist)" test-production.log | head -10
cd ..

echo -e "\n✓ Config tests complete"