"""
Rich-native box VimReadline implementation using Rich's built-in box routines.

This leverages Rich's Panel and box system instead of manually drawing borders,
providing better alignment, more styles, and proper rendering.
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

# Rich imports
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.text import Text
import io
import os


class RichBoxVimReadline(BaseVimReadline):
    """
    VimReadline that uses Rich's built-in box system for perfect border rendering.

    Advantages over manual border drawing:
    - Uses Rich's tested and optimized box routines
    - Perfect alignment guaranteed by Rich
    - More box styles available (ASCII, DOUBLE, HEAVY, etc.)
    - Better terminal compatibility
    - Automatic width/height calculations
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
                 # Rich box options
                 box_width=60,
                 box_height=10,
                 box_title="",
                 rich_box_style="ROUNDED",    # Rich box styles
                 auto_size=True,
                 expand_to_fit=True):

        # Rich box style mapping
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII,
            "MINIMAL": box.MINIMAL,
            "SIMPLE": box.SIMPLE,
            "SIMPLE_HEAVY": box.SIMPLE_HEAVY,
        }

        # Store Rich-specific configuration
        self.box_width = box_width
        self.box_height = box_height
        self.box_title = box_title
        self.rich_box_style = rich_box_style
        self.auto_size = auto_size
        self.expand_to_fit = expand_to_fit

        # Get the Rich box object
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # Rich console for rendering
        self.rich_console = Console()

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
        """Get current terminal dimensions."""
        try:
            columns, rows = os.get_terminal_size()
            return columns, rows
        except (AttributeError, OSError):
            return 80, 24  # fallback

    def _calculate_box_dimensions(self):
        """Calculate box dimensions using Rich's logic."""
        if self.auto_size:
            terminal_width, terminal_height = self._get_terminal_size()
            # Leave margin for terminal display
            content_width = min(self.box_width, terminal_width - 4)
            content_height = min(self.box_height, terminal_height - 6)
        else:
            content_width = self.box_width
            content_height = self.box_height

        return max(20, content_width), max(5, content_height)

    def _extract_rich_box_characters(self):
        """Extract box characters from Rich's box system."""
        return {
            "top_left": self.rich_box.top_left,
            "top_right": self.rich_box.top_right,
            "bottom_left": self.rich_box.bottom_left,
            "bottom_right": self.rich_box.bottom_right,
            "horizontal": self.rich_box.top,  # Use top for horizontal lines
            "vertical": self.rich_box.mid_left,  # Use mid_left for vertical lines
        }

    def _render_rich_panel_borders(self, width, height):
        """Use Rich Panel to render perfect borders and extract the structure."""

        # Create content that fills the desired dimensions
        content_lines = []
        for i in range(height):
            line = f"Line {i+1}".ljust(width)
            content_lines.append(line)

        content_text = "\n".join(content_lines)

        # Create Rich Panel
        panel = Panel(
            content_text,
            title=self.box_title if self.box_title else None,
            box=self.rich_box,
            width=width + 2,  # Account for borders
            expand=False
        )

        # Render to string to extract the border structure
        with io.StringIO() as string_io:
            temp_console = Console(
                file=string_io,
                width=width + 10,  # Extra width to prevent wrapping
                legacy_windows=False
            )
            temp_console.print(panel)
            rendered_output = string_io.getvalue()

        # Parse the rendered output to extract border lines
        lines = rendered_output.strip().split('\n')

        if len(lines) >= 3:
            top_border = lines[0]
            bottom_border = lines[-1]
            # Middle lines contain the vertical borders and content
            return top_border, bottom_border, lines[1:-1]
        else:
            # Fallback if rendering fails
            chars = self._extract_rich_box_characters()
            top_border = chars["top_left"] + chars["horizontal"] * width + chars["top_right"]
            bottom_border = chars["bottom_left"] + chars["horizontal"] * width + chars["bottom_right"]
            return top_border, bottom_border, []

    def _create_layout(self):
        """Create layout using Rich's box system for perfect borders."""

        content_width, content_height = self._calculate_box_dimensions()

        # Get Rich-rendered borders
        top_border, bottom_border, middle_template = self._render_rich_panel_borders(
            content_width, content_height
        )

        # Create buffer control
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Create text window
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            width=Dimension(min=content_width, max=content_width, preferred=content_width),
            height=Dimension(min=content_height, max=content_height, preferred=content_height),
            ignore_content_width=True,
            ignore_content_height=True,
            scroll_offsets=ScrollOffsets(left=0, right=0, top=0, bottom=0),
            left_margins=[ConditionalMargin(
                margin=NumberedMargin(display_tildes=False),
                filter=Condition(lambda: self.show_line_numbers)
            )] if self.show_line_numbers else []
        )

        # Extract characters from Rich box
        chars = self._extract_rich_box_characters()

        # Create layout components using Rich's calculated borders

        # Top border (from Rich rendering)
        top_border_window = Window(
            content=FormattedTextControl(lambda: top_border),
            height=1,
            style='class:rich-box-border'
        )

        # Middle section with Rich-style borders
        middle_section = VSplit([
            # Left border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([chars["vertical"]] * content_height)
                ),
                width=1,
                style='class:rich-box-border'
            ),
            # Text area
            text_window,
            # Right border
            Window(
                content=FormattedTextControl(
                    lambda: "\n".join([chars["vertical"]] * content_height)
                ),
                width=1,
                style='class:rich-box-border'
            )
        ], padding=0)

        # Bottom border (from Rich rendering)
        bottom_border_window = Window(
            content=FormattedTextControl(lambda: bottom_border),
            height=1,
            style='class:rich-box-border'
        )

        # Assemble layout
        layout_components = [
            top_border_window,
            middle_section,
            bottom_border_window
        ]

        # Optional status bar
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
            layout_components.append(status_window)

        # Create final layout
        self.layout = Layout(HSplit(layout_components))

    def _create_style(self):
        """Create styling with Rich-compatible box styles."""
        base_style = super()._create_style()
        base_dict = dict(base_style.style_rules)

        # Rich box styles
        rich_box_styles = {
            'rich-box-border': '#888888',  # Consistent with Rich's default
            'status': 'reverse',
        }

        return Style.from_dict({**base_dict, **rich_box_styles})


