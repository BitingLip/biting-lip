#!/usr/bin/env python3
"""Debug script to identify the import issue"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'managers', 'model-manager'))

print("Testing imports step by step...")

print("1. Testing basic imports...")
try:
    from typing import List, Optional, Union, cast
    import asyncio
    import logging
    print("✓ Basic imports successful")
except Exception as e:
    print(f"✗ Basic imports failed: {e}")
    sys.exit(1)

print("2. Testing schema imports...")
try:
    from app.schemas.models import ModelEntry, WorkerInfo
    print("✓ Schema imports successful")
except Exception as e:
    print(f"✗ Schema imports failed: {e}")
    sys.exit(1)

print("3. Testing registry imports...")
try:
    from app.models.registry import ModelRegistry
    print("✓ ModelRegistry import successful")
except Exception as e:
    print(f"✗ ModelRegistry import failed: {e}")
    sys.exit(1)

try:
    from app.models.postgresql_registry import PostgreSQLModelRegistry
    print("✓ PostgreSQLModelRegistry import successful")
except Exception as e:
    print(f"✗ PostgreSQLModelRegistry import failed: {e}")
    sys.exit(1)

print("4. Testing registry_service file parsing...")
try:
    with open('managers/model-manager/app/services/registry_service.py', 'r') as f:
        content = f.read()
    
    # Check if RegistryService class is defined
    if 'class RegistryService:' in content:
        print("✓ RegistryService class definition found in file")
        # Count lines in class
        lines = content.split('\n')
        class_start = -1
        for i, line in enumerate(lines):
            if 'class RegistryService:' in line:
                class_start = i
                break
        
        if class_start >= 0:
            indent_level = 0
            for i in range(class_start + 1, len(lines)):
                line = lines[i]
                if line.strip() == '':
                    continue
                current_indent = len(line) - len(line.lstrip())
                if current_indent == 0 and line.strip():
                    # End of class
                    break
                if indent_level == 0 and line.strip():
                    indent_level = current_indent
            
            print(f"Class definition spans lines {class_start + 1} to {i}")
    else:
        print("✗ RegistryService class definition not found in file")
        
except Exception as e:
    print(f"✗ Error reading registry_service file: {e}")

print("5. Testing module import...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'registry_service', 
        'managers/model-manager/app/services/registry_service.py'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    print("✓ Module execution successful")
    print(f"Available attributes: {[attr for attr in dir(module) if not attr.startswith('_')]}")
    
    if hasattr(module, 'RegistryService'):
        print("✓ RegistryService class available")
    else:
        print("✗ RegistryService class not available after module execution")
        
except Exception as e:
    print(f"✗ Module import failed: {e}")
    import traceback
    traceback.print_exc()
