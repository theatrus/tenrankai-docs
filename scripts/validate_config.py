#!/usr/bin/env python3
"""Validate Tenrankai TOML configuration files.

Requires: pip install toml
"""

import sys
import os
import toml

configs = [
    "tenrankai-dot-com/config.toml",
    "tenrankai-dot-com/config.dev.toml",
    "tenrankai-dot-com/config.production.toml",
]

exit_code = 0

for config in configs:
    try:
        with open(config, "r") as f:
            data = toml.load(f)
        print(f"✓ {config} is valid TOML")

        # Check required sections - server and app are always required
        for section in ["server", "app"]:
            if section not in data:
                print(f"✗ {config} missing required section: {section}")
                exit_code = 1

        # ConfigStorage configs use config_storage instead of inline sections
        if "config_storage" in data.get("app", {}):
            storage_path = data["app"]["config_storage"]
            config_dir = os.path.dirname(config)
            full_path = os.path.join(config_dir, storage_path)
            if os.path.isdir(full_path):
                print(f"  ✓ ConfigStorage directory exists: {storage_path}")
            else:
                print(f"  ⚠ ConfigStorage directory not found: {full_path}")
        else:
            # Legacy config - check for inline sections
            for section in ["templates", "static_files"]:
                if section not in data:
                    print(f"✗ {config} missing required section: {section}")
                    exit_code = 1
    except FileNotFoundError:
        print(f"✗ {config} not found")
        exit_code = 1
    except Exception as e:
        print(f"✗ {config} failed validation: {e}")
        exit_code = 1

sys.exit(exit_code)
