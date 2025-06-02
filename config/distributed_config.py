"""
BitingLip Platform - Distributed Configuration Loader

This module provides configuration loading for the new microservice architecture
where each service manages its own configuration files.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Any, List
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class DistributedConfigLoader:
    """
    Loads configuration from distributed service directories with fallback to central config.
    
    Configuration loading order (highest to lowest priority):
    1. Environment variables
    2. Service-specific local.env (for development overrides)
    3. Service-specific configuration files
    4. Central platform configuration
    5. Default values
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize the distributed config loader"""
        self.project_root = project_root or self._find_project_root()
        self.central_config_dir = self.project_root / "config"
        self.managers_dir = self.project_root / "managers"
        self.interfaces_dir = self.project_root / "interfaces"
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "requirements.txt").exists() or (current / "pyproject.toml").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def load_service_config(self, service_name: str, service_type: str = "manager") -> Dict[str, Any]:
        """
        Load configuration for a specific service.
        
        Args:
            service_name: Name of the service (e.g., 'model-manager')
            service_type: Type of service ('manager', 'interface', 'worker')
        
        Returns:
            Dictionary containing all configuration values
        """
        config = {}
        
        # 1. Load central platform configuration first (lowest priority)
        config.update(self._load_central_config())
        
        # 2. Load service-specific configuration
        service_config = self._load_service_specific_config(service_name, service_type)
        config.update(service_config)
        
        # 3. Load local development overrides (highest priority)
        local_config = self._load_local_overrides(service_name, service_type)
        config.update(local_config)
        
        # 4. Environment variables override everything
        config.update(self._get_env_overrides())
        
        logger.info(f"Loaded configuration for {service_type} '{service_name}' with {len(config)} settings")
        return config
    
    def _load_central_config(self) -> Dict[str, Any]:
        """Load central platform configuration"""
        config = {}
        
        # Load environment-specific config
        env = os.getenv('BITINGLIP_ENV', 'development')
        env_files = [
            self.central_config_dir / "environments" / "base.env",
            self.central_config_dir / "environments" / f"{env}.env"
        ]
        
        for env_file in env_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)
                config.update(self._read_env_file(env_file))
                logger.debug(f"Loaded central config from {env_file}")
        
        return config
    
    def _load_service_specific_config(self, service_name: str, service_type: str) -> Dict[str, Any]:
        """Load service-specific configuration files"""
        config = {}
        
        # Determine service directory
        if service_type == "manager":
            service_dir = self.managers_dir / service_name / "config"
        elif service_type == "interface":
            service_dir = self.interfaces_dir / service_name / "config"
        elif service_type == "worker":
            service_dir = self.managers_dir / "cluster-manager" / "config" / "workers"
        else:
            logger.warning(f"Unknown service type: {service_type}")
            return config
        
        if not service_dir.exists():
            logger.warning(f"Service config directory not found: {service_dir}")
            return config
        
        # Load service configuration files
        service_env_files = [
            service_dir / f"{service_name}.env",
            service_dir / f"{service_name}-db.env"
        ]
        
        for env_file in service_env_files:
            if env_file.exists():
                load_dotenv(env_file, override=False)
                config.update(self._read_env_file(env_file))
                logger.debug(f"Loaded service config from {env_file}")
        
        return config
    
    def _load_local_overrides(self, service_name: str, service_type: str) -> Dict[str, Any]:
        """Load local development overrides"""
        config = {}
        
        # Determine service directory
        if service_type == "manager":
            service_dir = self.managers_dir / service_name / "config"
        elif service_type == "interface":
            service_dir = self.interfaces_dir / service_name / "config"
        elif service_type == "worker":
            service_dir = self.managers_dir / "cluster-manager" / "config" / "workers"
        else:
            return config
        
        local_env_file = service_dir / "local.env"
        if local_env_file.exists():
            load_dotenv(local_env_file, override=True)
            config.update(self._read_env_file(local_env_file))
            logger.debug(f"Loaded local overrides from {local_env_file}")
        
        return config
    
    def _get_env_overrides(self) -> Dict[str, Any]:
        """Get environment variable overrides"""
        # This would typically filter environment variables by prefix
        # For now, we'll let dotenv handle this
        return {}
    
    def _read_env_file(self, env_file: Path) -> Dict[str, Any]:
        """Read environment file and return as dictionary"""
        config = {}
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
        except Exception as e:
            logger.error(f"Error reading {env_file}: {e}")
        
        return config
    
    def load_infrastructure_config(self) -> Dict[str, Any]:
        """Load platform-wide infrastructure configuration"""
        config = {}
        
        infrastructure_dir = self.central_config_dir / "infrastructure"
        if infrastructure_dir.exists():
            for env_file in infrastructure_dir.glob("*.env"):
                load_dotenv(env_file, override=False)
                config.update(self._read_env_file(env_file))
                logger.debug(f"Loaded infrastructure config from {env_file}")
        
        return config
    
    def get_service_list(self) -> List[str]:
        """Get list of all available services"""
        services = []
        
        # Manager services
        if self.managers_dir.exists():
            for manager_dir in self.managers_dir.iterdir():
                if manager_dir.is_dir() and (manager_dir / "config").exists():
                    services.append(f"manager:{manager_dir.name}")
        
        # Interface services
        if self.interfaces_dir.exists():
            for interface_dir in self.interfaces_dir.iterdir():
                if interface_dir.is_dir() and (interface_dir / "config").exists():
                    services.append(f"interface:{interface_dir.name}")
        
        return services


# Global instance for easy access
_config_loader = None

def get_config_loader() -> DistributedConfigLoader:
    """Get the global configuration loader instance"""
    global _config_loader
    if _config_loader is None:
        _config_loader = DistributedConfigLoader()
    return _config_loader


def load_service_config(service_name: str, service_type: str = "manager") -> Dict[str, Any]:
    """Convenience function to load service configuration"""
    loader = get_config_loader()
    return loader.load_service_config(service_name, service_type)


def load_infrastructure_config() -> Dict[str, Any]:
    """Convenience function to load infrastructure configuration"""
    loader = get_config_loader()
    return loader.load_infrastructure_config()
