# BitingLip Web UI

🚧 **Status: In Development**

Vue.js-based web interface for managing the BitingLip AI inference platform. Provides a modern, responsive dashboard for cluster management, task monitoring, and system administration.

## Core Features

- 🚧 Cluster management dashboard (planned)
- 🚧 Real-time task and worker monitoring (planned)
- 🚧 Model management interface (planned)
- 🚧 System metrics and analytics (planned)
- 🚧 User authentication and authorization (planned)
- 🚧 Mobile-responsive design (planned)
- 🚧 Dark/light theme support (planned)

## Quick Start

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The development server will start on `http://localhost:3000`

## Documentation

See [docs/](docs/) for detailed documentation:
- [Architecture](docs/architecture.md) - Frontend architecture and design
- [Development Guide](docs/development.md) - Setup and development workflow
- [Component Library](docs/components.md) - UI component documentation
- [Deployment Guide](docs/deployment.md) - Production deployment

## Integration

The Web UI integrates with:
- **Gateway Manager**: API communication for all operations
- **Cluster Manager**: Real-time cluster monitoring
- **Model Manager**: Model browser and management
- **Task Manager**: Task dashboard and analytics

## Configuration

Key configuration options:
```bash
# API endpoint
VITE_API_URL=http://localhost:8080

# Authentication
VITE_AUTH_ENABLED=true

# Theme
VITE_DEFAULT_THEME=light

# Refresh intervals
VITE_REFRESH_INTERVAL=5000
```

See [docs/configuration.md](docs/configuration.md) for complete configuration options.manage models, search, preload, etc
- manage gateways accounts and api keys.
- 