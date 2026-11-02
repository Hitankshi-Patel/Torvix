# Contributing to Torvix

Thank you for your interest in contributing to Torvix! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A text editor or IDE

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/torvix.git
   cd torvix
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```

4. **Run tests to ensure everything works**:
   ```bash
   pytest tests/
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Use meaningful variable and function names

### Testing

- Write tests for new features and bug fixes
- Ensure all tests pass before submitting a PR
- Aim for good test coverage
- Use pytest for testing

### Commit Messages

Use clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests when applicable

Example:
```
Add support for custom AI models

- Allow users to configure custom OpenAI-compatible endpoints
- Add validation for custom model configurations
- Update documentation with custom model examples

Fixes #123
```

## Types of Contributions

### Bug Reports

When filing a bug report, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Torvix version)
- Relevant logs or error messages

### Feature Requests

For feature requests, please provide:
- Clear description of the proposed feature
- Use case and motivation
- Possible implementation approach
- Any relevant examples or mockups

### Code Contributions

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**:
   ```bash
   pytest tests/
   python demo.py  # Test the demo
   ```

4. **Commit and push**:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Use a clear title and description
   - Reference any related issues
   - Include screenshots if applicable

## Areas for Contribution

### High Priority
- Additional AI provider integrations
- Improved command parsing and validation
- Enhanced security features
- Performance optimizations
- Better error handling and user feedback

### Medium Priority
- Plugin system for custom commands
- Configuration file import/export
- Command history and favorites
- Shell integration improvements
- Documentation improvements

### Low Priority
- GUI interface
- Web dashboard
- Advanced scripting capabilities
- Integration with other tools

## AI Provider Integration

When adding support for new AI providers:

1. Create a new provider class inheriting from `AIProvider`
2. Implement the `query` method
3. Add the provider to `SUPPORTED_PROVIDERS` in `config.py`
4. Add the provider class to `PROVIDER_CLASSES` in `ai_providers.py`
5. Write tests for the new provider
6. Update documentation

## Security Considerations

- Never commit API keys or sensitive information
- Use secure methods for credential storage
- Validate all user inputs
- Be cautious with command execution
- Follow security best practices

## Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Keep CHANGELOG.md updated

## Getting Help

- Check existing issues and discussions
- Ask questions in GitHub Discussions
- Join our community chat (link in README)
- Contact maintainers directly for sensitive issues

## Code of Conduct

Please be respectful and inclusive in all interactions. We follow the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## License

By contributing to Torvix, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Torvix! 🚀
