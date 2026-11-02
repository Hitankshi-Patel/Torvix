#!/bin/bash

# Torvix One-Click Deployment Script
# This script handles the complete deployment process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists python; then
        print_error "Python is not installed or not in PATH"
        exit 1
    fi
    
    if ! command_exists git; then
        print_error "Git is not installed or not in PATH"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python --version 2>&1 | cut -d' ' -f2)
    print_status "Python version: $python_version"
    
    print_success "Prerequisites check passed"
}

# Clean previous builds
clean_build() {
    print_status "Cleaning previous builds..."
    rm -rf build/ dist/ *.egg-info/
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    print_success "Build artifacts cleaned"
}

# Install dependencies
install_dependencies() {
    print_status "Installing build dependencies..."
    pip install --upgrade pip
    pip install build twine
    pip install -e .[dev]
    print_success "Dependencies installed"
}

# Run tests
run_tests() {
    print_status "Running tests..."
    
    if command_exists pytest; then
        pytest tests/ -v
    else
        print_warning "pytest not found, skipping tests"
    fi
    
    print_success "Tests completed"
}

# Build package
build_package() {
    print_status "Building package..."
    python -m build
    
    print_status "Validating package..."
    twine check dist/*
    
    print_success "Package built and validated"
}

# Test installation
test_installation() {
    print_status "Testing package installation..."
    
    # Create temporary virtual environment
    python -m venv test_env
    source test_env/bin/activate 2>/dev/null || source test_env/Scripts/activate
    
    # Install the built package
    pip install dist/*.whl
    
    # Test basic functionality
    torvix --version
    
    # Cleanup
    deactivate
    rm -rf test_env
    
    print_success "Package installation test passed"
}

# Publish to TestPyPI
publish_test() {
    print_status "Publishing to TestPyPI..."
    
    if [ -z "$TEST_PYPI_TOKEN" ]; then
        print_warning "TEST_PYPI_TOKEN not set, using interactive authentication"
        twine upload --repository testpypi dist/*
    else
        twine upload --repository testpypi dist/* --username __token__ --password "$TEST_PYPI_TOKEN"
    fi
    
    print_success "Published to TestPyPI"
    print_status "Test installation with:"
    echo "pip install --index-url https://test.pypi.org/simple/ torvix"
}

# Publish to PyPI
publish_prod() {
    print_warning "You are about to publish to PyPI (production)"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" != "yes" ]; then
        print_status "Cancelled by user"
        exit 0
    fi
    
    print_status "Publishing to PyPI..."
    
    if [ -z "$PYPI_TOKEN" ]; then
        print_warning "PYPI_TOKEN not set, using interactive authentication"
        twine upload dist/*
    else
        twine upload dist/* --username __token__ --password "$PYPI_TOKEN"
    fi
    
    print_success "Published to PyPI!"
    print_status "Users can now install with: pip install torvix"
}

# Create GitHub release
create_github_release() {
    if ! command_exists gh; then
        print_warning "GitHub CLI (gh) not found, skipping GitHub release"
        return
    fi
    
    version=$(grep "__version__" torvix/__init__.py | cut -d'"' -f2)
    
    print_status "Creating GitHub release v$version..."
    
    gh release create "v$version" dist/* \
        --title "Release v$version" \
        --notes "See CHANGELOG.md for details" \
        --latest
    
    print_success "GitHub release created"
}

# Main deployment function
deploy() {
    local target=$1
    
    print_status "Starting Torvix deployment process..."
    print_status "Target: $target"
    
    check_prerequisites
    clean_build
    install_dependencies
    run_tests
    build_package
    test_installation
    
    case $target in
        "test")
            publish_test
            ;;
        "prod")
            publish_prod
            create_github_release
            ;;
        "build")
            print_success "Build completed successfully"
            print_status "Built files:"
            ls -la dist/
            ;;
        *)
            print_error "Unknown target: $target"
            print_status "Usage: $0 [build|test|prod]"
            exit 1
            ;;
    esac
    
    print_success "Deployment completed successfully! 🚀"
}

# Show help
show_help() {
    echo "Torvix Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  build    - Build package only"
    echo "  test     - Build and publish to TestPyPI"
    echo "  prod     - Build and publish to PyPI (production)"
    echo "  help     - Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  PYPI_TOKEN      - PyPI API token for production publishing"
    echo "  TEST_PYPI_TOKEN - TestPyPI API token for test publishing"
    echo ""
    echo "Examples:"
    echo "  $0 build    # Build package locally"
    echo "  $0 test     # Publish to TestPyPI"
    echo "  $0 prod     # Publish to PyPI"
}

# Main script logic
case "${1:-help}" in
    "build"|"test"|"prod")
        deploy "$1"
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
