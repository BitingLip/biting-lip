# Common Utilities and Shared Code

This directory contains shared utilities, models, and configurations used across multiple BitingLip modules.

## Structure

- `models/` - Shared data models and schemas
- `utils/` - Common utility functions
- `config/` - Shared configuration classes
- `logging/` - Centralized logging setup
- `api/` - Shared API client helpers

## Usage

Each module can import from common using:

```python
from common.models import TaskRequest, ModelSpec
from common.utils import format_timestamp, validate_gpu_index
from common.logging import get_logger
```

## Guidelines

- Only add truly shared code here
- Avoid module-specific logic
- Keep dependencies minimal
- Document all public interfaces