# Convenience function
def rich_box_vim_input(prompt="",
                      initial_text="",
                      placeholder_text="",
                      show_line_numbers=False,
                      show_status=True,
                      wrap_lines=True,
                      box_width=60,
                      box_height=10,
                      box_title="",
                      rich_box_style="ROUNDED",
                      auto_size=True):
    """
    Create vim input using Rich's built-in box system.

    Args:
        prompt: Prompt text
        initial_text: Pre-populated text
        placeholder_text: Placeholder when empty
        show_line_numbers: Show line numbers
        show_status: Show vim mode status
        wrap_lines: Wrap long lines
        box_width: Box width
        box_height: Box height
        box_title: Title in box border
        rich_box_style: Rich box style (ROUNDED, SQUARE, DOUBLE, HEAVY, etc.)
        auto_size: Auto-size to terminal

    Returns:
        str: Edited text or None if cancelled
    """
    readline = RichBoxVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        box_width=box_width,
        box_height=box_height,
        box_title=box_title,
        rich_box_style=rich_box_style,
        auto_size=auto_size
    )
    return readline.run()


def demo_rich_native_direct():
    """Demo function for direct execution."""
    print("🎨 Rich-Native Box Demo (Direct Execution)")
    print("=" * 50)
    print()
    print("This demonstrates Rich's built-in box system.")
    print("For full interactive demos, use:")
    print("  python demo_rich_standalone.py")
    print("  python demo_rich_interactive_complete.py")
    print()

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich import box

        console = Console()

        # Show Rich box styles
        styles = ["ROUNDED", "SQUARE", "DOUBLE", "HEAVY"]

        for style_name in styles:
            box_style = getattr(box, style_name)
            panel = Panel(
                f"This is a {style_name} box rendered by Rich.\nPerfect alignment guaranteed!",
                title=f"{style_name} Demo",
                box=box_style,
                width=50
            )
            console.print(panel)
            console.print()

        console.print("✅ Rich-native box rendering working perfectly!")

    except ImportError as e:
        print(f"❌ Rich not available: {e}")


if __name__ == "__main__":
    demo_rich_native_direct()