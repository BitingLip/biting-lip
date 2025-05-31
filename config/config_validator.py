#!/usr/bin/env python3
"""
Enhanced Configuration Validation System

Provides comprehensive validation for the centralized configuration setup,
with better error reporting and performance optimizations.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import logging

# Add config to path
config_dir = Path(__file__).parent
sys.path.insert(0, str(config_dir))

from .central_config import ConfigurationManager, ConfigurationError

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when configuration validation fails"""
    pass


@dataclass
class ValidationResult:
    """Result of configuration validation with enhanced reporting"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    port_conflicts: List[Tuple[str, int]]
    missing_files: List[str]
    performance_issues: List[str]
    
    def __str__(self) -> str:
        """Human-readable validation summary"""
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        lines = [f"Configuration Validation: {status}"]
        
        if self.errors:
            lines.append(f"\n🚨 ERRORS ({len(self.errors)}):")
            for error in self.errors:
                lines.append(f"  - {error}")
        
        if self.warnings:
            lines.append(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        
        if self.port_conflicts:
            lines.append(f"\n🔌 PORT CONFLICTS ({len(self.port_conflicts)}):")
            for service, port in self.port_conflicts:
                lines.append(f"  - {service}: {port}")
        
        if self.performance_issues:
            lines.append(f"\n⚡ PERFORMANCE ISSUES ({len(self.performance_issues)}):")
            for issue in self.performance_issues:
                lines.append(f"  - {issue}")
        
        return "\n".join(lines)


class ConfigValidator:
    """Enhanced configuration validator with better error handling"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.config_dir = self.project_root / "config"
        self.required_files = [
            "central_config.py",
            "service_discovery.py",
            "__init__.py"
        ]
        self.service_ports = {
            'gateway': 8080,
            'cluster-manager': 8083,
            'task-manager': 8084,
            'model-manager': 8085
        }
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / ".git").exists() or (current / "biting-lip").name == current.name:
                return current
            current = current.parent
        return Path.cwd()
    
    def validate_all(self) -> ValidationResult:
        """Run comprehensive validation with enhanced reporting"""
        errors = []
        warnings = []
        port_conflicts = []
        missing_files = []
        performance_issues = []
        
        try:
            # 1. File structure validation
            structure_issues = self._validate_file_structure()
            missing_files.extend(structure_issues)
            
            # 2. Configuration loading validation
            config_issues = self._validate_configuration_loading()
            errors.extend(config_issues)
            
            # 3. Port conflict detection
            conflicts = self._detect_port_conflicts()
            port_conflicts.extend(conflicts)
            
            # 4. Performance analysis
            perf_issues = self._analyze_performance()
            performance_issues.extend(perf_issues)
            
            # 5. Environment validation
            env_warnings = self._validate_environment_setup()
            warnings.extend(env_warnings)
            
            # 6. Security validation
            security_warnings = self._validate_security_settings()
            warnings.extend(security_warnings)
            
        except Exception as e:
            errors.append(f"Validation failed with exception: {str(e)}")
        
        is_valid = len(errors) == 0 and len(missing_files) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            port_conflicts=port_conflicts,
            missing_files=missing_files,
            performance_issues=performance_issues
        )
    
    def _validate_file_structure(self) -> List[str]:
        """Validate that all required configuration files exist"""
        missing = []
        
        for file_name in self.required_files:
            file_path = self.config_dir / file_name
            if not file_path.exists():
                missing.append(f"Missing required file: {file_path}")
        
        return missing
    
    def _validate_configuration_loading(self) -> List[str]:
        """Test configuration loading and validation"""
        errors = []
        
        try:
            config_manager = ConfigurationManager()
            config = config_manager.load_config()
            
            # Test service configurations
            services = ['gateway', 'task-manager', 'model-manager', 'cluster-manager']
            for service in services:
                try:
                    service_config = config_manager.get_service_config(service)
                    if not service_config:
                        errors.append(f"Empty configuration for service: {service}")
                except Exception as e:
                    errors.append(f"Failed to load {service} config: {str(e)}")
            
        except Exception as e:
            errors.append(f"Configuration loading failed: {str(e)}")
        
        return errors
    
    def _detect_port_conflicts(self) -> List[Tuple[str, int]]:
        """Detect port conflicts between services"""
        conflicts = []
        used_ports = set()
        
        for service, port in self.service_ports.items():
            if port in used_ports:
                conflicts.append((service, port))
            used_ports.add(port)
        
        return conflicts
    
    def _analyze_performance(self) -> List[str]:
        """Analyze configuration for performance issues"""
        issues = []
        
        try:
            config_manager = ConfigurationManager()
            config = config_manager.load_config()
            
            # Check for performance-impacting settings
            if config.default_timeout > 600:  # 10 minutes
                issues.append(f"High default timeout: {config.default_timeout}s")
            
            if config.max_concurrent_tasks > 1000:
                issues.append(f"Very high concurrent task limit: {config.max_concurrent_tasks}")
            
            if config.model_load_timeout < 60:
                issues.append(f"Low model load timeout may cause failures: {config.model_load_timeout}s")
            
        except Exception as e:
            issues.append(f"Performance analysis failed: {str(e)}")
        
        return issues
    
    def _validate_environment_setup(self) -> List[str]:
        """Validate environment-specific settings"""
        warnings = []
        
        env_file = self.project_root / ".env"
        if not env_file.exists():
            warnings.append("Master .env file not found")
        
        environment = os.getenv('ENVIRONMENT', 'development')
        if environment == 'production':
            # Production-specific validations
            jwt_secret = os.getenv('JWT_SECRET_KEY', 'change-in-production')
            if jwt_secret == 'change-in-production':
                warnings.append("Using default JWT secret in production")
        
        return warnings
    
    def _validate_security_settings(self) -> List[str]:
        """Validate security-related configuration"""
        warnings = []
        
        try:
            config_manager = ConfigurationManager()
            config = config_manager.load_config()
            
            if config.cors_origins == "*":
                warnings.append("CORS origins set to wildcard (*) - security risk")
            
            if not config.api_key_required and config.environment == 'production':
                warnings.append("API key authentication disabled in production")
            
        except Exception as e:
            warnings.append(f"Security validation failed: {str(e)}")
        
        return warnings


def validate_configuration(project_root: Optional[Path] = None) -> ValidationResult:
    """Convenience function to validate configuration"""
    validator = ConfigValidator(project_root)
    return validator.validate_all()


if __name__ == "__main__":
    # CLI interface for validation
    print("🔍 BitingLip Configuration Validation")
    print("=" * 50)
    
    result = validate_configuration()
    print(result)
    
    if not result.is_valid:
        sys.exit(1)
    else:
        print("\n🎉 Configuration validation passed!")
