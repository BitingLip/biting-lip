#!/usr/bin/env python3
"""
Configuration Validation System
Validates the centralized configuration setup and checks for conflicts.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

# Add config to path
config_dir = Path(__file__).parent
sys.path.insert(0, str(config_dir))

from central_config import ConfigurationManager


@dataclass
class ValidationResult:
    """Result of configuration validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    port_conflicts: List[Tuple[str, int]]


class ConfigValidator:
    """Validates centralized configuration system"""
    
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.config_dir = Path(__file__).parent
        
    def validate_all(self) -> ValidationResult:
        """Run all validation checks"""
        errors = []
        warnings = []
        port_conflicts = []
        
        # Check file structure
        structure_errors = self._validate_file_structure()
        errors.extend(structure_errors)
        
        # Check port conflicts
        conflicts = self._check_port_conflicts()
        port_conflicts.extend(conflicts)
        
        # Check environment loading
        env_errors = self._validate_environment_loading()
        errors.extend(env_errors)
        
        # Check service discovery
        discovery_errors = self._validate_service_discovery()
        errors.extend(discovery_errors)
        
        # Check for missing required variables
        missing_vars = self._check_missing_variables()
        warnings.extend([f"Missing variable: {var}" for var in missing_vars])
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            port_conflicts=port_conflicts
        )
    
    def _validate_file_structure(self) -> List[str]:
        """Validate that all required configuration files exist"""
        errors = []
        
        required_files = [
            ".env",
            "config/central_config.py",
            "config/service_discovery.py",
            "config/__init__.py",
            "config/environments/base.env",
            "config/environments/development.env",
            "config/environments/staging.env",
            "config/environments/production.env",
            "config/services/network.env",
            "config/services/storage.env",
            "config/services/gpu.env",
            "config/services/security.env",
            "config/versions.env"
        ]
        
        root_dir = self.config_dir.parent
        
        for file_path in required_files:
            full_path = root_dir / file_path
            if not full_path.exists():
                errors.append(f"Missing required file: {file_path}")
        
        return errors
    
    def _check_port_conflicts(self) -> List[Tuple[str, int]]:
        """Check for port conflicts in configuration"""
        try:
            config = self.config_manager.load_config()
            ports = {}
            conflicts = []
            
            # Collect all port assignments
            service_ports = {
                'gateway': config.gateway_port,
                'cluster': config.cluster_manager_port,
                'task': config.task_manager_port,
                'model': config.model_manager_port
            }
            
            # Check for conflicts
            for service, port in service_ports.items():
                if port in ports:
                    conflicts.append((f"{ports[port]} vs {service}", port))
                else:
                    ports[port] = service
                    
            return conflicts
            
        except Exception as e:
            return [("Error checking ports", 0)]
    
    def _validate_environment_loading(self) -> List[str]:
        """Validate that environments can be loaded"""
        errors = []
        
        environments = ['development', 'staging', 'production']
        
        for env in environments:
            try:
                os.environ['BITINGLIP_ENV'] = env
                config = self.config_manager.load_config()
                # Try to access a basic property
                _ = config.gateway_port
            except Exception as e:
                errors.append(f"Failed to load {env} environment: {str(e)}")
        
        # Reset to development
        os.environ['BITINGLIP_ENV'] = 'development'
        
        return errors
    
    def _validate_service_discovery(self) -> List[str]:
        """Validate service discovery functionality"""
        errors = []
        
        try:
            from service_discovery import ServiceDiscovery
            discovery = ServiceDiscovery()
            
            # Test service URL resolution
            services = ['gateway', 'cluster-manager', 'task-manager', 'model-manager']
            for service in services:
                try:
                    url = discovery.get_service_url(service)
                    if not url:
                        errors.append(f"Service discovery failed for: {service}")
                except Exception as e:
                    errors.append(f"Service discovery error for {service}: {str(e)}")
                    
        except Exception as e:
            errors.append(f"Service discovery system error: {str(e)}")
        
        return errors
    
    def _check_missing_variables(self) -> List[str]:
        """Check for missing required configuration variables"""
        missing = []
        
        try:
            config = self.config_manager.load_config()
            
            # Check required variables
            required_vars = [
                'app_name', 'app_version', 'environment',
                'gateway_port', 'cluster_manager_port', 
                'task_manager_port', 'model_manager_port'
            ]
            
            for var in required_vars:
                if not hasattr(config, var) or getattr(config, var) is None:
                    missing.append(var)
                    
        except Exception as e:
            missing.append(f"Config loading error: {str(e)}")
        
        return missing


def main():
    """Run configuration validation"""
    print("🔍 Validating BitingLip Centralized Configuration...")
    print("=" * 60)
    
    validator = ConfigValidator()
    result = validator.validate_all()
    
    if result.is_valid:
        print("✅ Configuration validation PASSED!")
    else:
        print("❌ Configuration validation FAILED!")
        
    if result.errors:
        print(f"\n🚨 Errors ({len(result.errors)}):")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.port_conflicts:
        print(f"\n⚠️  Port Conflicts ({len(result.port_conflicts)}):")
        for conflict, port in result.port_conflicts:
            print(f"  - Port {port}: {conflict}")
    
    if result.warnings:
        print(f"\n⚠️  Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if result.is_valid and not result.warnings:
        print("\n🎉 All configuration checks passed!")
        print("The centralized configuration system is ready for deployment.")
    
    return 0 if result.is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
