#!/usr/bin/env python3
"""
Start BitingLip Platform Services
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.absolute()
os.environ['PYTHONPATH'] = str(ROOT_DIR)

def main():
    print("🔥 Starting BitingLip Platform Services...")
    
    # Start Model Manager
    print("🚀 Starting Model Manager...")
    subprocess.Popen([
        sys.executable, "app.py"
    ], cwd=ROOT_DIR / "managers" / "model-manager")
    
    # Start Task Manager  
    print("🚀 Starting Task Manager...")
    subprocess.Popen([
        sys.executable, "-m", "app.main"
    ], cwd=ROOT_DIR / "managers" / "task-manager")
    
    # Start Gateway Manager
    print("🚀 Starting Gateway Manager...")
    subprocess.Popen([
        sys.executable, "start_server.py"  
    ], cwd=ROOT_DIR / "managers" / "gateway-manager")
    
    print("✅ All services started!")
    print("🌐 API Gateway: http://localhost:8001")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
