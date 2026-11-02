# Torvix Release Checklist

Use this checklist to ensure a smooth release process.

## Pre-Release Preparation

### Code Quality
- [ ] All tests pass locally (`make test`)
- [ ] Code is properly formatted (`make format`)
- [ ] Linting passes (`make lint`)
- [ ] No security vulnerabilities (`make check-deps`)
- [ ] Documentation is up to date

### Version Management
- [ ] Version number updated in `torvix/__init__.py`
- [ ] Version follows semantic versioning (MAJOR.MINOR.PATCH)
- [ ] CHANGELOG.md updated with new changes
- [ ] All changes committed and pushed to main branch

### Testing
- [ ] Manual testing of core functionality
- [ ] Test installation from source (`pip install -e .`)
- [ ] Test CLI commands work correctly
- [ ] Test AI provider integrations
- [ ] Cross-platform testing (Windows, macOS, Linux)

## Release Process

### 1. Pre-Release Testing
- [ ] Build package locally (`make build`)
- [ ] Test package installation (`pip install dist/torvix-*.whl`)
- [ ] Verify CLI works after installation
- [ ] Test on clean environment/container

### 2. TestPyPI Release
- [ ] Publish to TestPyPI (`make publish-test`)
- [ ] Install from TestPyPI and test:
  ```bash
  pip install --index-url https://test.pypi.org/simple/ torvix
  torvix --version
  torvix setup
  torvix "echo test"
  ```
- [ ] Verify all functionality works

### 3. Production Release
- [ ] Create Git tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Publish to PyPI (`make publish-prod`)
- [ ] Create GitHub release with release notes

### 4. Post-Release Verification
- [ ] Install from PyPI: `pip install torvix`
- [ ] Verify installation works
- [ ] Check PyPI page looks correct
- [ ] Test installation on different platforms
- [ ] Update documentation if needed

## GitHub Release

### Release Notes Template
```markdown
## Torvix v1.0.0

### 🎉 New Features
- Feature 1 description
- Feature 2 description

### 🐛 Bug Fixes
- Bug fix 1
- Bug fix 2

### 🔧 Improvements
- Improvement 1
- Improvement 2

### 📚 Documentation
- Documentation updates

### 🔒 Security
- Security improvements

## Installation

```bash
pip install torvix
```

## Quick Start

```bash
# Setup your AI provider
torvix setup

# Start using natural language commands
torvix "show git status"
```

## What's Next

- Upcoming features
- Roadmap items

---

**Full Changelog**: https://github.com/torvix/torvix/compare/v0.9.0...v1.0.0
```

## Post-Release Tasks

### Communication
- [ ] Announce on social media
- [ ] Update project website
- [ ] Notify users/community
- [ ] Submit to relevant newsletters/blogs

### Monitoring
- [ ] Monitor PyPI download statistics
- [ ] Watch for user issues/feedback
- [ ] Monitor GitHub issues and discussions
- [ ] Check for compatibility issues

### Documentation
- [ ] Update installation guides
- [ ] Update API documentation
- [ ] Create/update tutorials
- [ ] Update examples

## Rollback Plan

If issues are discovered after release:

1. **Minor Issues:**
   - [ ] Create hotfix branch
   - [ ] Fix issue
   - [ ] Release patch version

2. **Major Issues:**
   - [ ] Consider yanking release from PyPI
   - [ ] Communicate issue to users
   - [ ] Prepare fixed version ASAP

## Automation Checklist

### GitHub Actions
- [ ] CI pipeline passes on all platforms
- [ ] Security scans pass
- [ ] Build artifacts are created
- [ ] Publish workflow is configured

### PyPI Configuration
- [ ] PyPI account has necessary permissions
- [ ] API tokens are configured in GitHub secrets
- [ ] Package metadata is correct
- [ ] Dependencies are properly specified

## Version-Specific Notes

### v1.0.0 Release Notes
- [ ] First stable release
- [ ] All core features implemented
- [ ] Comprehensive testing completed
- [ ] Documentation complete
- [ ] Ready for production use

---

## Emergency Contacts

- **PyPI Issues:** support@pypi.org
- **GitHub Issues:** GitHub Support
- **Security Issues:** security@torvix.ai (if applicable)

## Useful Commands

```bash
# Check current version
grep "__version__" torvix/__init__.py

# Build and test locally
make all

# Publish to TestPyPI
make publish-test

# Publish to PyPI
make publish-prod

# Create and push tag
git tag v1.0.0 && git push origin v1.0.0
```
