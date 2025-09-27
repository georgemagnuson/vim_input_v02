#!/usr/bin/env python3
"""
Vim Rich Box Style Editor - Vim editor with Rich box style appearance.

This creates a prompt-toolkit layout that renders Rich-style boxes around the
vim editing area. Uses Rich's character sets for authentic appearance, but
prompt-toolkit does all the actual rendering (pseudo-Rich approach).
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.containers import ScrollOffsets
from prompt_toolkit.layout.margins import NumberedMargin, ConditionalMargin
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.cursor_shapes import ModalCursorShapeConfig

# Rich imports for extracting box characters
from rich import box
from rich.console import Console


class VimInsideRich:
    """
    Vim editor that renders INSIDE Rich box boundaries.

    This creates a prompt-toolkit interface where the actual vim editing
    area is surrounded by Rich-style borders, making it appear as if
    you're editing inside a Rich box.
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 box_title="Vim Inside Rich",
                 rich_box_style="ROUNDED",
                 box_width=80,
                 box_height=20,
                 show_line_numbers=True,
                 show_status=True):

        self.initial_text = initial_text
        self.placeholder_text = placeholder_text
        self.box_title = box_title
        self.rich_box_style = rich_box_style
        self.box_width = box_width
        self.box_height = box_height
        self.show_line_numbers = show_line_numbers
        self.show_status = show_status

        # Rich box styles
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII
        }
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # Create buffer with initial content
        self.buffer = Buffer(
            document=self._create_initial_document(),
            multiline=True
        )

        # Create the application
        self.app = None
        self.result = None

    def _create_initial_document(self):
        """Create initial document with content."""
        from prompt_toolkit.document import Document

        text = self.initial_text or ""
        if not text and self.placeholder_text:
            text = self.placeholder_text

        return Document(text)

    def _extract_rich_box_characters(self):
        """Extract Rich box drawing characters."""
        return {
            "top_left": self.rich_box.top_left,
            "top_right": self.rich_box.top_right,
            "bottom_left": self.rich_box.bottom_left,
            "bottom_right": self.rich_box.bottom_right,
            "horizontal": self.rich_box.top,
            "vertical": self.rich_box.mid_left,
        }

    def _create_rich_border_lines(self):
        """Create Rich-style border lines for the box."""
        chars = self._extract_rich_box_characters()

        # Calculate content dimensions
        content_width = self.box_width - 2  # Account for left/right borders

        # Create title line
        if self.box_title:
            title_text = f" {self.box_title} "
            title_len = len(title_text)
            if title_len <= content_width:
                remaining = content_width - title_len
                left_pad = remaining // 2
                right_pad = remaining - left_pad
                top_line = chars["top_left"] + chars["horizontal"] * left_pad + title_text + chars["horizontal"] * right_pad + chars["top_right"]
            else:
                top_line = chars["top_left"] + chars["horizontal"] * content_width + chars["top_right"]
        else:
            top_line = chars["top_left"] + chars["horizontal"] * content_width + chars["top_right"]

        return top_line, chars["vertical"], content_width

    def _create_bottom_border_with_mode(self):
        """Create bottom border line with vim mode information."""
        chars = self._extract_rich_box_characters()
        content_width = self.box_width - 2  # Account for left/right borders

        def get_bottom_line():
            # Get current vim mode
            mode_text = ""
            if self.app and hasattr(self.app, 'vi_state'):
                if self.app.vi_state.input_mode == 'vi-insert':
                    mode_text = " INSERT "
                elif self.app.vi_state.input_mode == 'vi-replace':
                    mode_text = " REPLACE "
                elif self.app.vi_state.input_mode == 'vi-navigation':
                    selection = self.buffer.selection_state
                    if selection:
                        from prompt_toolkit.selection import SelectionType
                        if selection.type == SelectionType.LINES:
                            mode_text = " VISUAL LINE "
                        elif selection.type == SelectionType.BLOCK:
                            mode_text = " VISUAL BLOCK "
                        else:
                            mode_text = " VISUAL "
                    else:
                        mode_text = " NORMAL "

            if not mode_text:
                mode_text = " NORMAL "

            # Create bottom line with left-aligned mode text
            mode_len = len(mode_text)
            if mode_len <= content_width:
                remaining = content_width - mode_len
                return chars["bottom_left"] + mode_text + chars["horizontal"] * remaining + chars["bottom_right"]
            else:
                # Mode text too long, just use horizontal line
                return chars["bottom_left"] + chars["horizontal"] * content_width + chars["bottom_right"]

        return get_bottom_line

    def _create_layout(self):
        """Create layout with Rich-style borders around vim editing area."""

        # Get Rich border components
        top_border, vertical_char, content_width = self._create_rich_border_lines()
        bottom_border_func = self._create_bottom_border_with_mode()

        # Calculate content dimensions
        content_height = self.box_height - 2  # Account for top/bottom borders

        # Create buffer control with vim functionality
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Create the main editing window (this is WHERE vim editing happens)
        vim_editor_window = Window(
            content=buffer_control,
            wrap_lines=True,
            width=Dimension(min=content_width, max=content_width, preferred=content_width),
            height=Dimension(min=content_height, max=content_height, preferred=content_height),
            scroll_offsets=ScrollOffsets(left=0, right=0, top=1, bottom=1),
            # Add line numbers if requested
            left_margins=[ConditionalMargin(
                margin=NumberedMargin(display_tildes=False),
                filter=Condition(lambda: self.show_line_numbers)
            )] if self.show_line_numbers else []
        )

        # Create Rich-style border windows

        # Top border with title
        top_border_window = Window(
            content=FormattedTextControl(lambda: top_border),
            height=1,
            width=Dimension(min=self.box_width, max=self.box_width),
            style='class:rich-border'
        )

        # Middle section with side borders + vim editor
        middle_section = VSplit([
            # Left border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([vertical_char] * content_height)
                ),
                width=1,
                style='class:rich-border'
            ),
            # VIM EDITING AREA (this is inside the Rich box!)
            vim_editor_window,
            # Right border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([vertical_char] * content_height)
                ),
                width=1,
                style='class:rich-border'
            )
        ], padding=0)

        # Bottom border with vim mode information
        bottom_border_window = Window(
            content=FormattedTextControl(bottom_border_func),
            height=1,
            width=Dimension(min=self.box_width, max=self.box_width),
            style='class:rich-border'
        )

        # Assemble the complete layout - no separate status bar needed
        layout_components = [
            top_border_window,
            middle_section,
            bottom_border_window
        ]

        return Layout(HSplit(layout_components))

    def _create_key_bindings(self):
        """Create key bindings for vim functionality."""
        kb = KeyBindings()

        @kb.add('c-m')  # Enter - submit
        def _(event):
            self.result = self.buffer.text
            event.app.exit()

        @kb.add('c-c')  # Ctrl+C - cancel
        def _(event):
            self.result = None
            event.app.exit()

        return kb

    def _create_style(self):
        """Create Rich-inspired styling."""
        return Style.from_dict({
            'rich-border': '#888888',  # Rich's default border color
            'vim-status': 'reverse',   # Vim status line
            'line-number': '#888888',  # Line numbers
        })

    def run(self):
        """Run the vim editor inside Rich box boundaries."""

        # Show preview
        console = Console()
        console.print()
        console.print(f"🎯 Starting Vim Editor INSIDE {self.rich_box_style} Rich Box Boundaries")
        console.print("=" * 70)
        console.print()
        console.print("The vim editing area will be surrounded by Rich box borders.")
        console.print("All vim editing happens INSIDE those visual boundaries!")
        console.print()
        console.print("🎮 Vim Controls:")
        console.print("  • ESC: Normal mode (hjkl navigation, dd, yy, p, etc.)")
        console.print("  • i/a/o: Insert modes")
        console.print("  • v: Visual mode")
        console.print("  • All standard vim commands work!")
        console.print("  • Ctrl+M (Enter): Submit")
        console.print("  • Ctrl+C: Cancel")
        console.print()

        # Create the application with vim editing mode
        self.app = Application(
            layout=self._create_layout(),
            key_bindings=self._create_key_bindings(),
            style=self._create_style(),
            editing_mode=EditingMode.VI,  # ENABLE VIM MODE
            cursor=ModalCursorShapeConfig(),  # Vim cursor shapes
            full_screen=True,
            mouse_support=True
        )

        print("🚀 Vim editor with Rich box boundaries starting...")
        print("(The vim editing area will appear inside Rich-style borders)")
        print()

        # Run the application
        try:
            self.app.run()
        except (EOFError, KeyboardInterrupt):
            self.result = None

        # Show result
        console.print()
        if self.result is not None:
            from rich.panel import Panel
            result_panel = Panel(
                self.result,
                title=f"✅ Vim Editing Result - {self.rich_box_style} Style",
                box=self.rich_box,
                border_style="green"
            )
            console.print(result_panel)
            console.print(f"\n🎉 SUCCESS: Vim editing happened INSIDE {self.rich_box_style} Rich box boundaries!")
        else:
            console.print("❌ Vim editing cancelled")

        return self.result


