#!/usr/bin/env python3
"""
Test script to verify mode indicator changes work properly.

This script tests both the standard and Rich-enhanced vim-readline
to ensure the mode indicators update dynamically when modes change.
"""

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

def show_instructions():
    """Show test instructions."""
    console.print(Rule("Mode Indicator Test", style="blue"))

    instructions = """
Test Instructions:
1. The editor will start in INSERT mode (should show "-- INSERT --" or "✏️ -- INSERT --")
2. Press ESC to enter NORMAL mode (should change to "" or "🔍 -- NORMAL --")
3. Press 'i' to return to INSERT mode
4. Press 'v' in NORMAL mode for VISUAL mode (should show "-- VISUAL --" or "📝 -- VISUAL --")
5. Press 'V' in NORMAL mode for VISUAL LINE mode
6. Press 'R' in NORMAL mode for REPLACE mode (should show "-- REPLACE --" or "🔄 -- REPLACE --")
7. Press Return to submit when done testing

Watch the status bar at the bottom - it should change in real-time as you switch modes!
    """

    console.print(Panel(instructions.strip(), border_style="blue"))
    console.print()

def test_standard_vim_readline():
    """Test standard vim-readline mode indicators."""
    console.print("[bold green]Testing Standard VimReadline Mode Indicators[/bold green]")
    console.print("Look for status changes like: [dim]-- INSERT --, -- VISUAL --, etc.[/dim]")
    console.print()

    from vim_readline import vim_input

    result = vim_input(
        initial_text="Test mode switching here!\nTry ESC, i, v, V, R commands.",
        show_status=True,
        show_line_numbers=True
    )

    if result is not None:
        console.print(f"[green]✅ Standard test completed[/green]")
    else:
        console.print("[yellow]📝 Standard test cancelled[/yellow]")

def test_rich_vim_readline():
    """Test Rich-enhanced vim-readline mode indicators."""
    console.print("[bold magenta]Testing Rich-Enhanced VimReadline Mode Indicators[/bold magenta]")
    console.print("Look for enhanced status with emojis: [dim]✏️ -- INSERT --, 🔍 -- NORMAL --, etc.[/dim]")
    console.print()

    try:
        from vim_readline import rich_vim_input

        result = rich_vim_input(
            initial_text="Test Rich mode switching!\nTry ESC, i, v, V, R commands.",
            panel_title="🧪 Mode Indicator Test",
            panel_box_style="rounded",
            show_rules=True,
            rule_style="magenta",
            show_status=True,
            enhanced_status=True,
            show_line_numbers=True
        )

        if result is not None:
            console.print(f"[green]✅ Rich test completed[/green]")
        else:
            console.print("[yellow]📝 Rich test cancelled[/yellow]")

    except ImportError:
        console.print("[red]❌ Rich not available - install with: pip install rich[/red]")

def main():
    """Main test function."""
    console.print()
    console.print("[bold blue]🧪 VimReadline Mode Indicator Test[/bold blue]")
    console.print()

    show_instructions()

    # Test standard version
    if console.input("Test standard VimReadline? [y/N]: ").lower().startswith('y'):
        test_standard_vim_readline()
        console.print()

    # Test Rich version
    if console.input("Test Rich-enhanced VimReadline? [y/N]: ").lower().startswith('y'):
        test_rich_vim_readline()
        console.print()

    console.print("[blue]🎉 Mode indicator testing complete![/blue]")
    console.print()
    console.print("The mode indicators should have changed in real-time as you switched between:")
    console.print("  • [green]INSERT mode[/green] - for typing text")
    console.print("  • [blue]NORMAL mode[/blue] - for vim navigation")
    console.print("  • [yellow]VISUAL mode[/yellow] - for text selection")
    console.print("  • [red]REPLACE mode[/red] - for overwriting text")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Test interrupted[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")