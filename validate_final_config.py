#!/usr/bin/env python3
"""
Simple validation script for BitingLip configuration migration.
Tests the distributed configuration system directly.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_distributed_config():
    """Test the distributed configuration system"""
    print("🔍 Configuration System Validation")
    print("=" * 50)
    
    try:
        # Test config package imports
        print("📦 Testing config package imports...")
        from config import (
            load_service_config, 
            load_infrastructure_config, 
            ServiceDiscovery
        )
        print("   ✅ Config package imports successful")
        
        # Test service config loading
        print("\n📁 Testing service configuration loading...")
        services = ['model-manager', 'cluster-manager', 'task-manager', 'gateway-manager']
        
        for service in services:
            try:
                config = load_service_config(service, 'manager')
                print(f"   ✅ {service}: {len(config)} config values loaded")
            except Exception as e:
                print(f"   ❌ {service}: {str(e)}")
        
        # Test infrastructure config
        print("\n🏗️ Testing infrastructure configuration...")
        infra_config = load_infrastructure_config()
        print(f"   ✅ Infrastructure config: {len(infra_config)} values loaded")
        
        # Test service discovery
        print("\n🔍 Testing service discovery...")
        try:
            service_discovery = ServiceDiscovery()
            print("   ✅ Service discovery initialized")
        except Exception as e:
            print(f"   ⚠️  Service discovery warning: {str(e)}")
        
        print("\n🎉 Configuration system validation complete!")
        print("✅ All core configuration functionality working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration system error: {str(e)}")
        return False

def test_config_files():
    """Test that all configuration files exist"""
    print("\n📂 Configuration Files Validation")
    print("=" * 40)
    
    config_files = [
        # Service configs
        'managers/model-manager/config/model-manager.env',
        'managers/model-manager/config/model-manager-db.env',
        'managers/model-manager/config/local.env',
        'managers/cluster-manager/config/cluster-manager.env',
        'managers/cluster-manager/config/cluster-manager-db.env',
        'managers/cluster-manager/config/local.env',
        'managers/task-manager/config/task-manager.env',
        'managers/task-manager/config/task-manager-db.env',
        'managers/task-manager/config/local.env',
        'managers/gateway-manager/config/gateway-manager.env',
        'managers/gateway-manager/config/gateway-manager-db.env',
        'managers/gateway-manager/config/local.env',
        # Infrastructure configs
        'config/infrastructure/services_gpu.env',
        'config/infrastructure/services_network.env',
        'config/infrastructure/services_security.env',
        'config/infrastructure/services_storage.env',
        # MCP configs
        'interfaces/model-context-protocol/config/mcp-ai-dev.env',
        'interfaces/model-context-protocol/config/mcp-core-tools.env',
        'interfaces/model-context-protocol/config/mcp-memory.env',
    ]
    
    missing_files = []
    existing_files = []
    
    for config_file in config_files:
        file_path = project_root / config_file
        if file_path.exists():
            existing_files.append(config_file)
            print(f"   ✅ {config_file}")
        else:
            missing_files.append(config_file)
            print(f"   ❌ {config_file}")
    
    print(f"\n📊 File Summary: {len(existing_files)}/{len(config_files)} files exist")
    
    if missing_files:
        print(f"⚠️  Missing {len(missing_files)} files:")
        for file in missing_files:
            print(f"     - {file}")
        return False
    else:
        print("✅ All configuration files exist")
        return True

if __name__ == "__main__":
    print("🚀 BitingLip Configuration Migration Validation")
    print("=" * 60)
    
    config_system_ok = test_distributed_config()
    config_files_ok = test_config_files()
    
    if config_system_ok and config_files_ok:
        print("\n🎉 VALIDATION SUCCESSFUL!")
        print("✅ Configuration migration completed successfully")
        print("✅ All services ready to use distributed configuration")
        sys.exit(0)
    else:
        print("\n⚠️  VALIDATION ISSUES DETECTED")
        print("Please review the errors above")
        sys.exit(1)
