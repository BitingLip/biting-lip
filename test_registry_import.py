#!/usr/bin/env python3
"""Test registry service import in isolation"""

import sys
import os

# Add the model-manager to Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'managers', 'model-manager'))

try:
    print("Testing imports...")
    from app.schemas.models import ModelEntry, WorkerInfo
    print("✅ Schema imports OK")
    
    from app.models.registry import ModelRegistry
    print("✅ SQLite registry import OK")
    
    from app.models.postgresql_registry import PostgreSQLModelRegistry
    print("✅ PostgreSQL registry import OK")
    
    # Now try to import the registry service directly
    from app.services.registry_service import RegistryService
    print("✅ RegistryService import OK")
    
    print("🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
