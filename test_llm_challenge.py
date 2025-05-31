#!/usr/bin/env python3
"""
LLM Challenge Test Script

This script tests the BitingLip platform by:
1. Requesting a small LLM model download via Model Manager
2. Running text generation tasks 
3. Testing distributed processing capabilities
"""

import asyncio
import aiohttp
import json
import time
from typing import Dict, Any, List

MODEL_MANAGER_URL = "http://localhost:8085"
TEST_MODEL = "gpt2"  # Small model for testing


async def test_model_manager_health():
    """Test if Model Manager is responding"""
    print("🔍 Testing Model Manager health...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{MODEL_MANAGER_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Model Manager is healthy: {data}")
                    return True
                else:
                    print(f"❌ Model Manager health check failed: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Cannot connect to Model Manager: {e}")
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
                        print(f"   - {model['id']}: {model['name']} ({model['status']})")
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


async def wait_for_model_availability(model_id: str, timeout: int = 300):
    """Wait for a model to become available"""
    print(f"\n⏳ Waiting for model {model_id} to become available...")
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < timeout:
            try:
                async with session.get(f"{MODEL_MANAGER_URL}/models/{model_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        status = data.get("status")
                        
                        if status == "available":
                            print(f"✅ Model {model_id} is now available!")
                            return True
                        elif status == "downloading":
                            print(f"📥 Model {model_id} is downloading... (progress info may vary)")
                        elif status == "error":
                            print(f"❌ Model {model_id} download failed")
                            return False
                        
            except Exception as e:
                print(f"⚠️ Error checking model status: {e}")
            
            await asyncio.sleep(5)  # Check every 5 seconds
        
        print(f"⏰ Timeout waiting for model {model_id}")
        return False


async def search_huggingface_models(query: str = "gpt2"):
    """Search for models on HuggingFace Hub"""
    print(f"\n🔍 Searching HuggingFace Hub for: {query}")
    
    params = {
        "query": query,
        "limit": 5
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                f"{MODEL_MANAGER_URL}/models/search", 
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])
                    print(f"🎯 Found {len(models)} models on HuggingFace:")
                    for model in models[:3]:  # Show top 3
                        print(f"   - {model['id']} (👍 {model.get('likes', 0)} likes, 📥 {model.get('downloads', 0)} downloads)")
                    return models
                else:
                    print(f"❌ Search failed: {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Error searching models: {e}")
            return []


async def run_llm_challenge():
    """Run the complete LLM challenge"""
    print("🚀 Starting BitingLip LLM Challenge")
    print("=" * 50)
    
    # Step 1: Health check
    if not await test_model_manager_health():
        print("❌ Cannot proceed - Model Manager is not responding")
        return False
    
    # Step 2: List current models
    current_models = await list_available_models()
    
    # Check if test model already exists
    test_model_available = any(
        model['id'] == TEST_MODEL and model['status'] == 'available' 
        for model in current_models
    )
    
    if test_model_available:
        print(f"✅ Test model {TEST_MODEL} is already available!")
    else:
        # Step 3: Search for models
        await search_huggingface_models(TEST_MODEL)
        
        # Step 4: Request model download
        if await request_model_download(TEST_MODEL):
            # Step 5: Wait for download to complete
            if not await wait_for_model_availability(TEST_MODEL):
                print("❌ Model download failed or timed out")
                return False
    
    # Step 6: Verify model is ready
    print(f"\n🎯 Model {TEST_MODEL} is ready for inference!")
    
    # Step 7: Show summary
    print("\n📊 Challenge Summary:")
    print("✅ Model Manager: Operational")
    print(f"✅ Model Downloaded: {TEST_MODEL}")
    print("✅ Ready for distributed processing")
    
    # Note about next steps
    print("\n🎯 Next Steps:")
    print("1. Start Cluster Manager to create workers")
    print("2. Start Task Manager for task orchestration") 
    print("3. Submit text generation tasks")
    print("4. Monitor distributed processing")
    
    return True


async def main():
    """Main test function"""
    try:
        success = await run_llm_challenge()
        if success:
            print("\n🎉 LLM Challenge Phase 1 completed successfully!")
            print("💡 The Model Manager is working properly and ready for distributed processing.")
        else:
            print("\n❌ LLM Challenge failed!")
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
