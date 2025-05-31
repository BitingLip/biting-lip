#!/usr/bin/env python3
"""
Mock Backend for BitingLip AI GPU Cluster Management Platform
Provides realistic API endpoints for development and testing
"""
import random
import time
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="BitingLip Mock Backend",
    description="Mock API for BitingLip AI GPU Cluster Management Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Mock Data Storage
mock_users = {
    "admin": {
        "id": "user-001",
        "username": "admin",
        "email": "admin@bitinglip.dev",
        "name": "Development Admin",
        "role": "admin",
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z",
        "last_login": datetime.now().isoformat() + "Z"
    }
}

mock_models = [
    {
        "id": "model-001",
        "name": "GPT-2 Base",
        "description": "OpenAI GPT-2 base model for text generation",
        "type": "text-generation",
        "status": "ready",
        "file_size": 548000000,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "metrics": {
            "accuracy": 0.85,
            "total_runs": 1250,
            "avg_response_time": 0.45,
            "error_rate": 0.02
        }
    },
    {
        "id": "model-002", 
        "name": "Stable Diffusion XL",
        "description": "High-resolution text-to-image generation model",
        "type": "image-generation",
        "status": "deployed",
        "file_size": 6800000000,
        "created_at": "2024-01-10T14:20:00Z",
        "updated_at": "2024-01-20T09:15:00Z",
        "metrics": {
            "accuracy": 0.92,
            "total_runs": 856,
            "avg_response_time": 2.3,
            "error_rate": 0.01
        }
    },
    {
        "id": "model-003",
        "name": "BERT Embeddings",
        "description": "BERT model for text embeddings and similarity",
        "type": "embeddings",
        "status": "loading",
        "file_size": 438000000,
        "created_at": "2024-01-25T16:45:00Z",
        "updated_at": "2024-01-25T16:45:00Z",
        "metrics": {
            "accuracy": 0.78,
            "total_runs": 445,
            "avg_response_time": 0.12,
            "error_rate": 0.03
        }
    }
]

mock_clusters = [
    {
        "id": "cluster-001",
        "name": "Production Cluster",
        "description": "Main production GPU cluster",
        "status": "active",
        "worker_count": 4,
        "total_gpus": 8,
        "available_gpus": 5,
        "cpu_usage": 65.2,
        "memory_usage": 78.5,
        "gpu_usage": 42.1,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": datetime.now().isoformat() + "Z"
    },
    {
        "id": "cluster-002",
        "name": "Development Cluster", 
        "description": "Development and testing environment",
        "status": "idle",
        "worker_count": 2,
        "total_gpus": 4,
        "available_gpus": 4,
        "cpu_usage": 12.8,
        "memory_usage": 23.1,
        "gpu_usage": 0.0,
        "created_at": "2024-01-05T10:30:00Z",
        "updated_at": datetime.now().isoformat() + "Z"
    }
]

mock_tasks = [
    {
        "id": "task-001",
        "name": "Generate Product Description",
        "type": "text-generation",
        "status": "completed",
        "priority": "normal",
        "model_id": "model-001",
        "cluster_id": "cluster-001",
        "input_data": {"prompt": "Generate a product description for wireless headphones"},
        "output_data": {"text": "Premium wireless headphones with noise cancellation..."},
        "progress": 100,
        "execution_time": 1.25,
        "created_at": "2024-01-25T14:30:00Z",
        "updated_at": "2024-01-25T14:31:15Z"
    },
    {
        "id": "task-002",
        "name": "Create Marketing Banner",
        "type": "image-generation", 
        "status": "running",
        "priority": "high",
        "model_id": "model-002",
        "cluster_id": "cluster-001",
        "input_data": {"prompt": "Modern tech banner with blue gradient"},
        "output_data": None,
        "progress": 67,
        "execution_time": None,
        "created_at": "2024-01-25T15:00:00Z",
        "updated_at": "2024-01-25T15:02:30Z"
    },
    {
        "id": "task-003",
        "name": "Document Similarity Analysis",
        "type": "embeddings",
        "status": "pending",
        "priority": "low",
        "model_id": "model-003",
        "cluster_id": "cluster-002",
        "input_data": {"documents": ["doc1.txt", "doc2.txt"]},
        "output_data": None,
        "progress": 0,
        "execution_time": None,
        "created_at": "2024-01-25T15:15:00Z",
        "updated_at": "2024-01-25T15:15:00Z"
    }
]

