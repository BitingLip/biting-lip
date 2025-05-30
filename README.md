# BitingLip

A distributed system architecture with modular components managed as Git submodules.

## Architecture

This repository contains the main orchestration layer for the BitingLip system, which consists of four core components:

- **cluster-manager**: Manages cluster orchestration and resource allocation
- **gateway-manager**: Handles API gateway and routing functionality  
- **model-manager**: Manages ML models and inference services
- **task-manager**: Coordinates task scheduling and execution

## Getting Started

### Initial Setup

When cloning this repository for the first time, you need to initialize and update the submodules:

```bash
git clone https://github.com/BitingLip/biting-lip.git
cd biting-lip
git submodule init
git submodule update
```

Or clone with submodules in one command:

```bash
git clone --recurse-submodules https://github.com/BitingLip/biting-lip.git
```

### Working with Submodules

#### Updating all submodules to latest:
```bash
git submodule update --remote
```

#### Updating a specific submodule:
```bash
cd cluster-manager
git pull origin main
cd ..
git add cluster-manager
git commit -m "Update cluster-manager submodule"
```

#### Checking submodule status:
```bash
git submodule status
```

### Development Workflow

1. Make changes in individual submodule repositories
2. Commit and push changes to the submodule's repository
3. Update the main repository to reference the new commit:
   ```bash
   git add <submodule-name>
   git commit -m "Update <submodule-name> to latest version"
   git push
   ```

## Submodule Repositories

- [cluster-manager](https://github.com/BitingLip/cluster-manager)
- [gateway-manager](https://github.com/BitingLip/gateway-manager)
- [model-manager](https://github.com/BitingLip/model-manager)
- [task-manager](https://github.com/BitingLip/task-manager)
