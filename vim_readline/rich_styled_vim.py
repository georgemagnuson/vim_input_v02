"""
Rich-styled VimReadline that makes prompt-toolkit look like Rich boxes.

This creates a prompt-toolkit interface that visually appears as if you're
editing inside Rich boxes, with Rich-style borders and formatting.
"""

from .core import VimReadline as BaseVimReadline
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.containers import ScrollOffsets
from prompt_toolkit.layout.margins import NumberedMargin, ConditionalMargin
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.layout import Layout

# Rich imports for character extraction
from rich import box
from rich.console import Console
from rich.panel import Panel
import io
import os


class RichStyledVimReadline(BaseVimReadline):
    """
    VimReadline that looks and feels like editing inside Rich boxes.

    This uses prompt-toolkit for the editing but styles it to appear
    as if you're editing within Rich box boundaries.
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 prompt="",
                 show_line_numbers=False,
                 show_status=True,
                 wrap_lines=True,
                 submit_key='c-m',
                 newline_key='c-j',
                 cancel_keys=None,
                 # Rich styling options
                 box_title="Rich-Styled Editor",
                 rich_box_style="ROUNDED",
                 box_width=70,
                 box_height=15):

        # Rich styling configuration
        self.box_title = box_title
        self.rich_box_style = rich_box_style
        self.box_width = box_width
        self.box_height = box_height

        # Rich box styles
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII
        }

        # Get Rich box object
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # Initialize parent
        super().__init__(
            initial_text=initial_text,
            placeholder_text=placeholder_text,
            prompt=prompt,
            show_line_numbers=show_line_numbers,
            show_status=show_status,
            wrap_lines=wrap_lines,
            submit_key=submit_key,
            newline_key=newline_key,
            cancel_keys=cancel_keys
        )

    def _get_terminal_size(self):
        """Get terminal dimensions."""
        try:
            columns, rows = os.get_terminal_size()
            return columns, rows
        except (AttributeError, OSError):
            return 80, 24

    def _extract_rich_characters(self):
        """Extract Rich box characters."""
        return {
            "top_left": self.rich_box.top_left,
            "top_right": self.rich_box.top_right,
            "bottom_left": self.rich_box.bottom_left,
            "bottom_right": self.rich_box.bottom_right,
            "horizontal": self.rich_box.top,
            "vertical": self.rich_box.mid_left,
        }

    def _create_rich_border_lines(self):
        """Create Rich-style border lines."""
        chars = self._extract_rich_characters()

        # Calculate content area
        content_width = self.box_width - 2  # Account for borders

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
                # Title too long, just use horizontal line
                top_line = chars["top_left"] + chars["horizontal"] * content_width + chars["top_right"]
        else:
            top_line = chars["top_left"] + chars["horizontal"] * content_width + chars["top_right"]

        # Create bottom line
        bottom_line = chars["bottom_left"] + chars["horizontal"] * content_width + chars["bottom_right"]

        return top_line, bottom_line, chars["vertical"]

    def _create_layout(self):
        """Create layout that looks like editing inside Rich boxes."""

        # Get Rich border lines
        top_border, bottom_border, vertical_char = self._create_rich_border_lines()

        # Calculate content dimensions
        content_width = self.box_width - 2  # Account for left/right borders
        content_height = self.box_height - 2  # Account for top/bottom borders

        # Create buffer control
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Create the main text window
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            width=Dimension(min=content_width, max=content_width, preferred=content_width),
            height=Dimension(min=content_height, max=content_height, preferred=content_height),
            ignore_content_width=True,
            ignore_content_height=True,
            scroll_offsets=ScrollOffsets(left=0, right=0, top=0, bottom=0),
            # Optional line numbers
            left_margins=[ConditionalMargin(
                margin=NumberedMargin(display_tildes=False),
                filter=Condition(lambda: self.show_line_numbers)
            )] if self.show_line_numbers else []
        )

        # Create Rich-style borders

        # Top border
        top_border_window = Window(
            content=FormattedTextControl(lambda: top_border),
            height=1,
            width=Dimension(min=self.box_width, max=self.box_width, preferred=self.box_width),
            style='class:rich-border'
        )

        # Middle section with side borders
        middle_section = VSplit([
            # Left border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([vertical_char] * content_height)
                ),
                width=1,
                style='class:rich-border'
            ),
            # Text area (the actual editing happens here)
            text_window,
            # Right border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([vertical_char] * content_height)
                ),
                width=1,
                style='class:rich-border'
            )
        ], padding=0)

        # Bottom border
        bottom_border_window = Window(
            content=FormattedTextControl(lambda: bottom_border),
            height=1,
            width=Dimension(min=self.box_width, max=self.box_width, preferred=self.box_width),
            style='class:rich-border'
        )

        # Assemble main layout
        main_components = [
            top_border_window,
            middle_section,
            bottom_border_window
        ]

        # Optional status bar (outside the box)
        if self.show_status:
            def get_status():
                app = self.app
                if app and hasattr(app, 'vi_state'):
                    if app.vi_state.input_mode == 'vi-insert':
                        if app.vi_state.temporary_navigation_mode:
                            return '-- (insert) --'
                        else:
                            return '-- INSERT --'
                    elif app.vi_state.input_mode == 'vi-replace':
                        return '-- REPLACE --'
                    elif app.vi_state.input_mode == 'vi-navigation':
                        selection = self.buffer.selection_state
                        if selection:
                            from prompt_toolkit.selection import SelectionType
                            if selection.type == SelectionType.LINES:
                                return '-- VISUAL LINE --'
                            elif selection.type == SelectionType.BLOCK:
                                return '-- VISUAL BLOCK --'
                            else:
                                return '-- VISUAL --'
                        return ''
                return ''

            status_window = Window(
                content=FormattedTextControl(get_status),
                height=1,
                style='class:status'
            )
            main_components.append(status_window)

        # Create final layout
        self.layout = Layout(HSplit(main_components))

    def _create_style(self):
        """Create Rich-inspired styling."""
        base_style = super()._create_style()
        base_dict = dict(base_style.style_rules)

        # Rich-inspired styles
        rich_styles = {
            'rich-border': '#888888',  # Rich's default border color
            'status': 'reverse',
        }

        return Style.from_dict({**base_dict, **rich_styles})

    def run(self):
        """Run with Rich-style pre/post display."""

        # Show Rich preview
        self._show_rich_preview()

        # Run the actual editing (which now looks Rich-styled)
        result = super().run()

        # Show Rich result
        if result is not None:
            self._show_rich_result(result)

        return result

    def _show_rich_preview(self):
        """Show Rich preview before editing."""
        console = Console()

        preview_text = self.initial_text or self.placeholder_text or "Ready to edit..."

        preview_panel = Panel(
            preview_text,
            title=f"🎨 {self.box_title} - Preview",
            box=self.rich_box,
            width=self.box_width,
            border_style="blue"
        )

        instructions = Panel(
            "You are about to edit inside a Rich-styled interface!\n\n"
            "The editing area will look like a Rich box, but you'll have\n"
            "full vim editing capabilities within those boundaries.\n\n"
            "Press Enter when ready...",
            title="📝 Instructions",
            box=box.MINIMAL,
            border_style="green"
        )

        console.print()
        from rich.align import Align
        console.print(Align.center(preview_panel))
        console.print(Align.center(instructions))

        input("\nPress Enter to start Rich-styled editing...")

    def _show_rich_result(self, result):
        """Show Rich result after editing."""
        console = Console()

        result_panel = Panel(
            result,
            title=f"✅ {self.box_title} - Final Result",
            box=self.rich_box,
            width=self.box_width,
            border_style="green"
        )

        stats_text = (
            f"Characters: {len(result)}\n"
            f"Lines: {len(result.split(chr(10)))}\n"
            f"Words: {len(result.split())}\n"
            f"Box style: {self.rich_box_style}"
        )

        stats_panel = Panel(
            stats_text,
            title="📊 Statistics",
            box=box.MINIMAL,
            border_style="blue"
        )

        console.print()
        from rich.align import Align
        console.print(Align.center(result_panel))
        console.print(Align.center(stats_panel))


# Convenience function
def rich_styled_vim_input(prompt="",
                         initial_text="",
                         placeholder_text="",
                         show_line_numbers=False,
                         show_status=True,
                         wrap_lines=True,
                         box_title="Rich Editor",
                         rich_box_style="ROUNDED",
                         box_width=70,
                         box_height=15):
    """
    Create vim input that looks like editing inside Rich boxes.

    Args:
        prompt: Prompt text
        initial_text: Pre-populated text
        placeholder_text: Placeholder when empty
        show_line_numbers: Show line numbers
        show_status: Show vim mode status
        wrap_lines: Wrap long lines
        box_title: Title for the Rich-styled box
        rich_box_style: Rich box style (ROUNDED, SQUARE, DOUBLE, etc.)
        box_width: Width of the editing area
        box_height: Height of the editing area

    Returns:
        str: Edited text or None if cancelled
    """
    editor = RichStyledVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        box_title=box_title,
        rich_box_style=rich_box_style,
        box_width=box_width,
        box_height=box_height
    )
    return editor.run()


def demo_rich_styled_vim():
    """Demo the Rich-styled vim interface."""
    print("🎨 Rich-Styled VimReadline Demo")
    print("=" * 50)
    print()
    print("This creates a prompt-toolkit interface that LOOKS like")
    print("you're editing inside Rich boxes, with proper vim functionality.")
    print()

    # Demo with different styles
    styles = [
        ("ROUNDED", "Rich's signature rounded corners"),
        ("SQUARE", "Clean square corners"),
        ("DOUBLE", "Double lines for emphasis")
    ]

    for style_name, description in styles:
        print(f"\n📦 {style_name} Style: {description}")

        if input(f"Try {style_name} style? (y/N): ").lower().startswith('y'):
            result = rich_styled_vim_input(
                initial_text=f"Rich-styled {style_name} editor demo!\n\nThis interface looks like a Rich box,\nbut you have full vim editing power.\n\nTry:\n• ESC: Normal mode\n• i: Insert mode\n• hjkl: Navigation\n• And all other vim commands!",
                box_title=f"{style_name} Rich Editor",
                rich_box_style=style_name,
                box_width=60,
                box_height=12,
                show_line_numbers=True,
                show_status=True
            )

            if result:
                print(f"✅ {style_name} demo completed!")
            else:
                print(f"⚠️ {style_name} demo cancelled")


if __name__ == "__main__":
    demo_rich_styled_vim()