mock_workers = [
    {
        "id": "worker-001",
        "name": "GPU-Worker-01",
        "cluster_id": "cluster-001",
        "status": "active",
        "cpu_usage": 45.2,
        "memory_usage": 67.8,
        "gpu_usage": 85.3,
        "gpu_memory": 89.1,
        "temperature": 72,
        "active_tasks": 2,
        "max_tasks": 4,
        "last_heartbeat": datetime.now().isoformat() + "Z"
    },
    {
        "id": "worker-002", 
        "name": "GPU-Worker-02",
        "cluster_id": "cluster-001",
        "status": "active",
        "cpu_usage": 38.7,
        "memory_usage": 54.2,
        "gpu_usage": 72.6,
        "gpu_memory": 76.4,
        "temperature": 68,
        "active_tasks": 1,
        "max_tasks": 4,
        "last_heartbeat": datetime.now().isoformat() + "Z"
    },
    {
        "id": "worker-003",
        "name": "GPU-Worker-03", 
        "cluster_id": "cluster-002",
        "status": "idle",
        "cpu_usage": 8.1,
        "memory_usage": 15.3,
        "gpu_usage": 0.0,
        "gpu_memory": 2.1,
        "temperature": 45,
        "active_tasks": 0,
        "max_tasks": 4,
        "last_heartbeat": datetime.now().isoformat() + "Z"
    }
]

# Pydantic Models
class LoginRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

# Auth dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Mock authentication - just return admin user
    return mock_users["admin"]

