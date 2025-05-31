"""
Common utility functions shared across BitingLip modules.
"""

import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Any


def generate_task_id() -> str:
    """Generate a unique task identifier"""
    timestamp = int(time.time() * 1000)  # milliseconds
    unique_part = str(uuid.uuid4())[:8]
    return f"task_{timestamp}_{unique_part}"


def generate_worker_id(gpu_index: int) -> str:
    """Generate a worker identifier"""
    return f"worker-gpu{gpu_index}-{int(time.time())}"


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to ISO string with UTC timezone"""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.isoformat()


def parse_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO timestamp string to datetime"""
    return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))


def validate_gpu_index(gpu_index: int, max_gpus: int = 8) -> bool:
    """Validate GPU index is within acceptable range"""
    return 0 <= gpu_index < max_gpus


def format_memory_size(bytes_size: float) -> str:
    """Format bytes to human readable memory size"""
    size = float(bytes_size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} PB"


def safe_get(dictionary: dict, key: str, default: Any = None) -> Any:
    """Safely get value from dictionary with nested key support"""
    try:
        keys = key.split('.')
        value = dictionary
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default


def retry_on_exception(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying functions that may raise exceptions"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay * (2 ** attempt))  # Exponential backoff
            return None
        return wrapper
    return decorator
