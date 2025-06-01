#!/usr/bin/env python3
"""
Model Manager Database Migration
Migrates from SQLite to PostgreSQL and updates configuration
"""

import sqlite3
import psycopg2
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ModelManagerMigration:
    """Handles migration from SQLite to PostgreSQL for model manager"""
    
    def __init__(self):
        self.sqlite_path = Path("managers/model-manager/model_registry.db")
        self.pg_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'bitinglip_models',
            'user': 'model_manager',
            'password': 'model_manager_2025!'
        }
    
    def create_postgresql_schema(self):
        """Create PostgreSQL schema for model manager"""
        schema_sql = """
        -- Models table
        CREATE TABLE IF NOT EXISTS models (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            size_gb REAL DEFAULT 0.0,
            status TEXT DEFAULT 'available',
            assigned_worker TEXT,
            download_progress REAL DEFAULT 0.0,
            description TEXT,
            tags JSONB DEFAULT '[]'::jsonb,
            capabilities JSONB DEFAULT '[]'::jsonb,
            requirements JSONB DEFAULT '{}'::jsonb,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            last_used TIMESTAMP,
            avg_inference_time REAL DEFAULT 0.0,
            usage_count INTEGER DEFAULT 0
        );

        -- Workers table
        CREATE TABLE IF NOT EXISTS workers (
            id TEXT PRIMARY KEY,
            gpu_index INTEGER NOT NULL,
            hostname TEXT NOT NULL,
            memory_total_gb REAL NOT NULL,
            memory_used_gb REAL DEFAULT 0.0,
            memory_available_gb REAL NOT NULL,
            loaded_models JSONB DEFAULT '[]'::jsonb,
            max_models INTEGER DEFAULT 1,
            status TEXT DEFAULT 'offline',
            last_heartbeat TIMESTAMP NOT NULL,
            error_message TEXT,
            avg_load_time REAL DEFAULT 0.0,
            total_inferences INTEGER DEFAULT 0
        );

        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_models_type ON models(type);
        CREATE INDEX IF NOT EXISTS idx_models_status ON models(status);
        CREATE INDEX IF NOT EXISTS idx_models_worker ON models(assigned_worker);
        CREATE INDEX IF NOT EXISTS idx_workers_status ON workers(status);
        CREATE INDEX IF NOT EXISTS idx_workers_gpu ON workers(gpu_index);
        CREATE INDEX IF NOT EXISTS idx_models_tags ON models USING GIN(tags);
        CREATE INDEX IF NOT EXISTS idx_models_capabilities ON models USING GIN(capabilities);
        CREATE INDEX IF NOT EXISTS idx_workers_loaded_models ON workers USING GIN(loaded_models);

        -- Create audit tables for logging
        CREATE TABLE IF NOT EXISTS model_audit_log (
            id SERIAL PRIMARY KEY,
            model_id TEXT NOT NULL,
            action TEXT NOT NULL,
            old_data JSONB,
            new_data JSONB,
            changed_by TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS worker_audit_log (
            id SERIAL PRIMARY KEY,
            worker_id TEXT NOT NULL,
            action TEXT NOT NULL,
            old_data JSONB,
            new_data JSONB,
            changed_by TEXT,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            conn = psycopg2.connect(**self.pg_config)
            cursor = conn.cursor()
            cursor.execute(schema_sql)
            conn.commit()
            cursor.close()
            conn.close()
            logger.info("✅ PostgreSQL schema created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create PostgreSQL schema: {e}")
            raise
    
    def migrate_data(self):
        """Migrate data from SQLite to PostgreSQL"""
        if not self.sqlite_path.exists():
            logger.warning(f"SQLite database not found at {self.sqlite_path}")
            return
        
        try:
            # Connect to SQLite
            sqlite_conn = sqlite3.connect(str(self.sqlite_path))
            sqlite_conn.row_factory = sqlite3.Row
            sqlite_cursor = sqlite_conn.cursor()
            
            # Connect to PostgreSQL
            pg_conn = psycopg2.connect(**self.pg_config)
            pg_cursor = pg_conn.cursor()
            
            # Migrate models
            self._migrate_models(sqlite_cursor, pg_cursor)
            
            # Migrate workers
            self._migrate_workers(sqlite_cursor, pg_cursor)
            
            pg_conn.commit()
            
            # Close connections
            sqlite_cursor.close()
            sqlite_conn.close()
            pg_cursor.close()
            pg_conn.close()
            
            logger.info("✅ Data migration completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Data migration failed: {e}")
            raise
    
    def _migrate_models(self, sqlite_cursor, pg_cursor):
        """Migrate models table"""
        sqlite_cursor.execute("SELECT * FROM models")
        models = sqlite_cursor.fetchall()
        
        logger.info(f"Migrating {len(models)} models...")
        
        for model in models:
            # Convert SQLite row to dict
            model_data = dict(model)
            
            # Parse JSON fields
            tags = json.loads(model_data['tags']) if model_data['tags'] else []
            capabilities = json.loads(model_data['capabilities']) if model_data['capabilities'] else []
            requirements = json.loads(model_data['requirements']) if model_data['requirements'] else {}
            
            # Convert datetime strings to proper timestamps
            created_at = datetime.fromisoformat(model_data['created_at'])
            updated_at = datetime.fromisoformat(model_data['updated_at'])
            last_used = datetime.fromisoformat(model_data['last_used']) if model_data['last_used'] else None
            
            # Insert into PostgreSQL
            pg_cursor.execute("""
                INSERT INTO models (
                    id, name, type, size_gb, status, assigned_worker, download_progress,
                    description, tags, capabilities, requirements, created_at, updated_at,
                    last_used, avg_inference_time, usage_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    type = EXCLUDED.type,
                    size_gb = EXCLUDED.size_gb,
                    status = EXCLUDED.status,
                    assigned_worker = EXCLUDED.assigned_worker,
                    download_progress = EXCLUDED.download_progress,
                    description = EXCLUDED.description,
                    tags = EXCLUDED.tags,
                    capabilities = EXCLUDED.capabilities,
                    requirements = EXCLUDED.requirements,
                    updated_at = EXCLUDED.updated_at,
                    last_used = EXCLUDED.last_used,
                    avg_inference_time = EXCLUDED.avg_inference_time,
                    usage_count = EXCLUDED.usage_count
            """, (
                model_data['id'], model_data['name'], model_data['type'],
                model_data['size_gb'], model_data['status'], model_data['assigned_worker'],
                model_data['download_progress'], model_data['description'],
                json.dumps(tags), json.dumps(capabilities), json.dumps(requirements),
                created_at, updated_at, last_used,
                model_data['avg_inference_time'], model_data['usage_count']
            ))
        
        logger.info(f"✅ Migrated {len(models)} models")
    
    def _migrate_workers(self, sqlite_cursor, pg_cursor):
        """Migrate workers table"""
        sqlite_cursor.execute("SELECT * FROM workers")
        workers = sqlite_cursor.fetchall()
        
        logger.info(f"Migrating {len(workers)} workers...")
        
        for worker in workers:
            # Convert SQLite row to dict
            worker_data = dict(worker)
            
            # Parse JSON fields
            loaded_models = json.loads(worker_data['loaded_models']) if worker_data['loaded_models'] else []
            
            # Convert datetime strings to proper timestamps
            last_heartbeat = datetime.fromisoformat(worker_data['last_heartbeat'])
            
            # Insert into PostgreSQL
            pg_cursor.execute("""
                INSERT INTO workers (
                    id, gpu_index, hostname, memory_total_gb, memory_used_gb,
                    memory_available_gb, loaded_models, max_models, status,
                    last_heartbeat, error_message, avg_load_time, total_inferences
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    gpu_index = EXCLUDED.gpu_index,
                    hostname = EXCLUDED.hostname,
                    memory_total_gb = EXCLUDED.memory_total_gb,
                    memory_used_gb = EXCLUDED.memory_used_gb,
                    memory_available_gb = EXCLUDED.memory_available_gb,
                    loaded_models = EXCLUDED.loaded_models,
                    max_models = EXCLUDED.max_models,
                    status = EXCLUDED.status,
                    last_heartbeat = EXCLUDED.last_heartbeat,
                    error_message = EXCLUDED.error_message,
                    avg_load_time = EXCLUDED.avg_load_time,
                    total_inferences = EXCLUDED.total_inferences
            """, (
                worker_data['id'], worker_data['gpu_index'], worker_data['hostname'],
                worker_data['memory_total_gb'], worker_data['memory_used_gb'],
                worker_data['memory_available_gb'], json.dumps(loaded_models),
                worker_data['max_models'], worker_data['status'],
                last_heartbeat, worker_data['error_message'],
                worker_data['avg_load_time'], worker_data['total_inferences']
            ))
        
        logger.info(f"✅ Migrated {len(workers)} workers")
    
    def backup_sqlite_database(self):
        """Create backup of SQLite database"""
        if self.sqlite_path.exists():
            backup_path = self.sqlite_path.with_suffix('.db.backup')
            import shutil
            shutil.copy2(self.sqlite_path, backup_path)
            logger.info(f"✅ SQLite database backed up to {backup_path}")
    
    def run_migration(self):
        """Run complete migration process"""
        logger.info("🚀 Starting Model Manager database migration")
        
        try:
            # 1. Backup existing SQLite database
            self.backup_sqlite_database()
            
            # 2. Create PostgreSQL schema
            self.create_postgresql_schema()
            
            # 3. Migrate data
            self.migrate_data()
            
            logger.info("🎉 Model Manager migration completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            raise

if __name__ == "__main__":
    migration = ModelManagerMigration()
    migration.run_migration()
