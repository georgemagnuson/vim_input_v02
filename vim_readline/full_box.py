"""
Full Box VimReadline implementation that draws complete borders like the screenshot.

This creates a true boxed input area with complete borders on all sides,
similar to the "Type entry" box shown in the screenshot.
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
import os


class FullBoxVimReadline(BaseVimReadline):
    """
    VimReadline that draws a complete box around the text area, exactly like the screenshot.

    Creates a bordered input area with:
    - Top border: ┌─────────────┐
    - Side borders: │ text area │
    - Bottom border: └─────────────┘
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
                 # Box appearance options
                 box_width=60,        # Default width
                 box_height=10,       # Default height
                 box_title="",        # Title shown in top border
                 border_style="rounded",  # "rounded", "square", "double", "heavy"
                 auto_size=True):     # Auto-size to terminal

        # Store box configuration
        self.box_width = box_width
        self.box_height = box_height
        self.box_title = box_title
        self.border_style = border_style
        self.auto_size = auto_size

        # Border character sets
        self.border_chars = {
            "rounded": {
                "top_left": "┌", "top_right": "┐",
                "bottom_left": "└", "bottom_right": "┘",
                "horizontal": "─", "vertical": "│"
            },
            "square": {
                "top_left": "┌", "top_right": "┐",
                "bottom_left": "└", "bottom_right": "┘",
                "horizontal": "─", "vertical": "│"
            },
            "double": {
                "top_left": "╔", "top_right": "╗",
                "bottom_left": "╚", "bottom_right": "╝",
                "horizontal": "═", "vertical": "║"
            },
            "heavy": {
                "top_left": "┏", "top_right": "┓",
                "bottom_left": "┗", "bottom_right": "┛",
                "horizontal": "━", "vertical": "┃"
            }
        }

        # Initialize parent (this will call our overridden _create_layout)
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
        """Calculate the actual box dimensions."""
        if self.auto_size:
            terminal_width, terminal_height = self._get_terminal_size()
            # Leave some margin around the box
            content_width = min(self.box_width, terminal_width - 4)
            content_height = min(self.box_height, terminal_height - 6)
        else:
            content_width = self.box_width
            content_height = self.box_height

        # Ensure minimum sizes
        return max(20, content_width), max(5, content_height)

    def _get_border_line(self, line_type, width):
        """Generate a border line of the specified type and width."""
        chars = self.border_chars[self.border_style]

        if line_type == "top":
            if self.box_title:
                # Calculate title positioning
                title_text = f" {self.box_title} "
                remaining_width = width - len(title_text)
                if remaining_width >= 2:
                    left_pad = remaining_width // 2
                    right_pad = remaining_width - left_pad
                    return chars["top_left"] + chars["horizontal"] * left_pad + title_text + chars["horizontal"] * right_pad + chars["top_right"]

            # No title or not enough space
            return chars["top_left"] + chars["horizontal"] * width + chars["top_right"]

        elif line_type == "bottom":
            return chars["bottom_left"] + chars["horizontal"] * width + chars["bottom_right"]

    def _create_layout(self):
        """Create a layout with a complete drawn box around the text area."""

        content_width, content_height = self._calculate_box_dimensions()
        chars = self.border_chars[self.border_style]

        # Create the main buffer control
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Calculate the exact text area width (accounting for borders)
        text_area_width = content_width  # This is the inner content width we want

        # Create the text window (constrained to fit inside the box)
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            # The text area width should match exactly what fits between borders
            width=Dimension(min=text_area_width, max=text_area_width, preferred=text_area_width),
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

        # CREATE THE COMPLETE BOX STRUCTURE USING HSplit/VSplit
        # This creates a reliable complete box without FloatContainer complexity

        # Calculate total box width (borders + content)
        total_box_width = content_width + 2  # +2 for left and right borders

        # Top border
        top_border = Window(
            content=FormattedTextControl(lambda: self._get_border_line("top", content_width)),
            height=1,
            width=Dimension(min=total_box_width, max=total_box_width, preferred=total_box_width),
            style='class:box-border'
        )

        # Middle section with complete side borders and the text area
        def create_bordered_line(line_index):
            """Create a function that returns a bordered line for a specific line index."""
            def get_bordered_content():
                # Get the text line for this specific index
                doc = self.buffer.document
                lines = doc.lines

                if line_index < len(lines):
                    line_text = lines[line_index]
                else:
                    line_text = ""

                # Truncate or pad the line to fit within the box
                inner_width = content_width
                if len(line_text) > inner_width:
                    line_text = line_text[:inner_width]
                else:
                    line_text = line_text.ljust(inner_width)

                return chars["vertical"] + line_text + chars["vertical"]

            return get_bordered_content

        # Create middle section with complete borders for each line
        middle_rows = []
        for i in range(content_height):
            line_window = Window(
                content=FormattedTextControl(create_bordered_line(i)),
                height=1,
                style='class:box-border'
            )
            middle_rows.append(line_window)

        # Bottom border
        bottom_border = Window(
            content=FormattedTextControl(lambda: self._get_border_line("bottom", content_width)),
            height=1,
            width=Dimension(min=total_box_width, max=total_box_width, preferred=total_box_width),
            style='class:box-border'
        )

        # For now, let's use the simpler approach with just the text window
        # and create a visual box around it using VSplit structure

        # Create the middle section with proper width alignment
        middle_section = VSplit([
            # Left border column - exactly 1 character wide
            Window(
                content=FormattedTextControl(lambda: "\n".join([chars["vertical"]] * content_height)),
                width=Dimension(min=1, max=1, preferred=1),
                style='class:box-border'
            ),
            # Text area - exact width to fit content
            text_window,
            # Right border column - exactly 1 character wide
            Window(
                content=FormattedTextControl(lambda: "\n".join([chars["vertical"]] * content_height)),
                width=Dimension(min=1, max=1, preferred=1),
                style='class:box-border'
            )
        ],
        padding=0,  # No padding between elements
        width=Dimension(min=total_box_width, max=total_box_width, preferred=total_box_width)
        )

        # Assemble the complete layout
        layout_components = [
            top_border,
            middle_section,
            bottom_border
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
            layout_components.append(status_window)

        # Create the final layout
        self.layout = Layout(HSplit(layout_components))

    def _create_style(self):
        """Create styling with enhanced box border styles."""
        base_style = super()._create_style()
        base_dict = dict(base_style.style_rules)

        # Enhanced box styles
        box_styles = {
            'box-border': '#888888',  # Lighter gray for borders
            'status': 'reverse',
        }

        return Style.from_dict({**base_dict, **box_styles})


# Convenience function
def full_box_vim_input(prompt="",
                      initial_text="",
                      placeholder_text="",
                      show_line_numbers=False,
                      show_status=True,
                      wrap_lines=True,
                      box_width=60,
                      box_height=10,
                      box_title="",
                      border_style="rounded",
                      auto_size=True):
    """
    Create a vim input with a complete drawn box around it, like the screenshot.

    Args:
        prompt: Prompt text (shown inside the box)
        initial_text: Pre-populated text
        placeholder_text: Placeholder when empty
        show_line_numbers: Show line numbers inside the box
        show_status: Show vim mode status below the box
        wrap_lines: Wrap long lines within the box
        box_width: Width of the box (auto-sized if auto_size=True)
        box_height: Height of the text area inside the box
        box_title: Title shown in the top border
        border_style: "rounded", "square", "double", or "heavy"
        auto_size: Auto-size to fit terminal

    Returns:
        str: The edited text, or None if cancelled
    """
    readline = FullBoxVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        box_width=box_width,
        box_height=box_height,
        box_title=box_title,
        border_style=border_style,
        auto_size=auto_size
    )
    return readline.run()