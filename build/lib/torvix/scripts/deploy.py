#!/usr/bin/env python3
"""
Deployment script for Torvix
Handles building, testing, and publishing the package
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, check=True, cwd=None):
    """Run a shell command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, cwd=cwd, 
                          capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result

def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    # Remove build directories
    dirs_to_remove = ['build', 'dist', '*.egg-info', '__pycache__', '.pytest_cache']
    for pattern in dirs_to_remove:
        run_command(f"rm -rf {pattern}", check=False)
    
    # Remove Python cache files
    run_command("find . -name '*.pyc' -delete", check=False)
    run_command("find . -name '__pycache__' -type d -exec rm -rf {} +", check=False)

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    
    # Install test dependencies
    run_command("pip install -e .[dev]")
    
    # Run linting
    print("Running flake8...")
    run_command("flake8 torvix tests --max-line-length=88")
    
    # Run formatting check
    print("Running black...")
    run_command("black --check torvix tests")
    
    # Run type checking
    print("Running mypy...")
    run_command("mypy torvix")
    
    # Run tests
    print("Running pytest...")
    run_command("pytest tests/ -v --cov=torvix")

def build_package():
    """Build the package."""
    print("📦 Building package...")
    
    # Install build dependencies
    run_command("pip install build twine")
    
    # Build the package
    run_command("python -m build")
    
    # Check the package
    run_command("twine check dist/*")

def publish_test():
    """Publish to TestPyPI."""
    print("🚀 Publishing to TestPyPI...")
    
    # Upload to TestPyPI
    run_command("twine upload --repository testpypi dist/*")
    
    print("✅ Published to TestPyPI!")
    print("Test installation with:")
    print("pip install --index-url https://test.pypi.org/simple/ torvix")

def publish_prod():
    """Publish to PyPI."""
    print("🚀 Publishing to PyPI...")
    
    # Confirm with user
    response = input("Are you sure you want to publish to PyPI? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Cancelled")
        return
    
    # Upload to PyPI
    run_command("twine upload dist/*")
    
    print("✅ Published to PyPI!")
    print("Install with: pip install torvix")

def check_version():
    """Check and display version information."""
    print("📋 Version Information:")
    
    # Get version from __init__.py
    init_file = Path("torvix/__init__.py")
    if init_file.exists():
        with open(init_file) as f:
            for line in f:
                if line.startswith("__version__"):
                    version = line.split("=")[1].strip().strip('"\'')
                    print(f"Package version: {version}")
                    break
    
    # Check if tag exists
    result = run_command(f"git tag -l v{version}", check=False)
    if result.stdout.strip():
        print(f"Git tag v{version} exists")
    else:
        print(f"Git tag v{version} does not exist")

def main():
    parser = argparse.ArgumentParser(description="Torvix deployment script")
    parser.add_argument("action", choices=[
        "clean", "test", "build", "publish-test", "publish-prod", 
        "version", "all"
    ], help="Action to perform")
    
    args = parser.parse_args()
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    try:
        if args.action == "clean":
            clean_build()
        elif args.action == "test":
            run_tests()
        elif args.action == "build":
            build_package()
        elif args.action == "publish-test":
            publish_test()
        elif args.action == "publish-prod":
            publish_prod()
        elif args.action == "version":
            check_version()
        elif args.action == "all":
            clean_build()
            run_tests()
            build_package()
            print("✅ All steps completed successfully!")
            print("Next steps:")
            print("- Review the built package in dist/")
            print("- Test with: python scripts/deploy.py publish-test")
            print("- Publish with: python scripts/deploy.py publish-prod")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
