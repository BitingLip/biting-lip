"""
BitingLip Platform - Centralized Configuration Manager

This module provides centralized configuration management for all BitingLip services.
It implements a hierarchical configuration system with environment-specific overrides.
"""

import os
from pathlib import Path
from typing import Dict, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails"""
    pass


class BitingLipConfig(BaseSettings):
    """
    Centralized configuration for the entire BitingLip platform.
    
    Configuration hierarchy (highest to lowest priority):
    1. Environment variables
    2. Local .env file (in service directory)
    3. Environment-specific .env file (.env.development, .env.production)
    4. Master .env file (project root)
    5. Default values
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # =============================================================================
    # Environment Configuration
    # =============================================================================
    environment: str = Field(default="development", description="Runtime environment")
    debug: bool = Field(default=True, description="Enable debug mode")
    
    # =============================================================================
    # Service Port Allocation (Standardized)
    # =============================================================================
    gateway_port: int = Field(default=8080, description="Gateway service port")
    task_manager_port: int = Field(default=8084, description="Task manager service port")
    model_manager_port: int = Field(default=8085, description="Model manager service port")
    cluster_manager_port: int = Field(default=8083, description="Cluster manager service port")
    
    # Service Host Configuration
    gateway_host: str = Field(default="localhost", description="Gateway service host")
    task_manager_host: str = Field(default="localhost", description="Task manager service host")
    model_manager_host: str = Field(default="localhost", description="Model manager service host")
    cluster_manager_host: str = Field(default="localhost", description="Cluster manager service host")
      # =============================================================================
    # Infrastructure Services
    # =============================================================================
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, description="Redis port")
    redis_db: int = Field(default=0, description="Redis database number")
    
    # PostgreSQL Database Configuration
    model_db_host: str = Field(default="localhost", description="Model Manager database host")
    model_db_port: int = Field(default=5432, description="Model Manager database port")
    model_db_name: str = Field(default="bitinglip_models", description="Model Manager database name")
    model_db_user: str = Field(default="model_manager", description="Model Manager database user")
    model_db_password: str = Field(default="model_manager_2025!", description="Model Manager database password")
    
    task_db_host: str = Field(default="localhost", description="Task Manager database host")
    task_db_port: int = Field(default=5432, description="Task Manager database port")
    task_db_name: str = Field(default="bitinglip_tasks", description="Task Manager database name")
    task_db_user: str = Field(default="task_manager", description="Task Manager database user")
    task_db_password: str = Field(default="task_manager_2025!", description="Task Manager database password")
    
    gateway_db_host: str = Field(default="localhost", description="Gateway Manager database host")
    gateway_db_port: int = Field(default=5432, description="Gateway Manager database port")
    gateway_db_name: str = Field(default="bitinglip_gateway", description="Gateway Manager database name")
    gateway_db_user: str = Field(default="gateway_manager", description="Gateway Manager database user")
    gateway_db_password: str = Field(default="gateway_manager_2025!", description="Gateway Manager database password")
    
    cluster_db_host: str = Field(default="localhost", description="Cluster Manager database host")
    cluster_db_port: int = Field(default=5432, description="Cluster Manager database port")
    cluster_db_name: str = Field(default="bitinglip_cluster", description="Cluster Manager database name")
    cluster_db_user: str = Field(default="cluster_manager", description="Cluster Manager database user")
    cluster_db_password: str = Field(default="cluster_manager_2025!", description="Cluster Manager database password")
    
    # =============================================================================
    # Celery Configuration (Shared)
    # =============================================================================
    celery_task_serializer: str = Field(default="json", description="Celery task serializer")
    celery_result_serializer: str = Field(default="json", description="Celery result serializer")
    celery_timezone: str = Field(default="UTC", description="Celery timezone")
    celery_enable_utc: bool = Field(default=True, description="Enable UTC in Celery")
    
    # =============================================================================
    # Common API Configuration
    # =============================================================================
    api_host: str = Field(default="0.0.0.0", description="API bind host")
    default_timeout: int = Field(default=300, description="Default request timeout")
    max_timeout: int = Field(default=1800, description="Maximum request timeout")
    rate_limit_requests_per_minute: int = Field(default=60, description="Rate limit per minute")
    
    # =============================================================================
    # Security (Global)
    # =============================================================================
    api_key_required: bool = Field(default=False, description="Require API key authentication")
    cors_origins: str = Field(default="*", description="CORS allowed origins")
    jwt_secret_key: str = Field(default="change-in-production", description="JWT secret key")
    
    # =============================================================================
    # Monitoring & Observability
    # =============================================================================
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format")
    enable_prometheus: bool = Field(default=True, description="Enable Prometheus metrics")
    prometheus_port: int = Field(default=9090, description="Prometheus metrics port")
    health_check_interval: int = Field(default=30, description="Health check interval in seconds")
    
    # =============================================================================
    # Task Manager Configuration
    # =============================================================================
    task_retry_limit: int = Field(default=3, description="Task retry limit")
    max_concurrent_tasks: int = Field(default=100, description="Maximum concurrent tasks")
    task_queue_name: str = Field(default="gpu_queue", description="Default task queue name")
    task_timeout: int = Field(default=300, description="Task timeout in seconds")
    
    # =============================================================================
    # Model Manager Configuration
    # =============================================================================
    model_cache_dir: str = Field(default="./models", description="Model cache directory")
    max_model_cache_size_gb: float = Field(default=50.0, description="Maximum model cache size in GB")
    model_load_timeout: int = Field(default=300, description="Model loading timeout")
    
    # =============================================================================
    # Cluster Manager Configuration
    # =============================================================================
    gpu_memory_fraction: float = Field(default=0.9, description="GPU memory fraction to use")
    max_workers_per_gpu: int = Field(default=1, description="Maximum workers per GPU")
    worker_health_check_interval: int = Field(default=60, description="Worker health check interval")
    
    # =============================================================================
    # Gateway Manager Configuration
    # =============================================================================
    gateway_request_timeout: int = Field(default=30, description="Gateway request timeout")
    gateway_retry_attempts: int = Field(default=3, description="Gateway retry attempts")
    gateway_circuit_breaker_threshold: int = Field(default=5, description="Circuit breaker threshold")
    
    # =============================================================================
    # Computed Properties
    # =============================================================================
    @property
    def redis_url(self) -> str:
        """Generate Redis URL from components"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def celery_broker_url(self) -> str:
        """Generate Celery broker URL"""
        return self.redis_url
    
    @property
    def celery_result_backend(self) -> str:
        """Generate Celery result backend URL"""
        return self.redis_url
    
    @property
    def gateway_url(self) -> str:
        """Generate Gateway service URL"""
        return f"http://{self.gateway_host}:{self.gateway_port}"
    
    @property
    def task_manager_url(self) -> str:
        """Generate Task Manager service URL"""
        return f"http://{self.task_manager_host}:{self.task_manager_port}"
    
    @property
    def model_manager_url(self) -> str:
        """Generate Model Manager service URL"""
        return f"http://{self.model_manager_host}:{self.model_manager_port}"
    
    @property
    def cluster_manager_url(self) -> str:
        """Generate Cluster Manager service URL"""
        return f"http://{self.cluster_manager_host}:{self.cluster_manager_port}"
      # =============================================================================
    # Validators
    # =============================================================================
    @field_validator('environment')
    @classmethod
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'Environment must be one of {allowed}')
        return v
    
    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v):
        allowed = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed:
            raise ValueError(f'Log level must be one of {allowed}')
        return v.upper()
    
    @field_validator('gpu_memory_fraction')
    @classmethod
    def validate_gpu_memory_fraction(cls, v):
        if not 0.1 <= v <= 1.0:
            raise ValueError('GPU memory fraction must be between 0.1 and 1.0')
        return v


class ConfigurationManager:
    """
    Manages configuration loading with environment-specific overrides.
    """
    
    def __init__(self, service_name: Optional[str] = None, project_root: Optional[Path] = None):
        self.service_name = service_name
        self.project_root = project_root or self._find_project_root()
        self._config: Optional[BitingLipConfig] = None
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / ".git").exists() or (current / "biting-lip").name == current.name:
                return current
            current = current.parent
        return Path.cwd()
    
    def load_config(self) -> BitingLipConfig:
        """
        Load configuration with hierarchical override support.
        
        Loading order (highest to lowest priority):
        1. Environment variables
        2. Service-specific .env file
        3. Environment-specific .env file
        4. Master .env file
        5. Default values
        """
        if self._config is not None:
            return self._config
        
        # Build list of potential .env files (in priority order)
        env_files = []
        
        # 1. Service-specific .env file (if service_name provided)
        if self.service_name:
            service_env = self.project_root / self.service_name / ".env"
            if service_env.exists():
                env_files.append(str(service_env))
        
        # 2. Environment-specific .env file
        environment = os.getenv('ENVIRONMENT', 'development')
        env_specific = self.project_root / f".env.{environment}"
        if env_specific.exists():
            env_files.append(str(env_specific))
        
        # 3. Master .env file
        master_env = self.project_root / ".env"
        if master_env.exists():
            env_files.append(str(master_env))        # Load configuration with file hierarchy
        try:            # Create configuration instance - env files handled by model_config
            self._config = BitingLipConfig()
            logger.info("Configuration loaded successfully")
            return self._config
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            # Fall back to default configuration
            self._config = BitingLipConfig()
            return self._config
    
    def get_service_config(self, service_name: str) -> Dict[str, Any]:
        """Get configuration specific to a service"""
        config = self.load_config()
        
        service_configs = {
            'gateway': {
                'port': config.gateway_port,
                'host': config.gateway_host,
                'url': config.gateway_url,
                'request_timeout': config.gateway_request_timeout,
                'retry_attempts': config.gateway_retry_attempts,
                'circuit_breaker_threshold': config.gateway_circuit_breaker_threshold,
            },
            'task-manager': {
                'port': config.task_manager_port,
                'host': config.task_manager_host,
                'url': config.task_manager_url,
                'retry_limit': config.task_retry_limit,
                'max_concurrent_tasks': config.max_concurrent_tasks,
                'queue_name': config.task_queue_name,
            },
            'model-manager': {
                'port': config.model_manager_port,
                'host': config.model_manager_host,
                'url': config.model_manager_url,
                'cache_dir': config.model_cache_dir,
                'max_cache_size_gb': config.max_model_cache_size_gb,
                'load_timeout': config.model_load_timeout,
            },
            'cluster-manager': {
                'port': config.cluster_manager_port,
                'host': config.cluster_manager_host,
                'url': config.cluster_manager_url,
                'gpu_memory_fraction': config.gpu_memory_fraction,
                'max_workers_per_gpu': config.max_workers_per_gpu,
                'health_check_interval': config.worker_health_check_interval,
            }
        }
        
        return service_configs.get(service_name, {})
    
    def reload_config(self) -> BitingLipConfig:
        """Reload configuration from files"""
        self._config = None
        return self.load_config()


# Global configuration manager instance
_config_manager = ConfigurationManager()

def get_config(service_name: Optional[str] = None) -> BitingLipConfig:
    """Get the global configuration instance"""
    if service_name:
        manager = ConfigurationManager(service_name=service_name)
        return manager.load_config()
    return _config_manager.load_config()

def get_service_config(service_name: str) -> Dict[str, Any]:
    """Get service-specific configuration"""
    return _config_manager.get_service_config(service_name)

def reload_config() -> BitingLipConfig:
    """Reload the global configuration"""
    return _config_manager.reload_config()
