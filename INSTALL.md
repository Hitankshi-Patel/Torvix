# Torvix Installation Guide

This guide provides multiple ways to install Torvix on your system.

## Quick Installation (Recommended)

### Method 1: Install from PyPI (pip)

```bash
# Install Torvix
pip install torvix

# Verify installation
torvix --version
```

### Method 2: Install with AI Provider Support

```bash
# Install with all AI provider dependencies
pip install torvix[ai-providers]

# Or install specific providers
pip install torvix openai anthropic google-generativeai
```

## Platform-Specific Installation

### Windows

#### Using pip (Recommended)
```cmd
# Install Python 3.8+ from python.org if not already installed
pip install torvix

# Add to PATH if needed (usually automatic)
# Verify installation
torvix --version
```

#### Using Windows Package Manager (winget)
```cmd
# Coming soon - will be available as:
# winget install torvix
```

### macOS

#### Using pip
```bash
# Install using system Python or Homebrew Python
pip3 install torvix

# Verify installation
torvix --version
```

#### Using Homebrew (Coming Soon)
```bash
# Will be available as:
# brew install torvix
```

### Linux

#### Ubuntu/Debian
```bash
# Install pip if not available
sudo apt update
sudo apt install python3-pip

# Install Torvix
pip3 install torvix

# Add to PATH if needed
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
torvix --version
```

#### CentOS/RHEL/Fedora
```bash
# Install pip if not available
sudo dnf install python3-pip  # Fedora
# or
sudo yum install python3-pip  # CentOS/RHEL

# Install Torvix
pip3 install torvix

# Verify installation
torvix --version
```

#### Arch Linux
```bash
# Install from AUR (coming soon)
# yay -S torvix

# Or use pip
pip install torvix
```

## Development Installation

### Install from Source

```bash
# Clone the repository
git clone https://github.com/torvix/torvix.git
cd torvix

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e .[all]
```

### Install from GitHub

```bash
# Install latest development version
pip install git+https://github.com/torvix/torvix.git

# Install specific branch or tag
pip install git+https://github.com/torvix/torvix.git@main
```

## Post-Installation Setup

After installation, you need to configure at least one AI provider:

```bash
# Run interactive setup
torvix setup

# Or configure a specific provider
torvix setup -p chatgpt
```

## Verification

Test your installation:

```bash
# Check version
torvix --version

# View help
torvix --help

# Test with a simple command
torvix "show current directory"
```

## Troubleshooting

### Common Issues

#### Command not found
```bash
# Check if torvix is in PATH
which torvix

# If not found, add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

#### Permission errors on Linux/macOS
```bash
# Install for user only
pip install --user torvix
```

#### Python version issues
```bash
# Check Python version (requires 3.8+)
python --version

# Use specific Python version
python3.9 -m pip install torvix
```

### Getting Help

- **Documentation**: https://torvix.readthedocs.io/
- **Issues**: https://github.com/torvix/torvix/issues
- **Discussions**: https://github.com/torvix/torvix/discussions

## Uninstallation

```bash
# Remove Torvix
pip uninstall torvix

# Remove configuration (optional)
rm -rf ~/.torvix
```
