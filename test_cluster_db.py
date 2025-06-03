#!/usr/bin/env python3
"""
Test PostgreSQL connection and create cluster manager database/schema
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

def test_postgres_connection():
    """Test basic PostgreSQL connection"""
    try:
        # Try to connect to default postgres database
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='postgres', 
            user='postgres',
            password='password'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        print("✅ PostgreSQL connection successful")
        
        # Check if cluster_manager database exists
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='cluster_manager'")
        db_exists = cursor.fetchone()
        
        if not db_exists:
            print("📦 Creating cluster_manager database...")
            cursor.execute("CREATE DATABASE cluster_manager")
            print("✅ cluster_manager database created")
        else:
            print("✅ cluster_manager database already exists")
            
        cursor.close()
        conn.close()
        
        # Test connection to cluster_manager database
        cluster_conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='cluster_manager',
            user='postgres', 
            password='password'
        )
        
        print("✅ cluster_manager database connection successful")
        
        # Check if schema exists
        cursor = cluster_conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'cluster_nodes'
        """)
        schema_exists = cursor.fetchone()
        
        if not schema_exists:
            print("🏗️  Need to create cluster schema")
            return cluster_conn, False
        else:
            print("✅ Cluster schema already exists")
            return cluster_conn, True
            
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        print("💡 Make sure PostgreSQL is running and accessible")
        return None, False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None, False

def create_cluster_schema(conn):
    """Create the cluster manager schema"""
    try:
        with open('managers/cluster-manager/database/cluster_manager_schema.sql', 'r') as f:
            schema_sql = f.read()
        
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Cluster manager schema created successfully")
        cursor.close()
        return True
        
    except FileNotFoundError:
        print("❌ Schema file not found: managers/cluster-manager/database/cluster_manager_schema.sql")
        return False
    except Exception as e:
        print(f"❌ Failed to create schema: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing PostgreSQL connection for cluster manager...")
    
    conn, schema_exists = test_postgres_connection()
    
    if conn:
        if not schema_exists:
            if create_cluster_schema(conn):
                print("🎉 Database setup complete!")
            else:
                print("❌ Database setup failed")
                sys.exit(1)
        else:
            print("🎉 Database already configured!")
        
        conn.close()
    else:
        print("❌ Cannot proceed without database connection")
        sys.exit(1)
