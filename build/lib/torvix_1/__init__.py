"""
Torvix - AI-powered terminal assistant

A CLI tool that translates natural language into terminal commands
and executes them with user confirmation.
"""

__version__ = "1.0.0"
__author__ = "Torvix Team"
__email__ = "contact@torvix.ai"

from .cli import main

__all__ = ["main"]
