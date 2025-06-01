#!/usr/bin/env python3
import sys
import os
sys.path.append('interfaces/model-context-protocol/servers/memory')
from tools.memory_system import MemorySystem

# Check the actual schema of persona_memories table
print("Checking persona_memories table schema...")
memory = MemorySystem()

if memory.connection_pool:
    try:
        with memory.connection_pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'persona_memories'
                    ORDER BY ordinal_position;
                """)
                columns = cur.fetchall()
        memory.connection_pool.putconn(conn)
        
        print('persona_memories table schema:')
        for col in columns:
            print(f'  {col[0]}: {col[1]}')
            
        # Also check if the table exists at all
        with memory.connection_pool.getconn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'persona_memories'
                    );
                """)
                exists = cur.fetchone()[0]
        memory.connection_pool.putconn(conn)
        
        print(f'\nTable exists: {exists}')
        
    except Exception as e:
        print(f'Error checking schema: {e}')
else:
    print('No database connection available')
