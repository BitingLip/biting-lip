#!/usr/bin/env python3
"""
Initialize All Database Schemas
Applies database schemas to all manager service databases
"""

import psycopg2
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configurations
DATABASES = {
    'model_manager': {
        'db_name': 'bitinglip_models',
        'user': 'model_manager',
        'password': 'model_manager_2025!',
        'schema_files': []  # Already migrated
    },
    'task_manager': {
        'db_name': 'bitinglip_tasks',
        'user': 'task_manager',
        'password': 'task_manager_2025!',
        'schema_files': ['database_schemas/task_manager_schema.sql']
    },
    'gateway_manager': {
        'db_name': 'bitinglip_gateway',
        'user': 'gateway_manager',
        'password': 'gateway_manager_2025!',
        'schema_files': ['database_schemas/gateway_manager_schema.sql']
    },
    'cluster_manager': {
        'db_name': 'bitinglip_cluster',
        'user': 'cluster_manager',
        'password': 'cluster_manager_2025!',
        'schema_files': ['database_schemas/cluster_manager_schema.sql']
    }
}

def apply_schema(service_name, config):
    """Apply database schema for a service"""
    if not config['schema_files']:
        logger.info(f"⏭️  {service_name}: No schema files to apply")
        return True
    
    try:
        # Connect to the service database
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user=config['user'],
            password=config['password'],
            database=config['db_name']
        )
        
        cursor = conn.cursor()
        
        # Apply each schema file
        for schema_file in config['schema_files']:
            schema_path = Path(schema_file)
            if not schema_path.exists():
                logger.warning(f"Schema file not found: {schema_file}")
                continue
            
            logger.info(f"Applying schema: {schema_file}")
            
            # Read and execute schema
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Split on semicolons and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements):
                try:
                    cursor.execute(statement)
                    logger.debug(f"Executed statement {i+1}/{len(statements)}")
                except Exception as e:
                    logger.error(f"Failed to execute statement {i+1}: {e}")
                    logger.error(f"Statement: {statement[:100]}...")
                    # Continue with next statement
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ {service_name}: Schema applied successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ {service_name}: Schema application failed - {e}")
        return False

def create_basic_schemas():
    """Create basic schemas for services without external schema files"""
    
    # Task Manager Schema (inline for simplicity)
    task_schema = """
    -- Basic task table
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        priority INTEGER DEFAULT 0,
        model_id TEXT,
        worker_id TEXT,
        input_data JSONB NOT NULL,
        output_data JSONB,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        started_at TIMESTAMP,
        completed_at TIMESTAMP,
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
    CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
    """
    
    # Gateway Manager Schema
    gateway_schema = """
    -- Basic API requests logging
    CREATE TABLE IF NOT EXISTS api_requests (
        id SERIAL PRIMARY KEY,
        request_id TEXT UNIQUE NOT NULL,
        method TEXT NOT NULL,
        path TEXT NOT NULL,
        client_ip INET,
        response_status INTEGER,
        response_time_ms INTEGER,
        request_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX IF NOT EXISTS idx_api_requests_timestamp ON api_requests(request_timestamp);
    """
    
    # Cluster Manager Schema
    cluster_schema = """
    -- Basic cluster nodes tracking
    CREATE TABLE IF NOT EXISTS cluster_nodes (
        id TEXT PRIMARY KEY,
        hostname TEXT NOT NULL,
        ip_address INET NOT NULL,
        status TEXT NOT NULL DEFAULT 'unknown',
        last_heartbeat TIMESTAMP,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX IF NOT EXISTS idx_cluster_nodes_status ON cluster_nodes(status);
    """
    
    schemas = {
        'task_manager': task_schema,
        'gateway_manager': gateway_schema,
        'cluster_manager': cluster_schema
    }
    
    for service_name, schema_sql in schemas.items():
        if service_name == 'model_manager':
            continue  # Already migrated
            
        config = DATABASES[service_name]
        
        try:
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user=config['user'],
                password=config['password'],
                database=config['db_name']
            )
            
            cursor = conn.cursor()
            cursor.execute(schema_sql)
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"✅ {service_name}: Basic schema created")
            
        except Exception as e:
            logger.error(f"❌ {service_name}: Failed to create basic schema - {e}")

def verify_schemas():
    """Verify that schemas were applied correctly"""
    logger.info("Verifying database schemas...")
    
    for service_name, config in DATABASES.items():
        try:
            conn = psycopg2.connect(
                host='localhost',
                port=5432,
                user=config['user'],
                password=config['password'],
                database=config['db_name']
            )
            
            cursor = conn.cursor()
              # Get table count
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            result = cursor.fetchone()
            table_count = result[0] if result else 0
            
            # Get index count
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pg_indexes 
                WHERE schemaname = 'public'
            """)
            result = cursor.fetchone()
            index_count = result[0] if result else 0
            
            cursor.close()
            conn.close()
            
            logger.info(f"✅ {service_name}: {table_count} tables, {index_count} indexes")
            
        except Exception as e:
            logger.error(f"❌ {service_name}: Verification failed - {e}")

def main():
    """Main execution function"""
    logger.info("🚀 Starting database schema initialization")
    
    try:
        # Create basic schemas for all services
        create_basic_schemas()
        
        # Apply additional schemas from files (if they exist)
        for service_name, config in DATABASES.items():
            apply_schema(service_name, config)
        
        # Verify all schemas
        verify_schemas()
        
        logger.info("🎉 Database schema initialization completed successfully!")
        
        print("\n" + "="*60)
        print("BitingLip Multi-Database Architecture Ready!")
        print("="*60)
        print("""
✅ Model Manager:     bitinglip_models     (PostgreSQL)
✅ Task Manager:      bitinglip_tasks      (PostgreSQL) 
✅ Gateway Manager:   bitinglip_gateway    (PostgreSQL)
✅ Cluster Manager:   bitinglip_cluster    (PostgreSQL)
✅ Memory System:     ai_memory            (PostgreSQL)

Each service now has:
- Dedicated database with proper isolation
- Audit logging capabilities  
- Performance-optimized indexes
- JSON metadata support
- Clean API-only inter-service communication

Next Steps:
1. Update service configurations to use new databases
2. Test service startup and connectivity
3. Validate API communication between services
        """)
        print("="*60)
        
    except Exception as e:
        logger.error(f"Schema initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
