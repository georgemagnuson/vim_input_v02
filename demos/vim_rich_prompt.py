#!/usr/bin/env python3
"""
Vim-Rich Prompt Editor - Full vim inside Rich-styled prompt-toolkit interface.

This uses prompt-toolkit's built-in vim mode but styles the interface to look
like you're editing inside Rich boxes. No additional dependencies needed!
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline.core import VimReadline
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.align import Align


class VimRichPromptEditor:
    """
    Vim editor with Rich-styled display that uses prompt-toolkit's vim mode.

    This gives you full vim functionality without needing the keyboard library,
    while making it LOOK like you're editing inside Rich boxes.
    """

    def __init__(self,
                 initial_text="",
                 box_title="Vim Rich Editor",
                 rich_box_style="ROUNDED",
                 box_width=80,
                 box_height=15,
                 show_line_numbers=True,
                 show_status=True):

        self.initial_text = initial_text
        self.box_title = box_title
        self.rich_box_style = rich_box_style
        self.box_width = box_width
        self.box_height = box_height
        self.show_line_numbers = show_line_numbers
        self.show_status = show_status

        # Rich setup
        self.console = Console()
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII
        }
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

    def _show_rich_preview(self):
        """Show Rich preview of what we're about to edit."""
        preview_text = self.initial_text or "Ready for vim editing inside Rich boxes..."

        preview_panel = Panel(
            preview_text,
            title=f"📝 {self.box_title} - Preview",
            box=self.rich_box,
            width=self.box_width,
            border_style="blue"
        )

        instructions = Panel(
            "🎯 VIM EDITING INSIDE RICH BOUNDARIES\n\n"
            "You're about to edit with FULL vim capabilities:\n"
            "• ESC: Normal mode (hjkl navigation, dd, yy, p, etc.)\n"
            "• i/a/o: Insert modes\n"
            "• v: Visual mode\n"
            "• All standard vim commands work!\n\n"
            "The editor will look like you're editing inside this Rich box.\n\n"
            "Press Enter when ready...",
            title="⚡ Vim + Rich Integration",
            box=box.MINIMAL,
            border_style="green"
        )

        self.console.print()
        self.console.print(Align.center(preview_panel))
        self.console.print(Align.center(instructions))

        input("\nPress Enter to start vim editing inside Rich-styled interface...")
        print()

    def _show_rich_result(self, result):
        """Show Rich result after vim editing."""
        if result is None:
            result = "(cancelled)"
            border_style = "red"
            title = f"❌ {self.box_title} - Cancelled"
        else:
            border_style = "green"
            title = f"✅ {self.box_title} - Final Result"

        result_panel = Panel(
            result,
            title=title,
            box=self.rich_box,
            width=self.box_width,
            border_style=border_style
        )

        stats_text = (
            f"🎯 Vim editing inside Rich box boundaries: SUCCESS!\n\n"
            f"📊 Statistics:\n"
            f"• Characters: {len(result) if result != '(cancelled)' else 0}\n"
            f"• Lines: {len(result.split(chr(10))) if result != '(cancelled)' else 0}\n"
            f"• Words: {len(result.split()) if result != '(cancelled)' else 0}\n"
            f"• Box style: {self.rich_box_style}\n\n"
            f"✨ Full vim capabilities were available during editing!"
        )

        stats_panel = Panel(
            stats_text,
            title="🎉 Vim-Rich Integration Complete",
            box=box.MINIMAL,
            border_style="blue"
        )

        self.console.print()
        self.console.print(Align.center(result_panel))
        self.console.print(Align.center(stats_panel))

    def run(self):
        """Run the vim-rich editor."""

        # Show Rich preview
        self._show_rich_preview()

        print(f"🚀 Starting vim editor with Rich {self.rich_box_style} styling...")
        print("(The editor will appear below with Rich-style borders)")
        print()

        # Create vim readline with Rich-inspired styling
        vim_editor = VimReadline(
            initial_text=self.initial_text,
            show_line_numbers=self.show_line_numbers,
            show_status=self.show_status,
            wrap_lines=True
        )

        # Run the vim editor
        result = vim_editor.run()

        # Show Rich result
        self._show_rich_result(result)

        return result


def main():
    """Main vim-rich demo app."""
    print("⚡ VIM-RICH PROMPT EDITOR")
    print("=" * 60)
    print()
    print("Full vim editing with Rich-styled interface!")
    print("✅ No extra dependencies needed (uses prompt-toolkit's built-in vim mode)")
    print("🎨 Rich-styled preview and results")
    print("⚡ Complete vim functionality")
    print()

    print("🎯 VIM FEATURES:")
    print("  • All vim modes: Normal, Insert, Visual, Replace")
    print("  • Navigation: hjkl, w, b, 0, $, gg, G")
    print("  • Editing: dd, yy, p, x, r, c, d, etc.")
    print("  • Visual selection and operations")
    print("  • Line numbers and status indicators")
    print("  • Everything you expect from vim!")
    print()

    # Get Rich box style
    print("Choose Rich box style for preview/results:")
    print("1. ROUNDED (default)")
    print("2. SQUARE")
    print("3. DOUBLE")
    print("4. HEAVY")
    print("5. ASCII")

    try:
        choice = input("\nEnter choice (1-5, or Enter for ROUNDED): ").strip()
        style_map = {
            "1": "ROUNDED", "2": "SQUARE", "3": "DOUBLE",
            "4": "HEAVY", "5": "ASCII", "": "ROUNDED"
        }
        rich_style = style_map.get(choice, "ROUNDED")
    except (EOFError, KeyboardInterrupt):
        rich_style = "ROUNDED"
        print()

    print(f"✅ Using {rich_style} style for Rich integration")
    print()

    # Create vim-rich editor
    editor = VimRichPromptEditor(
        box_title=f'Vim Rich Editor - {rich_style}',
        rich_box_style=rich_style,
        box_width=75,
        box_height=15,
        initial_text=f'# Welcome to Vim + Rich Integration!\n\ndef vim_rich_demo():\n    """\n    This is REAL vim editing with Rich styling.\n    \n    Try all your favorite vim commands:\n    • hjkl navigation\n    • dd to delete lines\n    • yy to yank (copy)\n    • p to paste\n    • i/a/o for insert modes\n    • v for visual mode\n    • And much more!\n    """\n    print("Vim + Rich = Perfect!")\n    return "editing_inside_rich_boundaries"\n\n# Edit this code with full vim power!\n# The Rich preview shows you\'re editing inside Rich box boundaries.',
        show_line_numbers=True,
        show_status=True
    )

    # Run the editor
    result = editor.run()

    print(f"\n{'='*80}")
    if result is not None:
        print("🎉 Vim-Rich editing complete!")
        print("You used full vim capabilities with Rich-styled interface!")
    else:
        print("👋 Vim-Rich editing cancelled.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")