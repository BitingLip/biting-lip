"""Test registry service imports step by step"""

import sys
import os

# Set up path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'managers', 'model-manager'))

print("Testing imports...")

try:
    print("1. Basic imports...")
    from typing import List, Optional, Union, cast
    import asyncio
    import logging
    print("✓ Basic imports successful")
except Exception as e:
    print(f"✗ Basic imports failed: {e}")
    exit(1)

try:
    print("2. Schema imports...")
    from app.schemas.models import ModelEntry, WorkerInfo
    print("✓ Schema imports successful")
except Exception as e:
    print(f"✗ Schema imports failed: {e}")
    exit(1)

try:
    print("3. ModelRegistry import...")
    from app.models.registry import ModelRegistry
    print("✓ ModelRegistry import successful")
except Exception as e:
    print(f"✗ ModelRegistry import failed: {e}")
    exit(1)

try:
    print("4. PostgreSQLModelRegistry import...")
    from app.models.postgresql_registry import PostgreSQLModelRegistry
    print("✓ PostgreSQLModelRegistry import successful")
except Exception as e:
    print(f"✗ PostgreSQLModelRegistry import failed: {e}")
    exit(1)

print("5. Creating simple class with these imports...")

logger = logging.getLogger(__name__)
RegistryType = Union[ModelRegistry, PostgreSQLModelRegistry]

try:
    class RegistryService:
        def __init__(self, registry: RegistryType):
            self.registry = registry
            logger.info("RegistryService adapter initialized")

        def _is_postgresql_registry(self) -> bool:
            return isinstance(self.registry, PostgreSQLModelRegistry)
    
    print("✓ RegistryService class created successfully")
    print(f"Class: {RegistryService}")
    
except Exception as e:
    print(f"✗ RegistryService class creation failed: {e}")
    import traceback
    traceback.print_exc()
