#!/usr/bin/env python3
"""
Demo script for Torvix AI Terminal Assistant
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm

console = Console()

def print_banner():
    """Print Torvix banner."""
    banner = Text("TORVIX", style="bold blue")
    subtitle = Text("AI-Powered Terminal Assistant", style="cyan")
    
    console.print(Panel(
        f"{banner}\n{subtitle}",
        border_style="blue",
        padding=(1, 2)
    ))

def demo_commands():
    """Show demo of common Torvix commands."""
    examples = [
        {
            "prompt": "push this code to github",
            "description": "Git operations made simple",
            "commands": [
                "git add .",
                "git commit -m 'Update code'",
                "git push origin main"
            ]
        },
        {
            "prompt": "find all python files modified today",
            "description": "File system operations",
            "commands": [
                "find . -name '*.py' -mtime -1"
            ]
        },
        {
            "prompt": "start a development server on port 3000",
            "description": "Development workflow automation",
            "commands": [
                "npm install",
                "npm run dev -- --port 3000"
            ]
        },
        {
            "prompt": "show disk usage for all directories",
            "description": "System administration tasks",
            "commands": [
                "du -sh */ | sort -hr"
            ]
        }
    ]
    
    console.print("\n[bold green]Example Commands:[/bold green]\n")
    
    for i, example in enumerate(examples, 1):
        console.print(f"[bold cyan]{i}. {example['description']}[/bold cyan]")
        console.print(f"   [yellow]torvix \"{example['prompt']}\"[/yellow]")
        console.print("   [dim]AI would suggest:[/dim]")
        
        for cmd in example['commands']:
            console.print(f"   [green]RUN: {cmd}[/green]")
        console.print()

def installation_guide():
    """Show installation guide."""
    console.print(Panel(
        "[bold blue]Installation Guide[/bold blue]\n\n"
        "[yellow]1. Install Torvix:[/yellow]\n"
        "   pip install torvix\n\n"
        "[yellow]2. Setup AI Provider:[/yellow]\n"
        "   torvix setup\n\n"
        "[yellow]3. Start using natural language:[/yellow]\n"
        "   torvix \"your command here\"\n\n"
        "[dim]Supported providers: ChatGPT, Gemini, Claude, DeepSeek, Perplexity, Grok[/dim]",
        border_style="green"
    ))

def safety_features():
    """Show safety features."""
    console.print(Panel(
        "[bold red]Safety Features[/bold red]\n\n"
        "🛡️  [yellow]Command Confirmation[/yellow] - Every command requires approval\n"
        "⚠️  [yellow]Dangerous Command Detection[/yellow] - Warns about risky operations\n"
        "⏱️  [yellow]Timeout Protection[/yellow] - Commands timeout after 60 seconds\n"
        "👁️  [yellow]Dry Run Mode[/yellow] - Preview commands without executing\n"
        "🔒 [yellow]Secure API Storage[/yellow] - Keys stored in system keyring",
        border_style="red"
    ))

def main():
    """Main demo function."""
    print_banner()
    
    console.print("[bold]Welcome to the Torvix Demo![/bold]\n")
    console.print("Torvix translates natural language into terminal commands")
    console.print("and executes them with your confirmation.\n")
    
    while True:
        console.print("[bold blue]Demo Options:[/bold blue]")
        console.print("1. View example commands")
        console.print("2. Installation guide")
        console.print("3. Safety features")
        console.print("4. Exit")
        
        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "1":
            demo_commands()
        elif choice == "2":
            installation_guide()
        elif choice == "3":
            safety_features()
        elif choice == "4":
            console.print("\n[green]Thanks for trying Torvix![/green]")
            console.print("Get started: [yellow]pip install torvix[/yellow]")
            break
        
        if choice != "4":
            console.print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
        sys.exit(0)
