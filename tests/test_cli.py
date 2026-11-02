"""
Tests for Torvix CLI functionality
"""

import pytest
from click.testing import CliRunner
from torvix.cli import cli
from torvix import __version__

def test_version():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert __version__ in result.output

def test_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Torvix' in result.output
    assert 'Available Commands' in result.output

def test_main_help():
    """Test main command without arguments shows help."""
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert 'Torvix' in result.output

def test_setup_command():
    """Test setup command exists."""
    runner = CliRunner()
    result = runner.invoke(cli, ['setup', '--help'])
    assert result.exit_code == 0
    assert 'setup' in result.output.lower()

def test_config_command():
    """Test config command exists."""
    runner = CliRunner()
    result = runner.invoke(cli, ['config', '--help'])
    assert result.exit_code == 0
    assert 'config' in result.output.lower()

def test_reset_command():
    """Test reset command exists."""
    runner = CliRunner()
    result = runner.invoke(cli, ['reset', '--help'])
    assert result.exit_code == 0
    assert 'reset' in result.output.lower()

if __name__ == '__main__':
    pytest.main([__file__])
