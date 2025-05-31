# BitingLip Development Guide

## Getting Started

### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended)
- Redis server
- Git with submodule support

### Quick Setup

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/BitingLip/biting-lip.git
cd biting-lip

# Start Redis (required for cluster operations)
docker-compose -f managers/cluster-manager/docker-compose.yml up -d redis

# Install dependencies for each module
cd managers/cluster-manager/cluster/worker && pip install -r requirements.txt
cd ../../../gateway-manager && pip install -r requirements.txt
cd ../model-manager && pip install -r requirements.txt
cd ../task-manager && pip install -r requirements.txt
```

## Development Workflow

### Starting the System

1. **Start Redis** (always first):
   ```bash
   cd cluster-manager && docker-compose up -d redis
   ```

2. **Start Model Manager** (manages centralized models):
   ```bash
   cd model-manager && python app/main.py
   # Available at http://localhost:8002
   ```

3. **Start Task Manager** (handles task scheduling):
   ```bash
   cd task-manager && python app/main.py
   # Available at http://localhost:8004
   ```

4. **Start Cluster Workers** (GPU processing):
   ```bash
   cd managers/cluster-manager/cluster/worker && python app/worker.py
   ```

5. **Start Gateway Manager** (API entry point):
   ```bash
   cd gateway-manager && python app/main.py
   # Available at http://localhost:8001
   ```

### Module Development

Each module follows the same structure:
```
module-name/
├── README.md              # Quick overview with links
├── requirements.txt       # Dependencies
├── docs/                  # Detailed documentation
│   ├── api.md            # API reference
│   ├── architecture.md   # Module architecture
│   └── development.md    # Development guide
├── app/                   # Application code
├── tests/                 # Test suite
└── .env.example          # Environment template
```

### Testing

```bash
# Run module-specific tests
cd <module-name>
python -m pytest tests/

# Run smoke tests
python tests/test_smoke.py

# Integration tests (from root)
python tests/test_integration.py
```

### Code Standards

- **Python**: PEP 8 compliance
- **Type Hints**: Required for all public APIs
- **Documentation**: Docstrings for all functions
- **Testing**: Minimum 80% coverage for new code

## Common Development Tasks

### Adding a New Model Type

1. Update `common/models/__init__.py` with new TaskType
2. Add model support in `model-manager/app/services.py`
3. Implement task handler in `cluster-manager/cluster/worker/app/tasks.py`
4. Update API schemas in `gateway-manager/app/schemas.py`

### Adding a New API Endpoint

1. Define schema in appropriate `schemas.py`
2. Implement business logic in `services/` directory
3. Add route in main module
4. Update documentation
5. Add tests

### Debugging Common Issues

#### Worker Not Finding Models
```bash
# Check model cache directory
ls -la model-manager/models/

# Verify worker configuration
cat cluster-manager/cluster/worker/.env
```

#### Redis Connection Issues
```bash
# Check Redis status
docker-compose -f cluster-manager/docker-compose.yml ps redis

# Test Redis connectivity
redis-cli ping
```

#### Import Errors with Common Module
```bash
# Ensure common module is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/common"
```

## Release Process

1. Update version numbers in all `main.py` files
2. Update CHANGELOG.md
3. Run full test suite
4. Create release branch
5. Deploy to staging
6. Performance testing
7. Production deployment
