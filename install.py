#!/usr/bin/env python3
"""
Installation script for Torvix
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"[SUCCESS] {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"[SUCCESS] Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_torvix():
    """Install latest Torvix (prefers PyPI; falls back to local source)."""
    print("Installing Torvix AI Terminal Assistant")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # 1) Try latest from PyPI
    if run_command("pip install --upgrade --no-cache-dir torvix", "Installing Torvix from PyPI (latest)"):
        # Verify installation
        if not run_command("torvix --version", "Verifying installation"):
            return False
        print("\n[SUCCESS] Torvix installed from PyPI")
        print("\nNext steps:")
        print("1. Run 'torvix setup' to configure your AI providers")
        print("2. Try 'torvix \"list files in current directory\"' to test it out")
        print("3. Use 'torvix switch gemini' to change default provider")
        print("\nFor help, run 'torvix --help'")
        return True
    
    # 2) Fallback to local source install (wheel-like)
    script_dir = Path(__file__).parent
    if run_command(f"pip install --force-reinstall --no-deps --upgrade {script_dir}", "Installing Torvix from local source"):
        if not run_command("torvix --version", "Verifying installation"):
            return False
        print("\n[SUCCESS] Torvix installed from local source")
        print("\nNext steps:")
        print("1. Run 'torvix setup' to configure your AI providers")
        print("2. Try 'torvix \"list files in current directory\"' to test it out")
        print("3. Use 'torvix switch gemini' to change default provider")
        print("\nFor help, run 'torvix --help'")
        return True
    
    # 3) Last resort: editable install
    if run_command(f"pip install -e {script_dir}", "Installing Torvix from source (editable)"):
        if not run_command("torvix --version", "Verifying installation"):
            return False
        print("\n[SUCCESS] Torvix installed in editable mode")
        print("\nNext steps:")
        print("1. Run 'torvix setup' to configure your AI providers")
        print("2. Try 'torvix \"list files in current directory\"' to test it out")
        print("3. Use 'torvix switch gemini' to change default provider")
        print("\nFor help, run 'torvix --help'")
        return True
    
    return False

if __name__ == "__main__":
    success = install_torvix()
    sys.exit(0 if success else 1)
