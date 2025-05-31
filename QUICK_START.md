# BitingLip Platform - Quick Start Guide

## 🚀 One-Command Setup

```bash
# Clone and setup the entire platform
git clone https://github.com/BitingLip/biting-lip.git
cd biting-lip
python setup_platform.py
```

This single command will:

- ✅ Check system dependencies
- ✅ Install Python packages
- ✅ Setup Redis infrastructure
- ✅ Configure all services
- ✅ Start the complete platform
- ✅ Validate functionality

## 🎯 What You Get

After running the setup, you'll have:

| Service               | URL                        | Purpose                 |
| --------------------- | -------------------------- | ----------------------- |
| **Web Interface**     | http://localhost:3000      | Modern Vue.js dashboard |
| **API Gateway**       | http://localhost:8001      | Main API endpoint       |
| **API Documentation** | http://localhost:8001/docs | Interactive API docs    |
| **Model Manager**     | http://localhost:8002      | Model management API    |
| **Task Manager**      | http://localhost:8004      | Task scheduling API     |
| **Redis Commander**   | http://localhost:8081      | Redis database UI       |
| **Celery Flower**     | http://localhost:5555      | Task queue monitoring   |

## 🔐 Default Login

```
Username: admin
Password: admin123
```

## 🧪 Validate Installation

```bash
# Run comprehensive validation tests
python validate_platform.py
```

## 📱 Quick Test

1. **Web Interface**: Visit http://localhost:3000
2. **Login**: Use admin/admin123
3. **Dashboard**: View real-time system metrics
4. **Models**: Download a test model (e.g., GPT-2)
5. **Tasks**: Create and monitor inference tasks

## 🔧 Manual Setup (If Needed)

### Prerequisites

```bash
# Python 3.10+
python --version

# Redis (via Docker)
docker --version

# Node.js (for frontend)
node --version
```

### Step-by-Step Setup

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Start Redis
cd managers/cluster-manager
docker-compose up -d redis
cd ../..

# 3. Start services (in separate terminals)
cd managers/model-manager && python app.py         # Port 8002
cd managers/task-manager && python -m app.main     # Port 8004
cd managers/gateway-manager && python start_server.py  # Port 8001

# 4. Start frontend (optional)
cd interfaces/graphical-user-interface
npm install
npm run dev  # Port 3000
```

## 🚨 Troubleshooting

### Redis Connection Issues

```bash
# Check if Redis is running
redis-cli ping

# Start Redis manually
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### Service Not Starting

```bash
# Check Python path
echo $PYTHONPATH

# Check port availability
netstat -an | grep :8001

# View service logs
python -m app.main  # For detailed error messages
```

### Permission Issues (Windows)

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### GPU Issues

```bash
# Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Install GPU support (NVIDIA)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install DirectML support (AMD/Intel)
pip install torch-directml
```

## 🔗 Important Links

- **Documentation**: [docs/](docs/)
- **Architecture**: [docs/architecture.md](docs/architecture.md)
- **API Reference**: http://localhost:8001/docs
- **Development Guide**: [docs/development.md](docs/development.md)

## 🆘 Getting Help

1. **Check Logs**: Service logs appear in terminal windows
2. **Health Checks**: Visit `/health` endpoints for each service
3. **Validation Script**: Run `python validate_platform.py`
4. **Issues**: Create GitHub issue with logs and error details

## 🎉 Next Steps

1. **Explore the Dashboard**: Navigate through all sections
2. **Download Models**: Try different AI models from HuggingFace
3. **Run Inference**: Test text generation and image synthesis
4. **Monitor Performance**: Use the monitoring dashboard
5. **API Integration**: Build custom applications using the API

---

**💡 Pro Tip**: The platform runs entirely locally, so no internet connection is required after initial setup (except for downloading new models).
