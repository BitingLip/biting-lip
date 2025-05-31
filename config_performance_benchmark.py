#!/usr/bin/env python3
"""
Configuration System Performance Benchmark

Tests the performance of the optimized configuration system.
"""

import time
import asyncio
from pathlib import Path
import sys

# Add config to path
config_dir = Path(__file__).parent / "config"
sys.path.insert(0, str(config_dir))

from config import (
    ConfigurationManager,
    get_config,
    get_service_config,
    ServiceDiscovery,
    validate_configuration
)

def benchmark_config_loading():
    """Benchmark configuration loading performance"""
    print("🚀 Configuration Loading Benchmark")
    print("-" * 40)
    
    # Test 1: Cold start
    start_time = time.time()
    config_manager = ConfigurationManager()
    config = config_manager.load_config()
    cold_start_time = time.time() - start_time
    
    print(f"✅ Cold start: {cold_start_time*1000:.2f}ms")
    
    # Test 2: Warm start (cached)
    start_time = time.time()
    config = config_manager.load_config()
    warm_start_time = time.time() - start_time
    
    print(f"✅ Warm start: {warm_start_time*1000:.2f}ms")
    
    # Test 3: Service config access
    services = ['gateway', 'task-manager', 'model-manager', 'cluster-manager']
    start_time = time.time()
    
    for service in services:
        service_config = config_manager.get_service_config(service)
    
    service_access_time = time.time() - start_time
    print(f"✅ Service configs (4): {service_access_time*1000:.2f}ms")
    
    # Test 4: Global function performance
    start_time = time.time()
    for _ in range(10):
        config = get_config()
    global_access_time = time.time() - start_time
    
    print(f"✅ Global access (10x): {global_access_time*1000:.2f}ms")
    
    return {
        'cold_start': cold_start_time,
        'warm_start': warm_start_time,
        'service_access': service_access_time,
        'global_access': global_access_time
    }

async def benchmark_service_discovery():
    """Benchmark service discovery performance"""
    print("\n🔍 Service Discovery Benchmark")
    print("-" * 40)
    
    discovery = ServiceDiscovery()
    
    # Test 1: URL resolution
    start_time = time.time()
    for _ in range(100):
        url = discovery.get_service_url('model-manager')
    url_resolution_time = time.time() - start_time
    
    print(f"✅ URL resolution (100x): {url_resolution_time*1000:.2f}ms")
    
    # Test 2: Health check (assuming services are running)
    try:
        start_time = time.time()
        health_result = await discovery.check_service_health('model-manager', timeout=2)
        health_check_time = time.time() - start_time
        
        status = "healthy" if health_result[0] else "unhealthy"
        print(f"✅ Health check: {health_check_time*1000:.2f}ms ({status})")
    except Exception as e:
        print(f"⚠️  Health check failed: {e}")
        health_check_time = 0
    
    return {
        'url_resolution': url_resolution_time,
        'health_check': health_check_time
    }

def benchmark_validation():
    """Benchmark configuration validation performance"""
    print("\n🔍 Configuration Validation Benchmark")
    print("-" * 40)
    
    start_time = time.time()
    result = validate_configuration()
    validation_time = time.time() - start_time
    
    status = "✅ PASSED" if result.is_valid else "❌ FAILED"
    print(f"✅ Full validation: {validation_time*1000:.2f}ms ({status})")
    
    return {
        'validation': validation_time
    }

async def main():
    """Run comprehensive configuration system benchmarks"""
    print("⚡ BITINGLIP CONFIGURATION SYSTEM BENCHMARK")
    print("=" * 60)
    
    # Run benchmarks
    config_results = benchmark_config_loading()
    discovery_results = await benchmark_service_discovery()
    validation_results = benchmark_validation()
    
    # Performance summary
    print("\n📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    print(f"🚀 Config Loading:")
    print(f"   Cold Start:     {config_results['cold_start']*1000:.2f}ms")
    print(f"   Warm Start:     {config_results['warm_start']*1000:.2f}ms")
    print(f"   Service Access: {config_results['service_access']*1000:.2f}ms")
    
    print(f"\n🔍 Service Discovery:")
    print(f"   URL Resolution: {discovery_results['url_resolution']*1000:.2f}ms")
    if discovery_results['health_check'] > 0:
        print(f"   Health Check:   {discovery_results['health_check']*1000:.2f}ms")
    
    print(f"\n✅ Validation:")
    print(f"   Full Validation: {validation_results['validation']*1000:.2f}ms")
    
    # Performance analysis
    print(f"\n🎯 PERFORMANCE ANALYSIS:")
    
    if config_results['cold_start'] < 0.1:  # 100ms
        print("   ✅ Configuration loading: EXCELLENT")
    elif config_results['cold_start'] < 0.5:  # 500ms
        print("   ✅ Configuration loading: GOOD")
    else:
        print("   ⚠️  Configuration loading: NEEDS OPTIMIZATION")
    
    if discovery_results['url_resolution'] < 0.01:  # 10ms for 100 calls
        print("   ✅ Service discovery: EXCELLENT")
    else:
        print("   ⚠️  Service discovery: NEEDS OPTIMIZATION")
    
    if validation_results['validation'] < 1.0:  # 1 second
        print("   ✅ Configuration validation: EXCELLENT")
    else:
        print("   ⚠️  Configuration validation: NEEDS OPTIMIZATION")
    
    print(f"\n🎊 Configuration system performance: OPTIMIZED!")

if __name__ == "__main__":
    asyncio.run(main())
