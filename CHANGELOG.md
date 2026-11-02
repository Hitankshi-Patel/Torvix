# Changelog

All notable changes to Torvix will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Torvix AI terminal assistant
- Support for multiple AI providers (ChatGPT, Gemini, Claude, DeepSeek, Perplexity, Grok, Torvix Cloud)
- Secure API key storage using system keyring
- Natural language to terminal command translation
- Interactive command execution with user confirmation
- Dangerous command detection and warnings
- Rich terminal UI with syntax highlighting
- Configuration management system
- Command timeout protection (60 seconds)
- Dry run mode for command preview

### Features
- `torvix` - Display help and available commands
- `torvix setup` - Interactive AI provider configuration
- `torvix config` - View and edit configurations
- `torvix "prompt"` - Natural language command execution
- `torvix reset` - Clear configurations with confirmation
- `torvix --version` - Version information
- `torvix --help` - Help documentation

### Security
- Secure credential storage using system keyring
- Command validation and dangerous pattern detection
- User confirmation required for all command execution
- Timeout protection for long-running commands

### Documentation
- Comprehensive README with usage examples
- API documentation for all supported providers
- Contributing guidelines
- MIT License
