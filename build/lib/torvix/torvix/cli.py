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
    "torvix \"prompt\"": "Send a natural language prompt to AI",
    "torvix reset": "Clear all stored configurations",
    "torvix reset [model]": "Clear configuration for specific model",
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
        console.print(f"  [yellow]{cmd:<25}[/yellow] {desc}")
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
@click.argument('prompt', required=True)
@click.option('--provider', '-p', help='Specific AI provider to use')
@click.option('--dry-run', '-d', is_flag=True, help='Show commands without executing')
def query(prompt, provider, dry_run):
    """Send a natural language prompt to AI and execute suggested commands."""
    try:
        config_manager = ConfigManager()
        ai_manager = AIProviderManager(config_manager)
        executor = CommandExecutor()
        
        # Get AI response
        console.print(f"[blue]Sending prompt to AI...[/blue]")
        response = ai_manager.query(prompt, provider)
        
        if not response:
            console.print("[red]No response from AI provider[/red]")
            return
        
        console.print(Panel(response, title="[bold green]AI Response[/bold green]"))
        
        # Parse and execute commands
        commands = executor.parse_commands(response)
        if commands:
            executor.execute_commands(commands, dry_run)
        else:
            console.print("[yellow]No executable commands found in response[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        sys.exit(1)

def main():
    """Main entry point for the CLI."""
    try:
        # Handle direct prompt without subcommand
        if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
            # Check if it's a known subcommand
            known_commands = ['setup', 'config', 'reset', 'query']
            arg = sys.argv[1]

            # If it's not a known command, treat it as a direct prompt
            if arg not in known_commands:
                # Direct prompt: torvix "prompt text" (quotes are stripped by shell)
                prompt = arg

                # Create a mock context and invoke query directly
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