# Health Check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Authentication Endpoints
@app.post("/api/v1/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "admin123":
        return AuthResponse(
            access_token="mock-jwt-token-" + str(int(time.time())),
            user=mock_users["admin"]
        )
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/v1/auth/logout")
async def logout(user=Depends(get_current_user)):
    return {"message": "Logged out successfully"}

@app.get("/api/v1/auth/profile")
async def get_profile(user=Depends(get_current_user)):
    return user

# Models Endpoints
@app.get("/api/v1/models")
async def get_models(user=Depends(get_current_user)):
    return {"data": mock_models, "success": True}

@app.get("/api/v1/models/{model_id}")
async def get_model(model_id: str, user=Depends(get_current_user)):
    model = next((m for m in mock_models if m["id"] == model_id), None)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return {"data": model, "success": True}

@app.post("/api/v1/models/{model_id}/deploy")
async def deploy_model(model_id: str, user=Depends(get_current_user)):
    model = next((m for m in mock_models if m["id"] == model_id), None)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model["status"] = "deployed"
    return {"message": f"Model {model_id} deployed successfully", "success": True}

@app.post("/api/v1/models/{model_id}/undeploy")
async def undeploy_model(model_id: str, user=Depends(get_current_user)):
    model = next((m for m in mock_models if m["id"] == model_id), None)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    model["status"] = "ready"
    return {"message": f"Model {model_id} undeployed successfully", "success": True}

@app.delete("/api/v1/models/{model_id}")
async def delete_model(model_id: str, user=Depends(get_current_user)):
    global mock_models
    mock_models = [m for m in mock_models if m["id"] != model_id]
    return {"message": f"Model {model_id} deleted successfully", "success": True}

# Clusters Endpoints  
@app.get("/api/v1/clusters")
async def get_clusters(user=Depends(get_current_user)):
    return {"data": mock_clusters, "success": True}

@app.get("/api/v1/clusters/{cluster_id}")
async def get_cluster(cluster_id: str, user=Depends(get_current_user)):
    cluster = next((c for c in mock_clusters if c["id"] == cluster_id), None)
    if not cluster:
        raise HTTPException(status_code=404, detail="Cluster not found")
    return {"data": cluster, "success": True}

@app.post("/api/v1/clusters")
async def create_cluster(cluster_data: dict, user=Depends(get_current_user)):
    new_cluster = {
        "id": f"cluster-{len(mock_clusters) + 1:03d}",
        "name": cluster_data.get("name", "New Cluster"),
        "description": cluster_data.get("description", ""),
        "status": "idle",
        "worker_count": 0,
        "total_gpus": 0,
        "available_gpus": 0,
        "cpu_usage": 0.0,
        "memory_usage": 0.0,
        "gpu_usage": 0.0,
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z"
    }
    mock_clusters.append(new_cluster)
    return {"data": new_cluster, "success": True}

@app.delete("/api/v1/clusters/{cluster_id}")
async def delete_cluster(cluster_id: str, user=Depends(get_current_user)):
    global mock_clusters
    mock_clusters = [c for c in mock_clusters if c["id"] != cluster_id]
    return {"message": f"Cluster {cluster_id} deleted successfully", "success": True}

# Tasks Endpoints
@app.get("/api/v1/tasks")
async def get_tasks(user=Depends(get_current_user)):
    return {"data": mock_tasks, "success": True}

@app.get("/api/v1/tasks/queue/stats")
async def get_queue_stats(user=Depends(get_current_user)):
    """Get task queue statistics"""
    pending_tasks = len([t for t in mock_tasks if t["status"] == "pending"])
    running_tasks = len([t for t in mock_tasks if t["status"] == "running"])
    completed_tasks = len([t for t in mock_tasks if t["status"] == "completed"])
    failed_tasks = len([t for t in mock_tasks if t["status"] == "failed"])
    
    return {
        "data": {
            "pending": pending_tasks,
            "running": running_tasks,
            "completed": completed_tasks,
            "failed": failed_tasks,
            "total": len(mock_tasks),
            "queue_length": pending_tasks + running_tasks,
            "throughput": {
                "tasks_per_hour": 45,
                "avg_wait_time": 2.3,
                "avg_execution_time": 1.8
            }
        },
        "success": True
    }

@app.get("/api/v1/tasks/{task_id}")
async def get_task(task_id: str, user=Depends(get_current_user)):
    task = next((t for t in mock_tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"data": task, "success": True}

@app.post("/api/v1/tasks")
async def create_task(task_data: dict, user=Depends(get_current_user)):
    new_task = {
        "id": f"task-{len(mock_tasks) + 1:03d}",
        "name": task_data.get("name", "New Task"),
        "type": task_data.get("type", "text-generation"),
        "status": "pending",
        "priority": task_data.get("priority", "normal"),
        "model_id": task_data.get("model_id"),
        "cluster_id": task_data.get("cluster_id"),
        "input_data": task_data.get("input_data", {}),
        "output_data": None,
        "progress": 0,
        "execution_time": None,
        "created_at": datetime.now().isoformat() + "Z",
        "updated_at": datetime.now().isoformat() + "Z"
    }
    mock_tasks.append(new_task)
    return {"data": new_task, "success": True}

@app.delete("/api/v1/tasks/{task_id}")
async def delete_task(task_id: str, user=Depends(get_current_user)):
    global mock_tasks
    mock_tasks = [t for t in mock_tasks if t["id"] != task_id]
    return {"message": f"Task {task_id} deleted successfully", "success": True}

# Workers Endpoints
@app.get("/api/v1/workers")
async def get_workers(user=Depends(get_current_user)):
    # Add some randomness to simulate live data
    for worker in mock_workers:
        if worker["status"] == "active":
            worker["cpu_usage"] = max(0, min(100, worker["cpu_usage"] + random.uniform(-5, 5)))
            worker["memory_usage"] = max(0, min(100, worker["memory_usage"] + random.uniform(-3, 3)))
            worker["gpu_usage"] = max(0, min(100, worker["gpu_usage"] + random.uniform(-10, 10)))
            worker["temperature"] = max(30, min(90, worker["temperature"] + random.uniform(-2, 2)))
        worker["last_heartbeat"] = datetime.now().isoformat() + "Z"
    
    return {"data": mock_workers, "success": True}

@app.get("/api/v1/workers/{worker_id}")
async def get_worker(worker_id: str, user=Depends(get_current_user)):
    worker = next((w for w in mock_workers if w["id"] == worker_id), None)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"data": worker, "success": True}

# Monitoring Endpoints
@app.get("/api/v1/monitoring/metrics")
async def get_metrics(user=Depends(get_current_user)):
    return {
        "data": {
            "system": {
                "total_workers": len(mock_workers),
                "active_workers": len([w for w in mock_workers if w["status"] == "active"]),
                "total_tasks": len(mock_tasks),
                "active_tasks": len([t for t in mock_tasks if t["status"] in ["running", "pending"]]),
                "total_models": len(mock_models),
                "deployed_models": len([m for m in mock_models if m["status"] == "deployed"])
            },
            "performance": {
                "avg_cpu_usage": sum(w["cpu_usage"] for w in mock_workers) / len(mock_workers),
                "avg_memory_usage": sum(w["memory_usage"] for w in mock_workers) / len(mock_workers),
                "avg_gpu_usage": sum(w["gpu_usage"] for w in mock_workers) / len(mock_workers),
                "total_processing_power": sum(c["total_gpus"] for c in mock_clusters)
            }
        },
        "success": True
    }

if __name__ == "__main__":
    print("🚀 Starting BitingLip Mock Backend...")
    print("📍 API Documentation: http://localhost:8001/docs")
    print("🔑 Login with: admin / admin123")
    print("🌐 Frontend: http://localhost:3000")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
