#!/usr/bin/env python3
"""
BitingLip Platform - Deployment Validation Script

This script validates that the entire platform is working correctly by:
1. Testing all service health endpoints
2. Testing basic API functionality
3. Testing frontend connectivity
4. Running end-to-end inference test
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List, Optional

# Service endpoints
SERVICES = {
    "Gateway Manager": "http://localhost:8001",
    "Model Manager": "http://localhost:8002", 
    "Task Manager": "http://localhost:8004",
    "Frontend": "http://localhost:3000"
}

# Test model for inference
TEST_MODEL = "gpt2"

class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass

class PlatformValidator:
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.results: Dict[str, Any] = {}
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def print_test(self, test_name: str, status: str = "INFO", details: str = ""):
        """Print a formatted test result"""
        emoji = {"INFO": "🔍", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{emoji.get(status, '🔍')} {test_name}")
        if details:
            print(f"   {details}")
    
    async def test_service_health(self, service_name: str, base_url: str) -> bool:
        """Test if a service health endpoint is responding"""
        try:
            async with self.session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    self.print_test(f"{service_name} Health Check", "SUCCESS", 
                                  f"Status: {data.get('status', 'unknown')}")
                    return True
                else:
                    self.print_test(f"{service_name} Health Check", "ERROR", 
                                  f"HTTP {response.status}")
                    return False
        except Exception as e:
            self.print_test(f"{service_name} Health Check", "ERROR", str(e))
            return False
    
    async def test_frontend_connectivity(self) -> bool:
        """Test if frontend is accessible"""
        try:
            async with self.session.get("http://localhost:3000") as response:
                if response.status == 200:
                    self.print_test("Frontend Connectivity", "SUCCESS", 
                                  "Web interface is accessible")
                    return True
                else:
                    self.print_test("Frontend Connectivity", "ERROR", 
                                  f"HTTP {response.status}")
                    return False
        except Exception as e:
            self.print_test("Frontend Connectivity", "ERROR", str(e))
            return False
    
    async def test_model_list(self) -> bool:
        """Test model listing functionality"""
        try:
            async with self.session.get("http://localhost:8002/models/") as response:
                if response.status == 200:
                    data = await response.json()
                    model_count = len(data.get('models', []))
                    self.print_test("Model List API", "SUCCESS", 
                                  f"Found {model_count} models")
                    return True
                else:
                    self.print_test("Model List API", "ERROR", 
                                  f"HTTP {response.status}")
                    return False
        except Exception as e:
            self.print_test("Model List API", "ERROR", str(e))
            return False
    
    async def test_model_download(self) -> bool:
        """Test model download functionality"""
        try:
            download_payload = {
                "model_name": TEST_MODEL,
                "source": "huggingface"
            }
            
            async with self.session.post(
                "http://localhost:8002/models/download",
                json=download_payload
            ) as response:
                if response.status in [200, 201, 202]:
                    data = await response.json()
                    self.print_test("Model Download API", "SUCCESS", 
                                  f"Download initiated for {TEST_MODEL}")
                    return True
                else:
                    text = await response.text()
                    self.print_test("Model Download API", "ERROR", 
                                  f"HTTP {response.status}: {text}")
                    return False
        except Exception as e:
            self.print_test("Model Download API", "ERROR", str(e))
            return False
    
    async def test_task_creation(self) -> bool:
        """Test task creation through Task Manager"""
        try:
            task_payload = {
                "task_type": "text_generation",
                "model_name": TEST_MODEL,
                "parameters": {
                    "prompt": "Hello, this is a test",
                    "max_tokens": 10
                },
                "priority": "normal"
            }
            
            async with self.session.post(
                "http://localhost:8004/tasks/",
                json=task_payload
            ) as response:
                if response.status in [200, 201, 202]:
                    data = await response.json()
                    task_id = data.get('task_id') or data.get('id')
                    self.print_test("Task Creation API", "SUCCESS", 
                                  f"Task created with ID: {task_id}")
                    return True
                else:
                    text = await response.text()
                    self.print_test("Task Creation API", "ERROR", 
                                  f"HTTP {response.status}: {text}")
                    return False
        except Exception as e:
            self.print_test("Task Creation API", "ERROR", str(e))
            return False
    
    async def test_gateway_inference(self) -> bool:
        """Test inference through Gateway Manager"""
        try:
            inference_payload = {
                "model": TEST_MODEL,
                "prompt": "Hello, this is a test",
                "max_tokens": 10,
                "temperature": 0.7
            }
            
            async with self.session.post(
                "http://localhost:8001/api/v1/inference/text-generation",
                json=inference_payload
            ) as response:
                if response.status in [200, 201, 202]:
                    data = await response.json()
                    self.print_test("Gateway Inference API", "SUCCESS", 
                                  "Inference request processed")
                    return True
                else:
                    text = await response.text()
                    self.print_test("Gateway Inference API", "ERROR", 
                                  f"HTTP {response.status}: {text}")
                    return False
        except Exception as e:
            self.print_test("Gateway Inference API", "ERROR", str(e))
            return False
    
    async def test_authentication(self) -> bool:
        """Test authentication endpoints"""
        try:
            auth_payload = {
                "username": "admin",
                "password": "admin123"
            }
            
            async with self.session.post(
                "http://localhost:8001/api/v1/auth/login",
                json=auth_payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    token = data.get('access_token')
                    self.print_test("Authentication API", "SUCCESS", 
                                  f"Login successful, token received")
                    return True
                else:
                    text = await response.text()
                    self.print_test("Authentication API", "ERROR", 
                                  f"HTTP {response.status}: {text}")
                    return False
        except Exception as e:
            self.print_test("Authentication API", "ERROR", str(e))
            return False
    
    async def run_validation(self) -> Dict[str, bool]:
        """Run all validation tests"""
        print("=" * 70)
        print("🔍 BITINGLIP PLATFORM VALIDATION")
        print("=" * 70)
        
        results = {}
        
        # Test 1: Service Health Checks
        print("\n🏥 Service Health Checks")
        print("-" * 30)
        for service_name, base_url in SERVICES.items():
            if service_name == "Frontend":
                continue  # Skip health check for frontend
            results[f"{service_name}_health"] = await self.test_service_health(
                service_name, base_url
            )
        
        # Test 2: Frontend Connectivity
        print("\n🌐 Frontend Connectivity")
        print("-" * 30)
        results["frontend_connectivity"] = await self.test_frontend_connectivity()
        
        # Test 3: Core API Functionality
        print("\n🔧 Core API Functionality")
        print("-" * 30)
        results["model_list"] = await self.test_model_list()
        results["model_download"] = await self.test_model_download()
        results["task_creation"] = await self.test_task_creation()
        results["authentication"] = await self.test_authentication()
        
        # Test 4: End-to-End Inference (Optional)
        print("\n🚀 End-to-End Inference")
        print("-" * 30)
        results["gateway_inference"] = await self.test_gateway_inference()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)
        
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        for test_name, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} {test_name.replace('_', ' ').title()}")
        
        print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Platform is fully functional.")
        elif passed >= total * 0.7:
            print("⚠️ Most tests passed. Some features may need attention.")
        else:
            print("❌ Multiple failures detected. Please check service logs.")
        
        return results

async def main():
    """Main validation function"""
    try:
        async with PlatformValidator() as validator:
            results = await validator.run_validation()
            
            # Exit with appropriate code
            passed = sum(1 for success in results.values() if success)
            total = len(results)
            
            if passed == total:
                print("\n🎉 Platform validation completed successfully!")
                return 0
            else:
                print(f"\n⚠️ Platform validation completed with {total - passed} failures.")
                return 1
                
    except Exception as e:
        print(f"💥 Validation failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
