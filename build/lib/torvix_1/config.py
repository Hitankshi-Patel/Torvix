"""
Configuration management for Torvix AI providers and settings
"""

import os
import json
import keyring
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

console = Console()

class ConfigManager:
    """Manages configuration and secure storage of API keys for AI providers."""
    
    SUPPORTED_PROVIDERS = {
        'chatgpt': {
            'name': 'ChatGPT (OpenAI)',
            'api_key_name': 'OpenAI API Key',
            'base_url': 'https://api.openai.com/v1',
            'model': 'gpt-4'
        },
        'gemini': {
            'name': 'Google Gemini',
            'api_key_name': 'Google AI API Key',
            'base_url': 'https://generativelanguage.googleapis.com/v1beta',
            'model': 'gemini-2.0-flash'
        },
        'deepseek': {
            'name': 'DeepSeek',
            'api_key_name': 'DeepSeek API Key',
            'base_url': 'https://api.deepseek.com/v1',
            'model': 'deepseek-chat'
        },
        'perplexity': {
            'name': 'Perplexity',
            'api_key_name': 'Perplexity API Key',
            'base_url': 'https://api.perplexity.ai',
            'model': 'llama-3.1-sonar-small-128k-online'
        },
        'claude': {
            'name': 'Anthropic Claude',
            'api_key_name': 'Anthropic API Key',
            'base_url': 'https://api.anthropic.com/v1',
            'model': 'claude-3-sonnet-20240229'
        },
        'grok': {
            'name': 'Grok (X.AI)',
            'api_key_name': 'Grok API Key',
            'base_url': 'https://api.x.ai/v1',
            'model': 'grok-beta'
        },
        'torvix': {
            'name': 'Torvix Cloud',
            'api_key_name': 'Torvix API Key',
            'base_url': 'https://api.torvix.ai/v1',
            'model': 'torvix-assistant'
        }
    }
    
    def __init__(self):
        self.config_dir = Path.home() / '.torvix'
        self.config_file = self.config_dir / 'config.json'
        self.keyring_service = 'torvix-ai-assistant'
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if not self.config_file.exists():
            return {'default_provider': None, 'providers': {}}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {'default_provider': None, 'providers': {}}
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            console.print(f"[red]Error saving configuration: {e}[/red]")
    
    def _store_api_key(self, provider: str, api_key: str):
        """Securely store API key using keyring."""
        try:
            keyring.set_password(self.keyring_service, provider, api_key)
        except Exception as e:
            console.print(f"[red]Error storing API key: {e}[/red]")
            raise
    
    def _get_api_key(self, provider: str) -> Optional[str]:
        """Retrieve API key from secure storage."""
        try:
            return keyring.get_password(self.keyring_service, provider)
        except Exception:
            return None
    
    def _delete_api_key(self, provider: str):
        """Delete API key from secure storage."""
        try:
            keyring.delete_password(self.keyring_service, provider)
        except Exception:
            pass  # Key might not exist
    
    def interactive_setup(self, specific_provider: Optional[str] = None):
        """Interactive setup for configuring AI providers."""
        console.print(Panel(
            "[bold blue]Torvix AI Provider Setup[/bold blue]\n"
            "Configure your AI providers to start using Torvix.",
            border_style="blue"
        ))
        
        config = self._load_config()
        
        if specific_provider:
            if specific_provider not in self.SUPPORTED_PROVIDERS:
                console.print(f"[red]Unknown provider: {specific_provider}[/red]")
                return
            providers_to_setup = [specific_provider]
        else:
            # Show available providers
            table = Table(title="Available AI Providers")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            
            for i, (provider_id, provider_info) in enumerate(self.SUPPORTED_PROVIDERS.items(), 1):
                status = "✓ Configured" if self._get_api_key(provider_id) else "Not configured"
                table.add_row(str(i), provider_info['name'], status)
            
            console.print(table)
            
            # Get user selection
            selection = Prompt.ask(
                "\nSelect providers to configure (comma-separated numbers or 'all')",
                default="1"
            )
            
            if selection.lower() == 'all':
                providers_to_setup = list(self.SUPPORTED_PROVIDERS.keys())
            else:
                try:
                    indices = [int(x.strip()) for x in selection.split(',')]
                    provider_list = list(self.SUPPORTED_PROVIDERS.keys())
                    providers_to_setup = [provider_list[i-1] for i in indices if 1 <= i <= len(provider_list)]
                except (ValueError, IndexError):
                    console.print("[red]Invalid selection[/red]")
                    return
        
        # Configure selected providers
        for provider_id in providers_to_setup:
            self._setup_provider(provider_id, config)
        
        # Set default provider if none exists
        if not config.get('default_provider') and providers_to_setup:
            config['default_provider'] = providers_to_setup[0]
            console.print(f"[green]Set {self.SUPPORTED_PROVIDERS[providers_to_setup[0]]['name']} as default provider[/green]")
        
        self._save_config(config)
        console.print("\n[bold green]Setup completed successfully![/bold green]")
    
    def _setup_provider(self, provider_id: str, config: Dict[str, Any]):
        """Setup a specific provider."""
        provider_info = self.SUPPORTED_PROVIDERS[provider_id]
        
        console.print(f"\n[bold cyan]Configuring {provider_info['name']}[/bold cyan]")
        
        # Get API key
        current_key = self._get_api_key(provider_id)
        if current_key:
            if not Confirm.ask(f"API key already exists for {provider_info['name']}. Replace it?"):
                return
        
        api_key = Prompt.ask(
            f"Enter your {provider_info['api_key_name']}",
            password=True
        )
        
        if not api_key.strip():
            console.print("[yellow]Skipping - no API key provided[/yellow]")
            return
        
        # Store API key securely
        self._store_api_key(provider_id, api_key.strip())
        
        # Update config
        if 'providers' not in config:
            config['providers'] = {}
        
        config['providers'][provider_id] = {
            'name': provider_info['name'],
            'model': provider_info['model'],
            'base_url': provider_info['base_url'],
            'enabled': True
        }
        
        console.print(f"[green]✓ {provider_info['name']} configured successfully[/green]")
    
    def list_config(self):
        """List current configuration."""
        config = self._load_config()
        
        if not config.get('providers'):
            console.print("[yellow]No providers configured. Run 'torvix setup' to get started.[/yellow]")
            return
        
        table = Table(title="Torvix Configuration")
        table.add_column("Provider", style="cyan")
        table.add_column("Model", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Default", style="magenta")
        
        for provider_id, provider_config in config['providers'].items():
            api_key_exists = bool(self._get_api_key(provider_id))
            status = "✓ Ready" if api_key_exists else "✗ No API Key"
            is_default = "✓" if config.get('default_provider') == provider_id else ""
            
            table.add_row(
                provider_config['name'],
                provider_config['model'],
                status,
                is_default
            )
        
        console.print(table)
    
    def show_config(self):
        """Show detailed configuration."""
        self.list_config()
    
    def edit_config(self, provider: str):
        """Edit configuration for a specific provider."""
        if provider not in self.SUPPORTED_PROVIDERS:
            console.print(f"[red]Unknown provider: {provider}[/red]")
            return
        
        config = self._load_config()
        self._setup_provider(provider, config)
        self._save_config(config)
    
    def reset_config(self, model: Optional[str] = None, confirm: bool = False):
        """Reset configuration for specific model or all models."""
        if model:
            if model not in self.SUPPORTED_PROVIDERS:
                console.print(f"[red]Unknown provider: {model}[/red]")
                return
            
            if not confirm and not Confirm.ask(f"Reset configuration for {self.SUPPORTED_PROVIDERS[model]['name']}?"):
                return
            
            self._delete_api_key(model)
            config = self._load_config()
            if 'providers' in config and model in config['providers']:
                del config['providers'][model]
            
            if config.get('default_provider') == model:
                config['default_provider'] = None
            
            self._save_config(config)
            console.print(f"[green]✓ Reset configuration for {self.SUPPORTED_PROVIDERS[model]['name']}[/green]")
        else:
            if not confirm and not Confirm.ask("Reset ALL configurations? This cannot be undone."):
                return
            
            # Delete all API keys
            for provider_id in self.SUPPORTED_PROVIDERS.keys():
                self._delete_api_key(provider_id)
            
            # Reset config file
            self._save_config({'default_provider': None, 'providers': {}})
            console.print("[green]✓ All configurations reset[/green]")
    
    def get_provider_config(self, provider_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific provider or the default provider."""
        config = self._load_config()
        
        if not provider_id:
            provider_id = config.get('default_provider')
        
        if not provider_id or provider_id not in config.get('providers', {}):
            return None
        
        provider_config = config['providers'][provider_id].copy()
        provider_config['api_key'] = self._get_api_key(provider_id)
        provider_config['provider_id'] = provider_id
        
        return provider_config if provider_config['api_key'] else None
