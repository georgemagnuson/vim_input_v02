#!/usr/bin/env python3
"""
Test the true bordered input area implementation.
"""

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

def test_true_box():
    """Test the true bordered input area."""
    console.print(Rule("True Bordered Input Test", style="green"))

    instructions = """
This tests the TRUE bordered input area where:
• Input is constrained within actual box borders
• Text wrapping respects box boundaries
• Cursor movement is limited to box interior
• Different box styles create real containers

Try different box styles and notice how the input area is truly contained!
    """

    console.print(Panel(instructions.strip(), border_style="green"))
    console.print()

    try:
        from vim_readline import rich_vim_input

        # Test different box styles
        styles = [
            ("rounded", "🔄 Rounded Box (Claude Code style)", "blue"),
            ("square", "⬜ Square Box (Clean borders)", "green"),
            ("double", "🔲 Double Box (Bold emphasis)", "yellow"),
            ("heavy", "⬛ Heavy Box (Maximum emphasis)", "red")
        ]

        for style_name, title, color in styles:
            console.print(f"\n[bold {color}]Testing {title}[/bold {color}]")
            console.print("Watch how the input stays within the box boundaries!")

            result = rich_vim_input(
                initial_text=f"This text is constrained within the {style_name} box!\n\nTry typing more text and see how it wraps within the borders.\nUse vim commands: ESC for normal mode, i for insert mode.",
                panel_title=f"📦 {style_name.title()} Box Test",
                panel_box_style=style_name,
                show_rules=True,
                rule_style=color,
                show_line_numbers=True,
                show_status=True,
                enhanced_status=True
            )

            if result is not None:
                console.print(f"[{color}]✅ {style_name.title()} test completed![/{color}]")
                # Show result in a panel
                result_panel = Panel(
                    result,
                    title=f"📄 Your {style_name.title()} Box Content",
                    border_style=color
                )
                console.print(result_panel)
            else:
                console.print(f"[dim]{style_name.title()} test cancelled[/dim]")

            if len(styles) > 1:  # If not the last one
                if not console.input(f"\n[dim]Press Enter to try next style (or 'q' to quit):[/dim] ").lower().startswith('q'):
                    continue
                else:
                    break

    except ImportError:
        console.print("[red]❌ Rich not available - install with: pip install rich[/red]")
    except KeyboardInterrupt:
        console.print("[yellow]Test interrupted[/yellow]")

def main():
    """Main test function."""
    console.print()
    console.print("[bold blue]📦 True Bordered Input Area Test[/bold blue]")
    console.print()

    test_true_box()

    console.print()
    console.print("[green]🎉 True box testing complete![/green]")
    console.print()
    console.print("Key improvements:")
    console.print("  • [green]Input area is truly constrained within box borders[/green]")
    console.print("  • [blue]Text wrapping respects box boundaries[/blue]")
    console.print("  • [yellow]Dynamic sizing based on terminal width[/yellow]")
    console.print("  • [red]Multiple box styles with real borders[/red]")

if __name__ == "__main__":
    main()