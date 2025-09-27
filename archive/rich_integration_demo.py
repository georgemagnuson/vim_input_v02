#!/usr/bin/env python3
"""
Demo of Rich integration possibilities with vim-readline.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.box import Box, DOUBLE, ROUNDED, SQUARE, HEAVY
from rich import print as rprint
from rich.rule import Rule

def demo_rich_boxes():
    """Show different Rich box styles for vim-readline integration."""
    console = Console()

    print("\n=== Rich Box Styles for vim-readline ===\n")

    # Different box styles
    styles = [
        ("SQUARE", SQUARE, "Simple square borders"),
        ("ROUNDED", ROUNDED, "Rounded corners (like Claude Code)"),
        ("DOUBLE", DOUBLE, "Double-line borders"),
        ("HEAVY", HEAVY, "Heavy/bold borders")
    ]

    sample_text = """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)"""

    for name, box_style, desc in styles:
        panel = Panel(
            sample_text,
            title=f"vim-readline ({name})",
            title_align="left",
            box=box_style,
            expand=False,
            padding=(1, 2)
        )
        console.print(f"\n{desc}:")
        console.print(panel)

def demo_claude_code_style():
    """Demo Claude Code style with rules."""
    console = Console()

    print("\n=== Claude Code Style with Rules ===\n")

    # Top rule
    console.print(Rule("vim input", style="blue"))

    # Content area (this would be the vim-readline input)
    content = """def hello_world():
    print("Hello from vim-readline!")
    return True"""

    panel = Panel(
        content,
        box=ROUNDED,
        padding=(0, 1),
        expand=False
    )
    console.print(panel)

    # Bottom rule
    console.print(Rule(style="blue"))

def demo_enhanced_status():
    """Demo enhanced status bars with Rich."""
    console = Console()

    print("\n=== Enhanced Status Bars ===\n")

    # Vim mode indicators with Rich styling
    modes = [
        ("INSERT", "green", "✏️"),
        ("NORMAL", "blue", "🔍"),
        ("VISUAL", "yellow", "📝"),
        ("REPLACE", "red", "🔄")
    ]

    for mode, color, icon in modes:
        status = Text()
        status.append(f" {icon} ", style=f"{color}")
        status.append(f"-- {mode} --", style=f"bold {color}")

        panel = Panel(
            Align.center(status),
            box=SQUARE,
            height=3,
            expand=False
        )
        console.print(panel)

def demo_integration_concept():
    """Show how Rich could integrate with vim-readline."""
    console = Console()

    print("\n=== Integration Concept ===\n")

    console.print("Rich could provide:")
    console.print("  • [green]Bordered text areas[/green] (Panel)")
    console.print("  • [blue]Ruled lines above/below[/blue] (Rule)")
    console.print("  • [yellow]Enhanced status indicators[/yellow] (styled Text)")
    console.print("  • [red]Syntax highlighting[/red] (Pygments integration)")
    console.print("  • [magenta]Better error messages[/magenta] (Rich formatting)")

    print("\nTwo main approaches:")
    print("1. Rich renders the container, prompt-toolkit handles input")
    print("2. prompt-toolkit layout uses Rich-generated content")

if __name__ == "__main__":
    demo_rich_boxes()
    demo_claude_code_style()
    demo_enhanced_status()
    demo_integration_concept()