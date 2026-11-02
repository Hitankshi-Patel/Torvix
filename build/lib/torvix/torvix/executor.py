"""
Command execution module for Torvix
"""

import re
import subprocess
import sys
from typing import List, Optional
from rich.console import Console
from rich.prompt import Confirm
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

class CommandExecutor:
    """Handles parsing and execution of commands from AI responses."""
    
    def __init__(self):
        self.dangerous_commands = {
            'rm -rf', 'sudo rm', 'format', 'fdisk', 'mkfs',
            'dd if=', 'shutdown', 'reboot', 'halt',
            'chmod 777', 'chown -R', 'sudo chmod',
            '| sh', '| bash', 'curl.*| sh', 'wget.*| sh',
            'pip install --force-reinstall',
            'npm install -g', 'sudo npm', 'sudo pip'
        }
    
    def parse_commands(self, ai_response: str) -> List[str]:
        """Parse commands from AI response that are prefixed with 'RUN:'."""
        commands = []
        lines = ai_response.split('\n')

        for line in lines:
            line = line.strip()
            # Handle different RUN: formats
            if line.startswith('RUN:'):
                command = line[4:].strip()
                if command:
                    commands.append(command)
            elif line.startswith('**RUN:**'):
                command = line[8:].strip()
                if command:
                    commands.append(command)
            elif '**RUN:**' in line:
                # Extract command after **RUN:**
                parts = line.split('**RUN:**', 1)
                if len(parts) > 1:
                    command = parts[1].strip()
                    if command:
                        commands.append(command)

        return commands
    
    def is_dangerous_command(self, command: str) -> bool:
        """Check if a command is potentially dangerous."""
        command_lower = command.lower()
        return any(dangerous in command_lower for dangerous in self.dangerous_commands)
    
    def execute_commands(self, commands: List[str], dry_run: bool = False):
        """Execute commands with user confirmation."""
        if not commands:
            console.print("[yellow]No commands to execute[/yellow]")
            return
        
        console.print(f"\n[bold blue]Found {len(commands)} command(s) to execute:[/bold blue]")
        
        # Show all commands first
        for i, command in enumerate(commands, 1):
            style = "red" if self.is_dangerous_command(command) else "green"
            console.print(f"  {i}. [bold {style}]{command}[/bold {style}]")
        
        if dry_run:
            console.print("\n[yellow]Dry run mode - commands not executed[/yellow]")
            return
        
        console.print()
        
        # Execute commands one by one
        for i, command in enumerate(commands, 1):
            self._execute_single_command(command, i, len(commands))
    
    def _execute_single_command(self, command: str, index: int, total: int):
        """Execute a single command with confirmation."""
        # Show command with syntax highlighting
        console.print(Panel(
            Syntax(command, "bash", theme="monokai", line_numbers=False),
            title=f"[bold blue]Command {index}/{total}[/bold blue]",
            border_style="blue"
        ))
        
        # Check for dangerous commands
        if self.is_dangerous_command(command):
            console.print("[bold red]⚠️  WARNING: This command may be dangerous![/bold red]")
        
        # Get user confirmation
        if not Confirm.ask(f"Execute this command?", default=True):
            console.print("[yellow]Skipped[/yellow]\n")
            return
        
        # Execute the command
        try:
            console.print(f"[blue]Executing: {command}[/blue]")
            
            # Use shell=True to handle complex commands with pipes, etc.
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60  # 60 second timeout
            )
            
            # Display output
            if result.stdout:
                console.print("[green]Output:[/green]")
                console.print(result.stdout)
            
            if result.stderr:
                console.print("[yellow]Errors/Warnings:[/yellow]")
                console.print(result.stderr)
            
            if result.returncode == 0:
                console.print("[bold green]✓ Command completed successfully[/bold green]\n")
            else:
                console.print(f"[bold red]✗ Command failed with exit code {result.returncode}[/bold red]\n")
                
                # Ask if user wants to continue with remaining commands
                if index < total:
                    if not Confirm.ask("Continue with remaining commands?", default=False):
                        console.print("[yellow]Execution stopped by user[/yellow]")
                        return
        
        except subprocess.TimeoutExpired:
            console.print("[red]Command timed out after 60 seconds[/red]\n")
        except subprocess.SubprocessError as e:
            console.print(f"[red]Error executing command: {e}[/red]\n")
        except KeyboardInterrupt:
            console.print("\n[yellow]Command interrupted by user[/yellow]")
            raise
    
    def validate_command(self, command: str) -> tuple[bool, Optional[str]]:
        """Validate a command before execution."""
        if not command.strip():
            return False, "Empty command"
        
        # Check for basic shell injection patterns
        suspicious_patterns = [
            r';\s*rm\s+-rf',
            r'&&\s*rm\s+-rf',
            r'\|\s*sh',
            r'>\s*/dev/sd[a-z]',
            r'curl.*\|\s*bash',
            r'wget.*\|\s*sh'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Potentially dangerous pattern detected: {pattern}"
        
        return True, None
