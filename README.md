# BitingLip

A distributed AI inference platform with modular microservices architecture. BitingLip provides scalable, GPU-accelerated AI model serving with support for multiple model types including text generation, image generation, and more.

## 🚀 Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/BitingLip/biting-lip.git
cd biting-lip

# Start Redis (required)
cd cluster-manager && docker-compose up -d redis && cd ..

# Start core services
cd managers/model-manager && python app/main.py &      # Port 8002
cd managers/task-manager && python app/main.py &      # Port 8004  
cd managers/cluster-manager/cluster/worker && python app/worker.py &
cd managers/gateway-manager && python app/main.py     # Port 8001
```

## 📋 Project Overview

| Module | Status | Purpose | Documentation |
|--------|--------|---------|---------------|
| 🖥️ **[cluster-manager](managers/cluster-manager/)** | ⚙️ **Operational** | GPU cluster & worker management | [📖 Docs](managers/cluster-manager/docs/) |
| 🌐 **[gateway-manager](managers/gateway-manager/)** | 🛠️ **In Progress** | API gateway & request routing | [📖 Docs](managers/gateway-manager/docs/) |
| 📦 **[model-manager](managers/model-manager/)** | ⚙️ **Operational** | Model storage & management | [📖 Docs](managers/model-manager/docs/) |
| 📋 **[task-manager](managers/task-manager/)** | 🚧 **In Development** | Task scheduling & lifecycle | [📖 Docs](managers/task-manager/docs/) |
| 💻 **[command-line-interface](interfaces/command-line-interface/)** | 🚧 **Planned** | CLI tools & utilities | [📖 Docs](interfaces/command-line-interface/docs/) |
| 🎨 **[graphical-user-interface](graphical-user-interface/)** | 🚧 **Planned** | Web interface | [📖 Docs](graphical-user-interface/docs/) |

**Status Legend:**
- ⚙️ **Operational**: Fully functional and tested
- 🛠️ **In Progress**: Core functionality working, some features pending  
- 🚧 **In Development**: Basic structure in place, actively being developed
- � **Planned**: Structure defined, implementation pending

## ✨ Features

- 🚀 **Distributed GPU Computing**: Scalable worker nodes with GPU acceleration
- 🤖 **Multi-Model Support**: Text generation, image generation, embeddings, and more
- 🔄 **Task Queue Management**: Robust task scheduling with Celery and Redis
- 📊 **Centralized Model Storage**: Unified model management across all workers
- 🌐 **RESTful API**: Clean HTTP API for all operations
- 📈 **Monitoring & Metrics**: Real-time system and task monitoring

## 📚 Documentation

- **[🏗️ Architecture Overview](docs/architecture.md)** - System design and component interaction
- **[🛠️ Development Guide](docs/development.md)** - Setup, workflow, and contribution guidelines  
- **[🚀 Deployment Guide](docs/deployment.md)** - Production deployment and scaling
- **[📋 Project Structure](PROJECT_STRUCTURE.md)** - Complete directory tree and file descriptions

## 🔧 Development

1.  Navigate to the specific submodule directory you want to work on (e.g., `cd cluster-manager`).
2.  Make your changes, commit them, and push them to the submodule's own remote repository (e.g., `git push origin main`).
3.  Navigate back to the parent `biting-lip` repository (e.g., `cd ..`).
4.  The parent repository will now see that the submodule has new changes. Stage this change:
    ```bash
    git add <submodule-name> 
    # Example: git add cluster-manager
    ```
5.  Commit the update to the parent repository, which records the new commit hash for the submodule:
    ```bash
    git commit -m "Update <submodule-name> to latest version"
    # Example: git commit -m "Update cluster-manager to latest version"
    ```
6.  Push the changes in the parent repository:
    ```bash
    git push
    ```

## Submodule Repositories

- [cluster-manager](https://github.com/BitingLip/cluster-manager)
- [gateway-manager](https://github.com/BitingLip/gateway-manager)
- [model-manager](https://github.com/BitingLip/model-manager)
- [task-manager](https://github.com/BitingLip/task-manager)
- [user-interface](https://github.com/BitingLip/user-interface)
