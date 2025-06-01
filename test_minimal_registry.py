"""
Minimal Registry Service Test
"""

from typing import List, Optional, Union, cast
import asyncio
import logging

# Dummy imports to test
class DummyModelEntry:
    pass

class DummyWorkerInfo:
    pass

class DummyModelRegistry:
    pass

class DummyPostgreSQLModelRegistry:
    pass

logger = logging.getLogger(__name__)

# Type alias for any registry implementation
RegistryType = Union[DummyModelRegistry, DummyPostgreSQLModelRegistry]


class RegistryService:
    """Adapter service for ModelRegistry with async interface"""
    
    def __init__(self, registry: RegistryType):
        self.registry = registry
        logger.info("RegistryService adapter initialized")

    def _is_postgresql_registry(self) -> bool:
        """Check if using PostgreSQL registry"""
        return isinstance(self.registry, DummyPostgreSQLModelRegistry)
    
    def test_method(self):
        return "test"


if __name__ == "__main__":
    print("RegistryService defined successfully")
    service = RegistryService(DummyModelRegistry())
    print("RegistryService instantiated successfully")
