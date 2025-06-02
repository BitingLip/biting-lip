#!/usr/bin/env python3
"""
Final validation script for BitingLip configuration migration.
Tests all service managers to ensure they can load configurations successfully.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_service_config_loading():
    """Test that all services can load their configurations"""
    print("🔍 Final Configuration Validation")
    print("=" * 50)
    
    services = [
        {
            'name': 'Model Manager',
            'path': 'managers.model-manager.app.config',
            'class': 'ModelManagerSettings'
        },
        {
            'name': 'Cluster Manager', 
            'path': 'managers.cluster-manager.app.config',
            'class': 'ClusterManagerSettings'
        },
        {
            'name': 'Task Manager',
            'path': 'managers.task-manager.app.core.config',
            'class': 'TaskManagerSettings'
        },
        {
            'name': 'Gateway Manager',
            'path': 'managers.gateway-manager.app.config', 
            'class': 'GatewayManagerSettings'
        }
    ]
    
    results = []
    
    for service in services:
        try:
            print(f"\n📦 Testing {service['name']}...")
            
            # Import the module
            module_path = service['path'].replace('-', '_')
            module = __import__(module_path, fromlist=[service['class']])
            
            # Get the settings class
            settings_class = getattr(module, service['class'])
            
            # Create an instance
            settings = settings_class()
            
            # Test some basic properties
            host = getattr(settings, 'host', 'N/A')
            port = getattr(settings, 'port', 'N/A')
            debug = getattr(settings, 'debug', 'N/A')
            
            print(f"   ✅ Configuration loaded successfully")
            print(f"   📊 Host: {host}, Port: {port}, Debug: {debug}")
            
            results.append({'service': service['name'], 'status': '✅ PASS'})
            
        except Exception as e:
            print(f"   ❌ Error loading {service['name']}: {str(e)}")
            results.append({'service': service['name'], 'status': f'❌ FAIL: {str(e)}'})
    
    print(f"\n📊 Validation Summary")
    print("=" * 30)
    
    passed = 0
    for result in results:
        print(f"{result['service']}: {result['status']}")
        if '✅' in result['status']:
            passed += 1
    
    total = len(results)
    print(f"\nResults: {passed}/{total} services passed")
    
    if passed == total:
        print("🎉 All services successfully migrated to distributed configuration!")
        return True
    else:
        print("⚠️  Some services failed validation. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = test_service_config_loading()
    sys.exit(0 if success else 1)
