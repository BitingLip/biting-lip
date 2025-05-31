"""
BitingLip Platform - Service Discovery

Provides service URL resolution and health checking capabilities.
"""

import httpx
from typing import Dict, Optional, List, Tuple
import asyncio
import logging

try:
    from .central_config import get_config
except ImportError:
    from central_config import get_config

logger = logging.getLogger(__name__)


class ServiceDiscoveryError(Exception):
    """Raised when service discovery operations fail"""
    pass


class ServiceDiscovery:
    """
    Manages service discovery and health checking for BitingLip platform services.
    """
    
    def __init__(self):
        self.config = get_config()
        self._service_cache: Dict[str, str] = {}
        self._health_cache: Dict[str, bool] = {}
    
    def get_service_url(self, service_name: str) -> str:
        """
        Get the URL for a service by name.
        
        Args:
            service_name: Name of the service ('gateway', 'task-manager', etc.)
            
        Returns:
            Service URL
            
        Raises:
            ValueError: If service name is not recognized
        """
        service_urls = {
            'gateway': self.config.gateway_url,
            'gateway-manager': self.config.gateway_url,
            'task-manager': self.config.task_manager_url,
            'model-manager': self.config.model_manager_url,
            'cluster-manager': self.config.cluster_manager_url,
        }
        
        if service_name not in service_urls:
            raise ValueError(f"Unknown service: {service_name}. Available: {list(service_urls.keys())}")
        
        return service_urls[service_name]
    
    def get_all_service_urls(self) -> Dict[str, str]:
        """Get URLs for all known services"""
        return {
            'gateway': self.config.gateway_url,
            'task-manager': self.config.task_manager_url,
            'model-manager': self.config.model_manager_url,
            'cluster-manager': self.config.cluster_manager_url,
        }
    
    async def check_service_health(self, service_name: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
        """
        Check if a service is healthy by calling its health endpoint.
        
        Args:
            service_name: Name of the service
            timeout: Request timeout in seconds
            
        Returns:
            Tuple of (is_healthy, error_message)
        """
        try:
            base_url = self.get_service_url(service_name)
            health_url = f"{base_url}/health"
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.get(health_url)
                
                if response.status_code == 200:
                    self._health_cache[service_name] = True
                    return True, None
                else:
                    error_msg = f"Health check failed with status {response.status_code}"
                    self._health_cache[service_name] = False
                    return False, error_msg
                    
        except httpx.TimeoutException:
            error_msg = f"Health check timeout after {timeout}s"
            self._health_cache[service_name] = False
            return False, error_msg
        except httpx.ConnectError:
            error_msg = "Cannot connect to service"
            self._health_cache[service_name] = False
            return False, error_msg
        except Exception as e:
            error_msg = f"Health check error: {str(e)}"
            self._health_cache[service_name] = False
            return False, error_msg
    
    async def check_all_services_health(self, timeout: int = 5) -> Dict[str, Tuple[bool, Optional[str]]]:
        """
        Check health of all known services concurrently.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            Dictionary mapping service names to (is_healthy, error_message) tuples
        """
        services = ['gateway', 'task-manager', 'model-manager', 'cluster-manager']
        
        # Run health checks concurrently
        tasks = [
            self.check_service_health(service, timeout)
            for service in services
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            service: result if not isinstance(result, Exception) else (False, str(result))
            for service, result in zip(services, results)
        }
    
    def get_healthy_services(self) -> List[str]:
        """Get list of services that are currently healthy (from cache)"""
        return [service for service, is_healthy in self._health_cache.items() if is_healthy]
    
    def get_unhealthy_services(self) -> List[str]:
        """Get list of services that are currently unhealthy (from cache)"""
        return [service for service, is_healthy in self._health_cache.items() if not is_healthy]
    
    async def wait_for_service(self, service_name: str, max_wait: int = 60, check_interval: int = 2) -> bool:
        """
        Wait for a service to become healthy.
        
        Args:
            service_name: Name of the service to wait for
            max_wait: Maximum time to wait in seconds
            check_interval: How often to check in seconds
            
        Returns:
            True if service became healthy, False if timeout
        """
        waited = 0
        while waited < max_wait:
            is_healthy, error = await self.check_service_health(service_name)
            if is_healthy:
                logger.info(f"Service {service_name} is now healthy")
                return True
            
            logger.info(f"Waiting for {service_name} to become healthy: {error}")
            await asyncio.sleep(check_interval)
            waited += check_interval
        
        logger.warning(f"Service {service_name} did not become healthy after {max_wait}s")
        return False
    
    async def wait_for_all_services(self, max_wait: int = 120, check_interval: int = 5) -> bool:
        """
        Wait for all services to become healthy.
        
        Args:
            max_wait: Maximum time to wait in seconds
            check_interval: How often to check in seconds
            
        Returns:
            True if all services became healthy, False if timeout
        """
        waited = 0
        services = ['gateway', 'task-manager', 'model-manager', 'cluster-manager']
        
        while waited < max_wait:
            health_results = await self.check_all_services_health()
            
            healthy_services = [
                service for service, (is_healthy, _) in health_results.items() 
                if is_healthy
            ]
            
            if len(healthy_services) == len(services):
                logger.info("All services are healthy")
                return True
            
            unhealthy = [s for s in services if s not in healthy_services]
            logger.info(f"Waiting for services to become healthy: {unhealthy}")
            
            await asyncio.sleep(check_interval)
            waited += check_interval
        
        logger.warning(f"Not all services became healthy after {max_wait}s")
        return False


# Global service discovery instance
_service_discovery = ServiceDiscovery()

def get_service_url(service_name: str) -> str:
    """Get the URL for a service by name"""
    return _service_discovery.get_service_url(service_name)

def get_all_service_urls() -> Dict[str, str]:
    """Get URLs for all known services"""
    return _service_discovery.get_all_service_urls()

async def check_service_health(service_name: str, timeout: int = 5) -> Tuple[bool, Optional[str]]:
    """Check if a service is healthy"""
    return await _service_discovery.check_service_health(service_name, timeout)

async def check_all_services_health(timeout: int = 5) -> Dict[str, Tuple[bool, Optional[str]]]:
    """Check health of all known services"""
    return await _service_discovery.check_all_services_health(timeout)

async def wait_for_service(service_name: str, max_wait: int = 60) -> bool:
    """Wait for a service to become healthy"""
    return await _service_discovery.wait_for_service(service_name, max_wait)

async def wait_for_all_services(max_wait: int = 120) -> bool:
    """Wait for all services to become healthy"""
    return await _service_discovery.wait_for_all_services(max_wait)
