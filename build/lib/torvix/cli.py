#!/usr/bin/env python3
"""
Main CLI module for Torvix - AI-powered terminal assistant
"""

import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .config import ConfigManager
from .ai_providers import AIProviderManager
from .executor import CommandExecutor

console = Console()

TORVIX_DEFINITION = """
Torvix is an AI-powered terminal assistant that translates natural language 
into terminal commands and executes them with your confirmation. It supports 
multiple AI providers and helps automate common development tasks.
"""

AVAILABLE_COMMANDS = {
    "torvix": "Display this help and available commands",
    "torvix setup": "Configure AI providers and API keys",
    "torvix config": "View or edit existing configuration",
    "torvix \"prompt\"": "Send a natural language prompt to AI and execute commands",
    "torvix query \"prompt\"": "Send prompt to AI and only display the response",
    "torvix explain [\"error_message\"]": "Explain the last or provided error",
    "torvix reset": "Clear all stored configurations",
    "torvix reset [model]": "Clear configuration for specific model (case-insensitive)",
    "torvix switch [provider]": "Switch default AI provider (case-insensitive)",
    "torvix --version/-v": "Display version information",
    "torvix --help/-h": "Display this help message"
}

def display_help():
    """Display the main help message with Torvix definition and commands."""
    console.print(Panel(
        Text(TORVIX_DEFINITION.strip(), style="cyan"),
        title="[bold blue]Torvix AI Terminal Assistant[/bold blue]",
        border_style="blue"
    ))
    
    console.print("\n[bold green]Available Commands:[/bold green]")
    for cmd, desc in AVAILABLE_COMMANDS.items():
        console.print(f"  [yellow]{cmd:<35}[/yellow] {desc}")
    console.print()

@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version information')
@click.option('--help', '-h', is_flag=True, help='Show this help message')
@click.pass_context
def cli(ctx, version, help):
    """Torvix - AI-powered terminal assistant"""
    if version:
        console.print(f"[bold blue]Torvix[/bold blue] v{__version__}")
        return
    
    if help or ctx.invoked_subcommand is None:
        display_help()
        return

@cli.command()
@click.option('--provider', '-p', help='Specific provider to configure')
def setup(provider):
    """Interactive setup to configure AI providers and API keys."""
    config_manager = ConfigManager()
    config_manager.interactive_setup(provider)

@cli.command()
@click.option('--list', '-l', is_flag=True, help='List current configuration')
@click.option('--edit', '-e', help='Edit configuration for specific provider')
def config(list, edit):
    """View or edit existing configuration."""
    config_manager = ConfigManager()
    
    if list:
        config_manager.list_config()
    elif edit:
        config_manager.edit_config(edit)
    else:
        config_manager.show_config()

@cli.command()
@click.argument('model', required=False)
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation prompt')
def reset(model, confirm):
    """Clear stored API keys and configurations."""
    config_manager = ConfigManager()
    config_manager.reset_config(model, confirm)

@cli.command()
@click.argument('provider', required=True)
def switch(provider):
    """Switch default AI provider to a configured provider."""
    config_manager = ConfigManager()
    config_manager.switch_default_provider(provider)

@cli.command()
@click.argument('message', required=False)
@click.option('--provider', '-p', help='Specific AI provider to use')
def explain(message, provider):
    """Explain last error (from Torvix session) or provided error text."""
    try:
        config_manager = ConfigManager()
        ai_manager = AIProviderManager(config_manager)
        
        if not message:
            last_error_text = CommandExecutor.read_last_error()
            if not last_error_text:
                console.print("[yellow]No recent error found. Provide an error message, e.g. torvix explain \"<error>\"[/yellow]")
                return
            message = last_error_text
        
        console.print(f"[blue]Asking AI to explain the error...[/blue]")
        prompt = f"Explain this error and provide likely fixes with commands (use RUN: lines where relevant):\n\n{message}"
        response = ai_manager.query(prompt, provider)
        if not response:
            console.print("[red]No response from AI provider[/red]")
            return
        console.print(Panel(response, title="[bold green]AI Explanation[/bold green]"))
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

@cli.command()
@click.argument('prompt', required=True)
@click.option('--provider', '-p', help='Specific AI provider to use')
@click.option('--dry-run', '-d', is_flag=True, help='Show commands without executing')
def query(prompt, provider, dry_run):
    """Ask the AI and only display the response (no execution)."""
    try:
        config_manager = ConfigManager()
        ai_manager = AIProviderManager(config_manager)
        
        # Get AI response
        console.print(f"[blue]Sending prompt to AI...[/blue]")
        response = ai_manager.query(prompt, provider)
        
        if not response:
            console.print("[red]No response from AI provider[/red]")
            return
        console.print(Panel(response, title="[bold green]AI Response[/bold green]"))
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    try:
        # Handle direct prompt without subcommand
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            # Check if it's a known subcommand
            known_commands = ['setup', 'config', 'reset', 'query', 'switch', 'explain']
            arg = sys.argv[1]

            # If it's not a known command, treat it as a direct prompt
            if arg not in known_commands:
                # Direct prompt: torvix "prompt text" (quotes are stripped by shell)
                prompt = arg

                # Create a mock context and invoke prompt execution directly
                config_manager = ConfigManager()
                ai_manager = AIProviderManager(config_manager)
                executor = CommandExecutor()

                console.print(f"[blue]Sending prompt to AI...[/blue]")
                response = ai_manager.query(prompt)

                if not response:
                    console.print("[red]No response from AI provider[/red]")
                    return

                console.print(Panel(response, title="[bold green]AI Response[/bold green]"))

                # Parse and execute commands
                commands = executor.parse_commands(response)
                if commands:
                    executor.execute_commands(commands, False)
                else:
                    console.print("[yellow]No executable commands found in response[/yellow]")
                return

        # Regular CLI command processing
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()
