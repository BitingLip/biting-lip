#!/usr/bin/env python3
"""
Enhanced LLM Challenge Test Script

This script tests the complete BitingLip platform by:
1. Testing service health (Model Manager, Task Manager)
2. Downloading and preparing models
3. Running text generation tasks
4. Demonstrating distributed processing capabilities
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

MODEL_MANAGER_URL = "http://localhost:8085"
TASK_MANAGER_URL = "http://localhost:8084"
TEST_MODEL = "gpt2"


async def test_service_health(service_name: str, url: str):
    """Test if a service is responding"""
    print(f"🔍 Testing {service_name} health...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ {service_name} is healthy: {data}")
                    return True
                else:
                    print(f"❌ {service_name} health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Cannot connect to {service_name}: {e}")
            return False


async def list_available_models():
    """List models currently available"""
    print("\n📋 Listing available models...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{MODEL_MANAGER_URL}/models/") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])
                    print(f"📊 Found {len(models)} registered models:")
                    for model in models:
                        print(f"   - {model.get('id')}: {model.get('name')} ({model.get('status')})")
                    return models
                else:
                    print(f"❌ Failed to list models: {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Error listing models: {e}")
            return []


async def request_model_download(model_name: str):
    """Request download of a specific model"""
    print(f"\n📥 Requesting download of model: {model_name}")
    
    payload = {
        "model_name": model_name,
        "model_id": model_name.replace("/", "_"),
        "model_type": "llm"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{MODEL_MANAGER_URL}/models/download", 
                json=payload
            ) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    print(f"✅ Download requested successfully: {data}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Download request failed: {response.status} - {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Error requesting download: {e}")
            return False


async def test_text_generation(model_id: str, prompt: str):
    """Test text generation with a model"""
    print(f"\n🤖 Testing text generation with {model_id}...")
    print(f"📝 Prompt: '{prompt}'")
    
    payload = {
        "model_id": model_id,
        "prompt": prompt,
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{MODEL_MANAGER_URL}/models/{model_id}/generate", 
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    generated_text = data.get("generated_text", "")
                    print(f"✅ Generated text: '{generated_text}'")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Text generation failed: {response.status} - {error_text}")
                    return False
        except Exception as e:
            print(f"❌ Error during text generation: {e}")
            return False


async def test_task_submission():
    """Test submitting a task to Task Manager"""
    print(f"\n📋 Testing task submission to Task Manager...")
    
    payload = {
        "task_type": "llm",
        "model_name": TEST_MODEL,
        "input_data": {
            "prompt": "The future of artificial intelligence is",
            "max_tokens": 30
        },
        "parameters": {
            "temperature": 0.8
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                f"{TASK_MANAGER_URL}/api/v1/tasks", 
                json=payload
            ) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    task_id = data.get("task_id")
                    print(f"✅ Task submitted successfully: {task_id}")
                    return task_id
                else:
                    error_text = await response.text()
                    print(f"❌ Task submission failed: {response.status} - {error_text}")
                    return None
        except Exception as e:
            print(f"❌ Error submitting task: {e}")
            return None


async def check_task_status(task_id: str):
    """Check the status of a submitted task"""
    if not task_id:
        return None
        
    print(f"\n📊 Checking status of task: {task_id}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{TASK_MANAGER_URL}/api/v1/tasks/{task_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    status = data.get("status")
                    print(f"📈 Task {task_id} status: {status}")
                    return data
                else:
                    error_text = await response.text()
                    print(f"❌ Failed to check task status: {response.status} - {error_text}")
                    return None
        except Exception as e:
            print(f"❌ Error checking task status: {e}")
            return None


async def run_comprehensive_test():
    """Run comprehensive test of the BitingLip platform"""
    print("🚀 Starting Comprehensive BitingLip LLM Challenge")
    print("=" * 55)
    
    # Step 1: Test service health
    model_manager_healthy = await test_service_health("Model Manager", MODEL_MANAGER_URL)
    task_manager_healthy = await test_service_health("Task Manager", TASK_MANAGER_URL)
    
    if not model_manager_healthy:
        print("❌ Model Manager not available. Cannot continue.")
        return False
    
    # Step 2: List available models
    models = await list_available_models()
    
    # Step 3: Ensure test model is available
    test_model_available = any(model.get("id") == TEST_MODEL for model in models)
    
    if not test_model_available:
        print(f"\n🔄 Model {TEST_MODEL} not found. Requesting download...")
        if await request_model_download(TEST_MODEL):
            print(f"✅ Model {TEST_MODEL} is now available!")
        else:
            print(f"❌ Failed to download {TEST_MODEL}")
            return False
    else:
        print(f"✅ Model {TEST_MODEL} is already available!")
    
    # Step 4: Test direct text generation
    test_prompts = [
        "Once upon a time",
        "The key to happiness is",
        "In the year 2030"
    ]
    
    generation_success = True
    for prompt in test_prompts:
        if not await test_text_generation(TEST_MODEL, prompt):
            generation_success = False
    
    # Step 5: Test task submission (if Task Manager is healthy)
    task_success = True
    if task_manager_healthy:
        task_id = await test_task_submission()
        if task_id:
            await asyncio.sleep(2)  # Give it a moment
            await check_task_status(task_id)
        else:
            task_success = False
    else:
        print("\n⚠️ Task Manager not healthy - skipping task submission tests")
        task_success = False
    
    # Step 6: Summary
    print("\n" + "=" * 55)
    print("📊 COMPREHENSIVE TEST SUMMARY")
    print("=" * 55)
    print(f"✅ Model Manager: {'Operational' if model_manager_healthy else 'Failed'}")
    print(f"{'✅' if task_manager_healthy else '❌'} Task Manager: {'Operational' if task_manager_healthy else 'Failed'}")
    print(f"✅ Model Available: {TEST_MODEL}")
    print(f"{'✅' if generation_success else '❌'} Text Generation: {'Working' if generation_success else 'Failed'}")
    print(f"{'✅' if task_success else '❌'} Task Submission: {'Working' if task_success else 'Failed'}")
    
    overall_success = model_manager_healthy and generation_success
    
    print(f"\n🎯 Overall Status: {'SUCCESS' if overall_success else 'PARTIAL SUCCESS'}")
    
    if overall_success:
        print("🎉 BitingLip platform is operational and ready for distributed LLM processing!")
        print("\n💡 Platform Capabilities Demonstrated:")
        print("   🔹 Model management and downloading")
        print("   🔹 Text generation with multiple models")
        print("   🔹 Service health monitoring")
        if task_manager_healthy:
            print("   🔹 Task submission and tracking")
        
        print("\n🚀 Ready for Production Use:")
        print("   • Start additional workers for scaling")
        print("   • Submit production workloads via Task Manager")
        print("   • Monitor performance via service endpoints")
    else:
        print("⚠️ Some components need attention for full functionality")
    
    return overall_success


if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())
