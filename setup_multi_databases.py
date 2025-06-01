#!/usr/bin/env python3
"""
Multi-Database Setup for BitingLip Platform
Creates dedicated PostgreSQL databases for each manager service
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configurations for each service
DATABASES = {
    'model_manager': {
        'db_name': 'bitinglip_models',
        'user': 'model_manager',
        'password': 'model_manager_2025!',
        'description': 'Model registry and worker management'
    },
    'task_manager': {
        'db_name': 'bitinglip_tasks',
        'user': 'task_manager', 
        'password': 'task_manager_2025!',
        'description': 'Task orchestration and execution history'
    },
    'gateway_manager': {
        'db_name': 'bitinglip_gateway',
        'user': 'gateway_manager',
        'password': 'gateway_manager_2025!',
        'description': 'API gateway logs and rate limiting'
    },
    'cluster_manager': {
        'db_name': 'bitinglip_cluster',
        'user': 'cluster_manager',
        'password': 'cluster_manager_2025!',
        'description': 'Cluster state and resource management'
    }
}

def connect_as_admin():
    """Connect to PostgreSQL as admin user"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            user='postgres',
            password='postgres',  # Adjust if different
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return conn
    except psycopg2.Error as e:
        logger.error(f"Failed to connect as admin: {e}")
        raise

def database_exists(cursor, db_name):
    """Check if database exists"""
    cursor.execute(
        "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
        (db_name,)
    )
    return cursor.fetchone() is not None

def user_exists(cursor, username):
    """Check if user exists"""
    cursor.execute(
        "SELECT 1 FROM pg_catalog.pg_user WHERE usename = %s",
        (username,)
    )
    return cursor.fetchone() is not None

def create_database_and_user(cursor, config):
    """Create database and user for a service"""
    db_name = config['db_name']
    username = config['user']
    password = config['password']
    description = config['description']
    
    logger.info(f"Setting up {db_name} for {description}")
    
    # Create user if not exists
    if not user_exists(cursor, username):
        cursor.execute(f"""
            CREATE USER {username} WITH
            LOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            INHERIT
            NOREPLICATION
            CONNECTION LIMIT -1
            PASSWORD '{password}';
        """)
        logger.info(f"Created user: {username}")
    else:
        logger.info(f"User {username} already exists")
    
    # Create database if not exists
    if not database_exists(cursor, db_name):
        cursor.execute(f'CREATE DATABASE {db_name} OWNER {username}')
        logger.info(f"Created database: {db_name}")
    else:
        logger.info(f"Database {db_name} already exists")
    
    # Grant permissions
    cursor.execute(f'GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {username}')
    logger.info(f"Granted permissions on {db_name} to {username}")

def setup_databases():
    """Set up all manager databases"""
    try:
        logger.info("Starting multi-database setup for BitingLip platform")
        
        # Connect as admin
        admin_conn = connect_as_admin()
        admin_cursor = admin_conn.cursor()
        
        # Create each database and user
        for service_name, config in DATABASES.items():
            try:
                create_database_and_user(admin_cursor, config)
                logger.info(f"✅ {service_name} database setup completed")
            except Exception as e:
                logger.error(f"❌ Failed to setup {service_name}: {e}")
                continue
        
        admin_cursor.close()
        admin_conn.close()
        
        logger.info("🎉 Multi-database setup completed successfully!")
        
        # Verify connections
        verify_connections()
        
    except Exception as e:
        logger.error(f"Failed to setup databases: {e}")
        sys.exit(1)

def verify_connections():
    """Verify that all database connections work"""
    logger.info("Verifying database connections...")
    
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
            cursor.execute('SELECT version()')
            result = cursor.fetchone()
            if result:
                version = result[0]
            cursor.close()
            conn.close()
            
            logger.info(f"✅ {service_name}: Connection successful")
            
        except Exception as e:
            logger.error(f"❌ {service_name}: Connection failed - {e}")

def print_summary():
    """Print setup summary"""
    print("\n" + "="*60)
    print("BitingLip Multi-Database Setup Summary")
    print("="*60)
    
    for service_name, config in DATABASES.items():
        print(f"""
{service_name.upper().replace('_', ' ')}:
  Database: {config['db_name']}
  User: {config['user']}
  Purpose: {config['description']}
        """)
    
    print("="*60)
    print("Next Steps:")
    print("1. Update manager service configurations to use new databases")
    print("2. Run database migrations for each service")
    print("3. Test service connectivity")
    print("="*60)

if __name__ == "__main__":
    setup_databases()
    print_summary()
