# BitingLip Deployment Guide

## Deployment Options

### Development Deployment

For local development and testing:

```bash
# Start Redis
docker-compose -f cluster-manager/docker-compose.yml up -d redis

# Start each service individually
cd model-manager && python app/main.py &
cd task-manager && python app/main.py &
cd cluster-manager/cluster/worker && python app/worker.py &
cd gateway-manager && python app/main.py &
```

### Docker Deployment (Planned)

```yaml
# docker-compose.yml (root level)
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  
  model-manager:
    build: ./model-manager
    ports: ["8002:8002"]
    volumes: ["./model-manager/models:/app/models"]
  
  task-manager:
    build: ./task-manager
    ports: ["8004:8004"]
    depends_on: [redis]
  
  gateway-manager:
    build: ./gateway-manager
    ports: ["8001:8001"]
    depends_on: [task-manager, model-manager]
  
  worker:
    build: ./cluster-manager
    deploy:
      replicas: 2
    depends_on: [redis, model-manager]
    runtime: nvidia  # For GPU access
```

### Production Deployment

#### Infrastructure Requirements

- **Minimum System**: 16GB RAM, 8 CPU cores, 1 GPU
- **Recommended**: 32GB RAM, 16 CPU cores, 2+ GPUs
- **Storage**: 100GB+ for model cache
- **Network**: Low latency between worker nodes

#### Environment Setup

```bash
# Production environment variables
export ENVIRONMENT=production
export REDIS_URL=redis://production-redis:6379
export MODEL_CACHE_DIR=/data/models
export GPU_MEMORY_FRACTION=0.8
export MAX_WORKERS=4
```

#### Health Checks

Each service provides health endpoints:

- Gateway Manager: `GET /health`
- Model Manager: `GET /health`
- Task Manager: `GET /health`
- Cluster Manager: Redis connectivity + worker status

#### Monitoring

Recommended monitoring stack:

- **Metrics**: Prometheus + Grafana
- **Logs**: ELK Stack or Fluentd
- **Alerting**: PagerDuty integration
- **Uptime**: Service health dashboards

#### Scaling Strategies

1. **Horizontal Scaling**: Add more worker nodes
2. **Vertical Scaling**: Increase GPU memory/cores
3. **Model Optimization**: Use quantized models
4. **Load Balancing**: Multiple gateway instances

## Security Considerations

### API Security
- JWT token authentication
- Rate limiting (10 requests/minute default)
- IP allowlisting for admin endpoints

### Model Security
- Model file integrity checks
- Access logging for model downloads
- Sandboxed execution environment

### Network Security
- TLS encryption for all external APIs
- Internal service mesh (planned)
- VPN access for management interfaces
