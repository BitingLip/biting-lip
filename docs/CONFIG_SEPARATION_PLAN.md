# BitingLip Configuration Separation Plan

## Moving to True Microservice Architecture

### 🎯 **Objective**

Transform BitingLip from shared-config architecture to true microservices with proper configuration boundaries.

---

## 📁 **Recommended Structure**

### **CENTRAL CONFIG** (Keep in `/config/`)

**Purpose:** Platform-wide settings that affect multiple services

```
/config/
├── environments/
│   ├── base.env          # Platform defaults (APP_NAME, LOG_LEVEL, etc.)
│   ├── development.env   # Dev environment overrides
│   ├── production.env    # Prod environment overrides
│   └── staging.env       # Staging environment overrides
├── central_config.py     # Configuration loading logic
└── service_discovery.py  # Service URL resolution & health checks
```

**Central Settings Should Include:**

- `APP_NAME=BitingLip`
- `APP_VERSION=1.0.0`
- `LOG_LEVEL=INFO`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- `SECRET_KEY_LENGTH=32`
- `TOKEN_EXPIRE_HOURS=24`
- `HEALTH_CHECK_INTERVAL=30`
- `PROMETHEUS_PORT=9090`
- Service discovery URLs and ports

---

### **SERVICE-SPECIFIC CONFIG** (Move to each service)

#### **Model Manager** (`/managers/model-manager/config/`)

```
/managers/model-manager/config/
├── model-manager.env     # Service-specific settings
├── model-manager-db.env  # Database configuration
└── local.env            # Local development overrides
```

**Should Include:**

- `MODEL_CACHE_DIR=./models`
- `MAX_MODEL_CACHE_SIZE_GB=50.0`
- `MODEL_LOAD_TIMEOUT=300`
- `MODEL_DB_HOST=localhost`
- `MODEL_DB_NAME=bitinglip_models`
- `MODEL_REGISTRY_CACHE_TTL=300`
- HuggingFace API settings
- Model download configurations

#### **Cluster Manager** (`/managers/cluster-manager/config/`)

```
/managers/cluster-manager/config/
├── cluster-manager.env
├── cluster-manager-db.env
└── local.env
```

**Should Include:**

- Cluster orchestration settings
- Node management configuration
- Scaling policies
- Cluster database settings

#### **Task Manager** (`/managers/task-manager/config/`)

```
/managers/task-manager/config/
├── task-manager.env
├── task-manager-db.env
└── local.env
```

**Should Include:**

- Task queue settings
- Worker pool configurations
- Task timeout settings
- Task database settings

#### **Gateway Manager** (`/managers/gateway-manager/config/`)

```
/managers/gateway-manager/config/
├── gateway-manager.env
├── gateway-manager-db.env
└── local.env
```

**Should Include:**

- API gateway settings
- Routing configurations
- Rate limiting
- Authentication settings

---

## 🔄 **Migration Steps**

### **Phase 1: Analyze & Categorize** ✅

- [x] Identify platform-wide vs service-specific settings
- [x] Document current configuration dependencies

### **Phase 2: Move Service-Specific Configs** ✅

1. ✅ Create `config/` directories in each manager
2. ✅ Move service-specific `.env` files:
   - ✅ `config/services/model-manager*.env` → `managers/model-manager/config/`
   - ✅ `config/services/cluster-manager*.env` → `managers/cluster-manager/config/`
   - ✅ `config/services/task-manager*.env` → `managers/task-manager/config/`
   - ✅ `config/services/gateway-manager*.env` → `managers/gateway-manager/config/`
3. ✅ Move infrastructure configs:
   - ✅ `config/services/services_*.env` → `config/infrastructure/`
   - ✅ `config/services/worker.env` → `managers/cluster-manager/config/workers/`
   - ✅ `config/services/mcp-*.env` → `interfaces/model-context-protocol/config/`
4. ✅ Create local.env files for development overrides
5. ✅ Clean up old central services directory

### **Phase 3: Update Configuration Loading** ✅

- ✅ Create distributed configuration loader (`config/distributed_config.py`)
- ✅ Modify model-manager to use new configuration loading
- ✅ Test and verify configuration migration working
- 🔄 Update remaining services (cluster-manager, task-manager, gateway-manager)
- 🔄 Update service discovery for inter-service communication

### **Phase 4: Clean Up Central Config** 🔄

- 🔄 Remove service-specific settings from central config
- 🔄 Keep only platform-wide defaults
- 🔄 Update documentation

---

## 🎁 **Benefits**

### **True Microservice Independence**

- Each service owns its configuration
- Services can be deployed independently
- No shared configuration dependencies

### **Better Development Experience**

- Clearer separation of concerns
- Easier to understand what affects what service
- Local development configurations per service

### **Improved Scalability**

- Services can have different scaling configurations
- Database settings specific to service needs
- Independent monitoring and alerting

### **Enhanced Security**

- Service-specific secrets and keys
- Granular access control
- Reduced blast radius for configuration errors

---

## 🚀 **Implementation Priority**

1. **High Priority:** Database configurations (already moved)
2. **Medium Priority:** Service-specific runtime settings
3. **Low Priority:** Shared infrastructure settings (Redis, monitoring)

---

Would you like me to start implementing this migration plan?
