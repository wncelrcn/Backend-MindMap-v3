#!/usr/bin/env python3
"""
Setup script for the Emotion Analysis API backend
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Set up the backend environment"""
    print("Setting up Emotion Analysis API Backend")
    print("=" * 50)
    
    # Check if we're in the backend directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found. Make sure you're in the backend directory.")
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not run_command("python3 -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    install_cmd = f"{pip_cmd} install -r requirements.txt"
    if not run_command(install_cmd, "Installing dependencies"):
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Backend setup completed successfully!")
    print("\nTo start the server:")
    print("1. Activate the virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the server:")
    print("   python start_server.py")
    print("\nOr simply run:")
    print("   python start_server.py")

if __name__ == "__main__":
    main() 