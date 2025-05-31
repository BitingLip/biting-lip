#!/usr/bin/env python3
"""
BitingLip Platform - Quick Start Launcher

This is a simple wrapper that calls the comprehensive setup script.
Use setup_platform.py for full control, or this for quick testing.
"""
import subprocess
import sys
from pathlib import Path

def main():
    """Launch the comprehensive platform setup"""
    print("🚀 BitingLip Quick Start")
    print("=" * 50)
    print("This will start the complete BitingLip platform...")
    print("For more control, use: python setup_platform.py")
    print("=" * 50)
    
    # Call the comprehensive setup script
    setup_script = Path(__file__).parent / "setup_platform.py"
    
    try:
        subprocess.run([sys.executable, str(setup_script)], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Quick start interrupted by user")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed with exit code: {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
