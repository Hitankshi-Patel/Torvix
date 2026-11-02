"""
Logging configuration for Torvix
"""

import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

console = Console()

class TorvixLogger:
    """Custom logger for Torvix with rich formatting."""
    
    def __init__(self, name: str = "torvix", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup logging handlers."""
        # Rich console handler for terminal output
        console_handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            rich_tracebacks=True
        )
        console_handler.setLevel(logging.INFO)
        
        # File handler for debug logs
        log_dir = Path.home() / '.torvix' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / 'torvix.log')
        file_handler.setLevel(logging.DEBUG)
        
        # Formatters
        console_format = logging.Formatter('%(message)s')
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message."""
        self.logger.critical(message)

# Global logger instance
logger = TorvixLogger()

def log_api_request(provider: str, prompt: str, success: bool):
    """Log API request details."""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"API Request to {provider}: {status}")
    logger.debug(f"Prompt: {prompt[:100]}...")

def log_command_execution(command: str, success: bool, output: str = ""):
    """Log command execution details."""
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Command execution: {status} - {command}")
    if output:
        logger.debug(f"Output: {output[:200]}...")

def log_error(error: Exception, context: str = ""):
    """Log error with context."""
    error_msg = f"Error in {context}: {str(error)}" if context else str(error)
    logger.error(error_msg)
    logger.debug(f"Exception details: {type(error).__name__}: {error}", exc_info=True)
