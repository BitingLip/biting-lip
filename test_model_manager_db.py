#!/usr/bin/env python3
"""
Test Model Manager PostgreSQL Connection
Quick test to verify database connection and basic functionality
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def set_environment():
    """Set required environment variables"""
    env_vars = {
        'MODEL_DB_HOST': 'localhost',
        'MODEL_DB_PORT': '5432',
        'MODEL_DB_NAME': 'bitinglip_models',
        'MODEL_DB_USER': 'model_manager',
        'MODEL_DB_PASSWORD': 'model_manager_2025!',
        'MODELS_DIRECTORY': './models'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✅ Set {key}={value}")

def test_registry_connection():
    """Test PostgreSQL registry connection"""
    try:
        # Add model-manager to Python path
        sys.path.append('managers/model-manager')
        from app.models.postgresql_registry import PostgreSQLModelRegistry
        
        # Database configuration
        db_config = {
            'host': os.getenv('MODEL_DB_HOST'),
            'port': int(os.getenv('MODEL_DB_PORT', '5432')),
            'database': os.getenv('MODEL_DB_NAME'),
            'user': os.getenv('MODEL_DB_USER'),
            'password': os.getenv('MODEL_DB_PASSWORD'),
        }
        
        print(f"\n🔗 Testing PostgreSQL connection...")
        print(f"   Database: {db_config['database']}")
        print(f"   Host: {db_config['host']}:{db_config['port']}")
        print(f"   User: {db_config['user']}")
        
        # Create registry instance
        registry = PostgreSQLModelRegistry(db_config)
        
        # Test basic operations
        print(f"\n📊 Testing registry operations...")
        
        # Get statistics
        stats = registry.get_statistics()
        print(f"   Model count: {stats.get('total_models', 'N/A')}")
        print(f"   Worker count: {stats.get('total_workers', 'N/A')}")
        
        # List models
        models = registry.list_models()
        print(f"   Listed {len(models)} models")
        for model in models[:3]:  # Show first 3
            print(f"     - {model.id}: {model.name} ({model.status.value})")
        
        print(f"\n✅ PostgreSQL registry connection successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Registry connection failed: {e}")
        return False

def test_model_manager_startup():
    """Test model manager application startup"""
    try:
        print(f"\n🚀 Testing Model Manager startup...")
        
        # Import the app
        from app.main import create_app
        
        # Create the FastAPI app
        app = create_app()
        print(f"   ✅ FastAPI app created successfully")
        
        # Test basic app properties
        print(f"   📋 App title: {app.title}")
        print(f"   📋 Routes: {len(app.routes)} routes registered")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Model Manager startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🧪 BitingLip Model Manager PostgreSQL Migration Test")
    print("=" * 60)
    
    # Set environment variables
    print("\n📝 Setting environment variables...")
    set_environment()
    
    # Test registry connection
    registry_ok = test_registry_connection()
    
    # Test model manager startup  
    startup_ok = test_model_manager_startup()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Registry Connection: {'✅ PASS' if registry_ok else '❌ FAIL'}")
    print(f"Model Manager Startup: {'✅ PASS' if startup_ok else '❌ FAIL'}")
    
    if registry_ok and startup_ok:
        print("\n🎉 All tests passed! Model Manager is ready for PostgreSQL.")
        print("\nNext steps:")
        print("1. Start model manager: python -m managers.model-manager.app.main")
        print("2. Test API endpoints")
        print("3. Integrate with other services")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
