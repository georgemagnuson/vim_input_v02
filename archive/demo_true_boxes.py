#!/usr/bin/env python3
"""
Visual demo of the true box styles.
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

def demo_box_styles():
    """Show what each box style looks like."""
    console.print("[bold blue]📦 True Box Styles Demo[/bold blue]")
    console.print()

    # Box characters for each style
    styles = {
        "rounded": {
            'top_left': '╭', 'top_right': '╮',
            'bottom_left': '╰', 'bottom_right': '╯',
            'horizontal': '─', 'vertical': '│',
            'desc': "Claude Code style - smooth and modern"
        },
        "square": {
            'top_left': '┌', 'top_right': '┐',
            'bottom_left': '└', 'bottom_right': '┘',
            'horizontal': '─', 'vertical': '│',
            'desc': "Clean and simple - classic terminal"
        },
        "double": {
            'top_left': '╔', 'top_right': '╗',
            'bottom_left': '╚', 'bottom_right': '╝',
            'horizontal': '═', 'vertical': '║',
            'desc': "Bold emphasis - important content"
        },
        "heavy": {
            'top_left': '┏', 'top_right': '┓',
            'bottom_left': '┗', 'bottom_right': '┛',
            'horizontal': '━', 'vertical': '┃',
            'desc': "Maximum emphasis - critical sections"
        }
    }

    for name, chars in styles.items():
        console.print(f"[bold]{name.title()} Style[/bold] - {chars['desc']}")

        # Create a sample box
        width = 50
        sample_text = "This is how text appears within the box.\nIt's truly constrained by the borders.\nVim editing happens inside this area!"

        # Top border
        title = f" vim input ({name}) "
        title_len = len(title)
        padding = (width - title_len - 2) // 2
        remaining = width - title_len - 2 - padding

        top_border = f"{chars['top_left']}{chars['horizontal']}{title}{chars['horizontal'] * (padding + remaining)}{chars['top_right']}"

        # Content lines
        content_lines = sample_text.split('\n')
        max_content_width = width - 2  # Account for side borders

        # Bottom border
        bottom_border = f"{chars['bottom_left']}{chars['horizontal'] * width}{chars['bottom_right']}"

        # Print the box
        console.print(top_border)
        for line in content_lines:
            if len(line) > max_content_width:
                # Wrap long lines
                wrapped_lines = [line[i:i+max_content_width] for i in range(0, len(line), max_content_width)]
                for wrapped_line in wrapped_lines:
                    padded_line = wrapped_line.ljust(max_content_width)
                    console.print(f"{chars['vertical']}{padded_line}{chars['vertical']}")
            else:
                padded_line = line.ljust(max_content_width)
                console.print(f"{chars['vertical']}{padded_line}{chars['vertical']}")

        console.print(bottom_border)
        console.print()

def main():
    """Main demo."""
    demo_box_styles()

    console.print("[green]🎯 Key Features of True Boxes:[/green]")
    console.print("  • Text input is constrained within the actual borders")
    console.print("  • Different Unicode box drawing characters for each style")
    console.print("  • Dynamic sizing based on terminal width")
    console.print("  • Proper text wrapping respects box boundaries")
    console.print("  • Vim editing happens entirely within the box area")
    console.print()

    console.print("[blue]🚀 Try it yourself:[/blue]")
    console.print("  python simple_rich_app.py")
    console.print("  python test_mode_indicator.py")
    console.print()
    console.print("The input area will be truly contained within these boxes!")

if __name__ == "__main__":
    main()