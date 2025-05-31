#!/usr/bin/env python3
"""
BitingLip Platform Startup Script
Starts all required services in the correct order with proper Python path configuration
"""
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# Get the root directory
ROOT_DIR = Path(__file__).parent.absolute()
print(f"BitingLip Root Directory: {ROOT_DIR}")

# Add the root directory to Python path
sys.path.insert(0, str(ROOT_DIR))
os.environ['PYTHONPATH'] = str(ROOT_DIR)

def start_service(name, working_dir, command, port):
    """Start a service in a separate thread"""
    def run_service():
        print(f"🚀 Starting {name} on port {port}...")
        try:
            env = os.environ.copy()
            env['PYTHONPATH'] = str(ROOT_DIR)
            process = subprocess.Popen(
                command,
                cwd=working_dir,
                env=env,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Print output in real-time
            if process.stdout:
                for line in process.stdout:
                    print(f"[{name}] {line.strip()}")
                
        except Exception as e:
            print(f"❌ Error starting {name}: {e}")
    
    thread = threading.Thread(target=run_service, daemon=True)
    thread.start()
    return thread

def main():
    print("=" * 60)
    print("🔥 BitingLip AI GPU Cluster Platform")
    print("=" * 60)
    
    services = []
    
    # Start Model Manager (Port 8002)
    services.append(start_service(
        "Model Manager",
        ROOT_DIR / "managers" / "model-manager",
        "python app.py",
        8002
    ))
    
    time.sleep(2)  # Give model manager time to start
    
    # Start Task Manager (Port 8004)  
    services.append(start_service(
        "Task Manager", 
        ROOT_DIR / "managers" / "task-manager",
        "python -m app.main",
        8004
    ))
    
    time.sleep(2)  # Give task manager time to start
    
    # Start Gateway Manager (Port 8001)
    services.append(start_service(
        "Gateway Manager",
        ROOT_DIR / "managers" / "gateway-manager", 
        "python start_server.py",
        8001
    ))
    
    print("\n" + "=" * 60)
    print("✅ All services starting...")
    print("🌐 Gateway API: http://localhost:8001")
    print("📊 Model Manager: http://localhost:8002") 
    print("📋 Task Manager: http://localhost:8004")
    print("🖥️ Web UI: http://localhost:3000")
    print("=" * 60)
    print("\nPress Ctrl+C to stop all services...")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        sys.exit(0)

if __name__ == "__main__":
    main()