def main():
    """Main demo app."""
    print("⚡ VIM INSIDE RICH BOXES")
    print("=" * 50)
    print()
    print("This creates vim editing that happens INSIDE Rich box visual boundaries!")
    print("The vim editing area is surrounded by Rich-style borders.")
    print()

    # Choose Rich box style
    print("Choose Rich box style:")
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

    # Create vim editor
    editor = VimInsideRich(
        box_title=f'Vim Inside {rich_style} Rich Box',
        rich_box_style=rich_style,
        box_width=85,
        box_height=22,
        initial_text=f'''# Vim Editing Inside {rich_style} Rich Box!

def vim_inside_rich_demo():
    """
    This vim editing is happening INSIDE Rich box boundaries!

    You can see the {rich_style} borders around this editing area.
    All vim functionality is available:

    • hjkl navigation
    • dd to delete lines
    • yy to yank (copy)
    • p to paste
    • i/a/o for insert modes
    • v for visual mode
    • And all other vim commands!
    """

    print("Editing inside Rich box boundaries!")
    print("The vim interface IS the Rich box!")

    return "vim_editing_inside_rich_success"

# Try editing this code with full vim power!
# Notice the {rich_style} borders surrounding this editing area.
# This IS a Rich box - you're editing inside it!''',
        show_line_numbers=True,
        show_status=True
    )

    # Run the editor
    result = editor.run()

    print("\n" + "=" * 70)
    if result:
        print("🎉 Vim editing inside Rich box boundaries: SUCCESS!")
    else:
        print("👋 Vim editing cancelled")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")