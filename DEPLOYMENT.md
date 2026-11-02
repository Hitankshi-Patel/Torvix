# Torvix Deployment Guide

This guide explains how to deploy Torvix to production and make it available for users to install.

## Prerequisites

1. **Python 3.8+** installed
2. **Git** for version control
3. **PyPI account** for package publishing
4. **GitHub account** for repository hosting
5. **Twine** for uploading packages

## Deployment Methods

### Method 1: PyPI Distribution (Recommended)

This is the primary method for distributing Torvix to end users.

#### Step 1: Prepare the Package

```bash
# Clean previous builds
python scripts/deploy.py clean

# Run tests
python scripts/deploy.py test

# Build the package
python scripts/deploy.py build
```

#### Step 2: Test on TestPyPI

```bash
# Upload to TestPyPI first
python scripts/deploy.py publish-test

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ torvix

# Test the installation
torvix --version
torvix "echo hello world"
```

#### Step 3: Publish to PyPI

```bash
# Publish to production PyPI
python scripts/deploy.py publish-prod
```

#### Step 4: Verify Installation

```bash
# Install from PyPI
pip install torvix

# Verify it works
torvix --version
```

### Method 2: GitHub Releases

#### Automated via GitHub Actions

1. **Create a Release on GitHub:**
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Tag version: `v1.0.0`
   - Release title: `Release v1.0.0`
   - Describe the changes
   - Click "Publish release"

2. **GitHub Actions will automatically:**
   - Run tests
   - Build the package
   - Publish to PyPI
   - Create release artifacts

#### Manual Release

```bash
# Create and push a tag
git tag v1.0.0
git push origin v1.0.0

# Build the package
python -m build

# Upload to GitHub releases manually
# (Use GitHub web interface or gh CLI)
```

### Method 3: Direct Installation from GitHub

Users can install directly from GitHub:

```bash
# Install latest version
pip install git+https://github.com/yourusername/torvix.git

# Install specific version
pip install git+https://github.com/yourusername/torvix.git@v1.0.0
```

## Distribution Channels

### 1. PyPI (Python Package Index)

**Advantages:**
- Standard Python package distribution
- Easy installation with `pip install torvix`
- Automatic dependency management
- Version management

**Setup:**
1. Create PyPI account at https://pypi.org
2. Create API token in account settings
3. Configure in GitHub secrets as `PYPI_API_TOKEN`

### 2. Conda-Forge (Future)

For Conda users, you can submit to conda-forge:

```bash
# Future: conda install torvix
```

### 3. Package Managers

#### Homebrew (macOS/Linux)
Create a Homebrew formula:

```ruby
# Formula/torvix.rb
class Torvix < Formula
  desc "AI-powered terminal assistant"
  homepage "https://github.com/yourusername/torvix"
  url "https://github.com/yourusername/torvix/archive/v1.0.0.tar.gz"
  sha256 "..."
  
  depends_on "python@3.11"
  
  def install
    virtualenv_install_with_resources
  end
end
```

#### Chocolatey (Windows)
Create a Chocolatey package:

```xml
<!-- torvix.nuspec -->
<package>
  <metadata>
    <id>torvix</id>
    <version>1.0.0</version>
    <title>Torvix</title>
    <authors>Torvix Team</authors>
    <description>AI-powered terminal assistant</description>
  </metadata>
</package>
```

## Automated Deployment Pipeline

### GitHub Actions Workflow

The repository includes automated workflows:

1. **CI Pipeline** (`.github/workflows/ci.yml`):
   - Runs on every push/PR
   - Tests on multiple Python versions
   - Tests on multiple operating systems
   - Runs security checks
   - Builds package

2. **Publish Pipeline** (`.github/workflows/publish.yml`):
   - Triggers on GitHub releases
   - Publishes to PyPI automatically
   - Creates GitHub release artifacts

### Setting Up Secrets

Configure these secrets in your GitHub repository:

```bash
# PyPI API Token
PYPI_API_TOKEN=pypi-...

# TestPyPI API Token (optional)
TEST_PYPI_API_TOKEN=pypi-...
```

## Version Management

### Semantic Versioning

Follow semantic versioning (semver):
- `1.0.0` - Major release
- `1.1.0` - Minor release (new features)
- `1.0.1` - Patch release (bug fixes)

### Release Process

1. **Update version** in `torvix/__init__.py`
2. **Update CHANGELOG.md** with changes
3. **Commit changes**
4. **Create and push tag**
5. **Create GitHub release**
6. **Automated pipeline handles the rest**

## Monitoring and Analytics

### PyPI Statistics

Monitor package downloads:
- https://pypistats.org/packages/torvix
- https://pepy.tech/project/torvix

### GitHub Analytics

Track repository metrics:
- Stars, forks, issues
- Download statistics
- User engagement

## Troubleshooting

### Common Issues

1. **Build Failures:**
   ```bash
   # Check dependencies
   pip install build twine
   
   # Verify package structure
   python -m build --check
   ```

2. **Upload Failures:**
   ```bash
   # Check credentials
   twine check dist/*
   
   # Test upload to TestPyPI first
   twine upload --repository testpypi dist/*
   ```

3. **Version Conflicts:**
   ```bash
   # Ensure version is unique
   pip search torvix
   
   # Update version in __init__.py
   ```

## Security Considerations

1. **API Keys:** Store securely in GitHub secrets
2. **Dependencies:** Regularly update and audit
3. **Code Signing:** Consider signing releases
4. **Vulnerability Scanning:** Use automated tools

## Post-Deployment

### User Support

1. **Documentation:** Keep README and docs updated
2. **Issue Tracking:** Monitor GitHub issues
3. **Community:** Engage with users
4. **Updates:** Regular maintenance releases

### Marketing

1. **Announce on social media**
2. **Submit to Python newsletters**
3. **Create blog posts/tutorials**
4. **Engage with developer communities**
