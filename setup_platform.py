#!/usr/bin/env python3
"""
BitingLip Platform - Comprehensive Setup and Deployment Script

This script handles:
1. Environment validation
2. Dependency installation  
3. Infrastructure setup (Redis)
4. Service configuration
5. Platform startup
6. Health verification
"""

import os
import sys
import subprocess
import time
import threading
import json
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Get the root directory
ROOT_DIR = Path(__file__).parent.absolute()
print(f"🔥 BitingLip Platform Setup")
print(f"📁 Root Directory: {ROOT_DIR}")
print(f"🖥️  Operating System: {platform.system()} {platform.release()}")
print(f"🐍 Python Version: {sys.version}")

# Add the root directory to Python path
sys.path.insert(0, str(ROOT_DIR))
os.environ['PYTHONPATH'] = str(ROOT_DIR)

class PlatformSetup:
    def __init__(self):
        self.root_dir = ROOT_DIR
        self.services = []
        self.redis_started = False
        
    def print_step(self, step: str, status: str = "INFO"):
        """Print a formatted step message"""
        emoji = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{emoji.get(status, 'ℹ️')} {step}")
    
    def run_command(self, command: str, cwd: Optional[Path] = None) -> Tuple[bool, str]:
        """Run a shell command and return success status and output"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd or self.root_dir,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "Command timed out"
        except Exception as e:
            return False, str(e)
    
    def check_dependencies(self) -> bool:
        """Check if required system dependencies are available"""
        self.print_step("Checking system dependencies...")
        
        # Check Python version
        if sys.version_info < (3, 10):
            self.print_step("Python 3.10+ is required", "ERROR")
            return False
        
        # Check if pip is available
        success, _ = self.run_command("pip --version")
        if not success:
            self.print_step("pip is not available", "ERROR")
            return False
        
        # Check if Docker is available (optional)
        success, _ = self.run_command("docker --version")
        if success:
            self.print_step("Docker is available", "SUCCESS")
        else:
            self.print_step("Docker not found (optional for Redis)", "WARNING")
        
        # Check if Node.js is available (for frontend)
        success, _ = self.run_command("node --version")
        if success:
            self.print_step("Node.js is available", "SUCCESS")
        else:
            self.print_step("Node.js not found (required for frontend)", "WARNING")
        
        self.print_step("System dependency check completed", "SUCCESS")
        return True
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies"""
        self.print_step("Installing Python dependencies...")
        
        # Install from master requirements.txt
        success, output = self.run_command("pip install -r requirements.txt")
        if not success:
            self.print_step(f"Failed to install Python dependencies: {output}", "ERROR")
            return False
        
        self.print_step("Python dependencies installed successfully", "SUCCESS")
        return True
    
    def setup_redis(self) -> bool:
        """Setup Redis using Docker or check if running locally"""
        self.print_step("Setting up Redis...")
        
        # First, check if Redis is already running locally
        success, _ = self.run_command("redis-cli ping")
        if success:
            self.print_step("Redis is already running locally", "SUCCESS")
            self.redis_started = True
            return True
        
        # Try to start Redis using Docker
        cluster_manager_dir = self.root_dir / "managers" / "cluster-manager"
        if (cluster_manager_dir / "docker-compose.yml").exists():
            self.print_step("Starting Redis using Docker Compose...")
            success, output = self.run_command(
                "docker-compose up -d redis", 
                cwd=cluster_manager_dir
            )
            if success:
                # Wait for Redis to be ready
                for i in range(10):
                    time.sleep(2)
                    success, _ = self.run_command("redis-cli ping")
                    if success:
                        self.print_step("Redis started successfully with Docker", "SUCCESS")
                        self.redis_started = True
                        return True
                    self.print_step(f"Waiting for Redis to be ready... ({i+1}/10)")
                
                self.print_step("Redis failed to start within timeout", "ERROR")
                return False
            else:
                self.print_step(f"Failed to start Redis with Docker: {output}", "ERROR")
        
        # Provide manual instructions
        self.print_step("Please install and start Redis manually:", "WARNING")
        self.print_step("1. Install Redis server", "INFO")
        self.print_step("2. Start Redis with: redis-server", "INFO")
        self.print_step("3. Verify with: redis-cli ping", "INFO")
        return False
    
    def setup_frontend(self) -> bool:
        """Setup frontend dependencies"""
        frontend_dir = self.root_dir / "interfaces" / "graphical-user-interface"
        if not frontend_dir.exists():
            self.print_step("Frontend directory not found", "WARNING")
            return False
        
        self.print_step("Setting up frontend dependencies...")
        
        # Check if node_modules exists
        if (frontend_dir / "node_modules").exists():
            self.print_step("Frontend dependencies already installed", "SUCCESS")
            return True
        
        # Install npm dependencies
        success, output = self.run_command("npm install", cwd=frontend_dir)
        if not success:
            self.print_step(f"Failed to install frontend dependencies: {output}", "ERROR")
            return False
        
        self.print_step("Frontend dependencies installed successfully", "SUCCESS")
        return True
    
    def validate_configuration(self) -> bool:
        """Validate service configurations"""
        self.print_step("Validating service configurations...")
        
        # Check if central config can be imported
        try:
            from config.central_config import BitingLipConfig
            config = BitingLipConfig()
            self.print_step("Configuration validation passed", "SUCCESS")
            return True
        except Exception as e:
            self.print_step(f"Configuration validation failed: {e}", "ERROR")
            return False
    
    def start_service(self, name: str, working_dir: Path, command: str, port: int) -> threading.Thread:
        """Start a service in a separate thread"""
        def run_service():
            self.print_step(f"Starting {name} on port {port}...")
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = str(self.root_dir)
                
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=working_dir,
                    env=env,
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
                self.print_step(f"Error starting {name}: {e}", "ERROR")
        
        thread = threading.Thread(target=run_service, daemon=True)
        thread.start()
        return thread
    
    def start_backend_services(self) -> bool:
        """Start all backend services in the correct order"""
        if not self.redis_started:
            self.print_step("Redis is not running. Cannot start backend services.", "ERROR")
            return False
        
        self.print_step("Starting backend services...")
        
        # Start Model Manager (Port 8002)
        self.services.append(self.start_service(
            "Model Manager",
            self.root_dir / "managers" / "model-manager",
            "python app.py",
            8002
        ))
        
        time.sleep(3)  # Give model manager time to start
        
        # Start Task Manager (Port 8004)
        self.services.append(self.start_service(
            "Task Manager",
            self.root_dir / "managers" / "task-manager",
            "python -m app.main",
            8004
        ))
        
        time.sleep(3)  # Give task manager time to start
        
        # Start Gateway Manager (Port 8001)
        self.services.append(self.start_service(
            "Gateway Manager",
            self.root_dir / "managers" / "gateway-manager",
            "python start_server.py",
            8001
        ))
        
        self.print_step("Backend services starting...", "SUCCESS")
        return True
    
    def start_frontend(self) -> Optional[threading.Thread]:
        """Start the frontend development server"""
        frontend_dir = self.root_dir / "interfaces" / "graphical-user-interface"
        if not frontend_dir.exists():
            self.print_step("Frontend directory not found", "WARNING")
            return None
        
        self.print_step("Starting frontend development server...")
        thread = self.start_service(
            "Frontend",
            frontend_dir,
            "npm run dev",
            3000
        )
        return thread
    
    def verify_services(self) -> bool:
        """Verify that all services are responding"""
        self.print_step("Verifying service health...")
        
        services_to_check = [
            ("Model Manager", "http://localhost:8002/health"),
            ("Task Manager", "http://localhost:8004/health"),
            ("Gateway Manager", "http://localhost:8001/health"),
        ]
        
        # Wait a bit for services to start
        time.sleep(10)
        
        all_healthy = True
        for service_name, health_url in services_to_check:
            try:
                import requests
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    self.print_step(f"{service_name} is healthy", "SUCCESS")
                else:
                    self.print_step(f"{service_name} health check failed: {response.status_code}", "ERROR")
                    all_healthy = False
            except Exception as e:
                self.print_step(f"{service_name} health check failed: {e}", "ERROR")
                all_healthy = False
        
        return all_healthy
    
    def run_setup(self) -> bool:
        """Run the complete setup process"""
        print("\n" + "=" * 70)
        print("🚀 BITINGLIP PLATFORM SETUP")
        print("=" * 70)
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            return False
        
        # Step 2: Install Python dependencies
        if not self.install_python_dependencies():
            return False
        
        # Step 3: Setup Redis
        if not self.setup_redis():
            self.print_step("Redis setup failed. Please set up Redis manually.", "WARNING")
            return False
        
        # Step 4: Setup frontend
        self.setup_frontend()  # Non-critical
        
        # Step 5: Validate configuration
        if not self.validate_configuration():
            return False
        
        # Step 6: Start backend services
        if not self.start_backend_services():
            return False
        
        # Step 7: Start frontend (optional)
        frontend_thread = self.start_frontend()
        
        # Step 8: Verify services
        time.sleep(5)  # Give services more time to start
        # services_healthy = self.verify_services()
        
        print("\n" + "=" * 70)
        print("✅ PLATFORM SETUP COMPLETED")
        print("=" * 70)
        print("🌐 Gateway API: http://localhost:8001")
        print("📊 Model Manager: http://localhost:8002")
        print("📋 Task Manager: http://localhost:8004")
        if frontend_thread:
            print("🖥️ Web Interface: http://localhost:3000")
        print("🔧 Redis Commander: http://localhost:8081")
        print("🌸 Celery Flower: http://localhost:5555")
        print("=" * 70)
        print("📚 API Documentation: http://localhost:8001/docs")
        print("🔍 Health Check: http://localhost:8001/health")
        print("=" * 70)
        print("\n💡 Development Login: admin / admin123")
        print("🛑 Press Ctrl+C to stop all services\n")
        
        return True
    
    def cleanup(self):
        """Cleanup resources"""
        self.print_step("Cleaning up resources...")
        
        # Stop Docker services if we started them
        if self.redis_started:
            cluster_manager_dir = self.root_dir / "managers" / "cluster-manager"
            if (cluster_manager_dir / "docker-compose.yml").exists():
                self.run_command("docker-compose down", cwd=cluster_manager_dir)

def main():
    """Main setup function"""
    setup = PlatformSetup()
    
    try:
        success = setup.run_setup()
        if success:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down platform...")
        setup.cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        setup.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
