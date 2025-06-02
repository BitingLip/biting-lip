"""
BitingLip Platform Configuration Package

Enhanced centralized configuration management with:
- Type safety and validation
- Performance optimizations  
- Better error handling
- Improved naming conventions
"""

from .central_config import (
    BitingLipConfig,
    ConfigurationManager,
    get_config,
    get_service_config,
    reload_config,
    ConfigurationError
)

from .distributed_config import (
    load_service_config,
    load_infrastructure_config,
    get_config_loader
)

from .service_discovery import (
    ServiceDiscovery,
    get_service_url,
    get_all_service_urls,
    check_service_health,
    check_all_services_health,
    wait_for_service,
    wait_for_all_services
)




# Version info
__version__ = "2.0.0"
__author__ = "BitingLip Platform Team"

# Public API
__all__ = [
    # Core configuration
    'BitingLipConfig',
    'ConfigurationManager', 
    'get_config',
    'get_service_config',
    'reload_config',
    'ConfigurationError',

    # Distributed configuration
    'load_service_config',
    'load_infrastructure_config',
    'get_config_loader',
    
    # Service discovery
    'ServiceDiscovery',
    'get_service_url',
    'get_all_service_urls',
    'check_service_health',
    'check_all_services_health',
    'wait_for_service',
    'wait_for_all_services'
]
