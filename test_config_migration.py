#!/usr/bin/env python3
"""
Test script to verify the configuration migration
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_distributed_config():
    """Test the distributed configuration system"""
    print("🔧 Testing Distributed Configuration System")
    print("=" * 50)
    
    try:
        from config.distributed_config import DistributedConfigLoader, get_config_loader
        
        # Initialize the config loader
        loader = get_config_loader()
        print(f"✅ Config loader initialized with project root: {loader.project_root}")
        
        # Test service list
        services = loader.get_service_list()
        print(f"✅ Found {len(services)} services: {services}")
        
        # Test model-manager configuration
        print("\n📁 Testing Model Manager Configuration:")
        model_config = loader.load_service_config('model-manager', 'manager')
        print(f"   Loaded {len(model_config)} configuration values")
        for key, value in list(model_config.items())[:5]:  # Show first 5
            print(f"   {key}={value}")
        
        # Test infrastructure configuration
        print("\n🏗️ Testing Infrastructure Configuration:")
        infra_config = loader.load_infrastructure_config()
        print(f"   Loaded {len(infra_config)} infrastructure values")
        for key, value in list(infra_config.items())[:5]:  # Show first 5
            print(f"   {key}={value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing distributed config: {e}")
        return False

def test_service_configs():
    """Test that service configurations are properly located"""
    print("\n📂 Testing Service Configuration Files")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Check manager configurations
    managers = ['model-manager', 'cluster-manager', 'task-manager', 'gateway-manager']
    for manager in managers:
        config_dir = project_root / "managers" / manager / "config"
        if config_dir.exists():
            files = list(config_dir.glob("*.env"))
            print(f"✅ {manager}: {len(files)} config files in {config_dir}")
            for file in files:
                print(f"   - {file.name}")
        else:
            print(f"❌ {manager}: config directory not found at {config_dir}")
    
    # Check infrastructure configurations
    infra_dir = project_root / "config" / "infrastructure"
    if infra_dir.exists():
        files = list(infra_dir.glob("*.env"))
        print(f"✅ Infrastructure: {len(files)} config files in {infra_dir}")
        for file in files:
            print(f"   - {file.name}")
    else:
        print(f"❌ Infrastructure: config directory not found at {infra_dir}")
    
    # Check MCP configurations
    mcp_dir = project_root / "interfaces" / "model-context-protocol" / "config"
    if mcp_dir.exists():
        files = list(mcp_dir.glob("*.env"))
        print(f"✅ MCP Interface: {len(files)} config files in {mcp_dir}")
        for file in files:
            print(f"   - {file.name}")
    else:
        print(f"❌ MCP Interface: config directory not found at {mcp_dir}")

def test_model_manager_integration():
    """Test model manager with new configuration"""
    print("\n🤖 Testing Model Manager Integration")
    print("=" * 50)
    
    try:
        # Clear any existing config modules from cache
        if 'config' in sys.modules:
            del sys.modules['config']
        
        # Test importing model manager config
        model_manager_path = Path(__file__).parent / "managers" / "model-manager" / "app"
        if str(model_manager_path) not in sys.path:
            sys.path.insert(0, str(model_manager_path))
        
        # Import from the model manager's app.config module
        import config as model_config
        
        # Verify the import is correct
        if not hasattr(model_config, 'get_settings'):
            print(f"❌ Config module doesn't have get_settings. Available: {dir(model_config)}")
            return False
        
        settings = model_config.get_settings()
        print(f"✅ Model Manager settings loaded successfully")
        print(f"   Host: {settings.host}")
        print(f"   Port: {settings.port}")
        print(f"   Debug: {settings.debug}")
        print(f"   DB Host: {settings.db_host}")
        print(f"   Cache Dir: {settings.model_cache_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing model manager integration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all configuration tests"""
    print("🚀 BitingLip Configuration Migration Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Distributed config system
    results.append(test_distributed_config())
    
    # Test 2: Service config files
    test_service_configs()
    
    # Test 3: Model manager integration
    results.append(test_model_manager_integration())
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Configuration migration successful!")
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
