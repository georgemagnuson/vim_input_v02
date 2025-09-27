"""
Box-constrained VimReadline implementation with proper text boundary control.

This module provides a VimReadline that properly constrains text within defined boundaries,
similar to pyvim's window management system but for single-buffer editing.
"""

from .core import VimReadline as BaseVimReadline
from prompt_toolkit.layout.containers import HSplit, VSplit, Window, ScrollOffsets
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.margins import NumberedMargin, ConditionalMargin
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor
from prompt_toolkit.styles import Style
import os


class BoxConstrainedVimReadline(BaseVimReadline):
    """
    VimReadline with proper text boundary constraints using pyvim-style window management.

    Features:
    - Text is properly constrained within defined box boundaries
    - Configurable box dimensions (width/height)
    - Internal padding creates the "box" effect
    - Text wrapping respects box boundaries
    - Scrolling when content exceeds box size
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
                 # Box constraint options
                 box_width=None,      # None = use terminal width - padding
                 box_height=None,     # None = use terminal height - padding
                 box_padding_left=2,
                 box_padding_right=2,
                 box_padding_top=1,
                 box_padding_bottom=1,
                 show_box_border=True,
                 border_char='│'):

        # Store box parameters
        self.box_width = box_width
        self.box_height = box_height
        self.box_padding_left = box_padding_left
        self.box_padding_right = box_padding_right
        self.box_padding_top = box_padding_top
        self.box_padding_bottom = box_padding_bottom
        self.show_box_border = show_box_border
        self.border_char = border_char

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
        """Calculate the actual box dimensions based on terminal size and settings."""
        terminal_width, terminal_height = self._get_terminal_size()

        # Calculate available space for content (inside the box)
        if self.box_width is None:
            # Auto-calculate based on terminal width
            content_width = terminal_width - self.box_padding_left - self.box_padding_right
            if self.show_box_border:
                content_width -= 2  # Account for left/right borders
        else:
            content_width = self.box_width

        if self.box_height is None:
            # Auto-calculate based on terminal height, reserving space for status/prompts
            content_height = terminal_height - self.box_padding_top - self.box_padding_bottom - 3  # reserve for status
            if self.show_box_border:
                content_height -= 2  # Account for top/bottom borders
        else:
            content_height = self.box_height

        return max(10, content_width), max(3, content_height)  # minimum sizes

    def _create_layout(self):
        """Create a box-constrained layout using pyvim-style window management."""

        content_width, content_height = self._calculate_box_dimensions()

        # Create constrained buffer control (similar to pyvim's approach)
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Create the constrained text window (KEY DIFFERENCE from base class)
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            # CONSTRAIN the window size (this is what was missing!)
            width=Dimension(min=content_width, max=content_width, preferred=content_width),
            height=Dimension(min=content_height, max=content_height, preferred=content_height),
            # Use pyvim-style settings for proper constraint behavior
            ignore_content_width=True,   # Let the container control width
            ignore_content_height=True,  # Let the container control height
            # Add scroll offsets to create internal "box" padding
            scroll_offsets=ScrollOffsets(
                left=1, right=1,
                top=0, bottom=0
            ),
            # Optional line numbers as left margin (like pyvim)
            left_margins=[ConditionalMargin(
                margin=NumberedMargin(display_tildes=False),
                filter=Condition(lambda: self.show_line_numbers)
            )] if self.show_line_numbers else []
        )

        # Build the layout components
        content_components = []

        # Optional top border
        if self.show_box_border:
            top_border_char = '─'
            top_border = Window(
                content=FormattedTextControl(lambda: '┌' + top_border_char * content_width + '┐'),
                height=1,
                style='class:box-border'
            )
            content_components.append(top_border)

        # Main content area with side borders
        if self.show_box_border:
            # Create content with left and right borders
            content_with_borders = VSplit([
                # Left border
                Window(
                    content=FormattedTextControl(lambda: self.border_char),
                    width=1,
                    style='class:box-border'
                ),
                # Main text area
                text_window,
                # Right border
                Window(
                    content=FormattedTextControl(lambda: self.border_char),
                    width=1,
                    style='class:box-border'
                )
            ])
            content_components.append(content_with_borders)
        else:
            content_components.append(text_window)

        # Optional bottom border
        if self.show_box_border:
            bottom_border_char = '─'
            bottom_border = Window(
                content=FormattedTextControl(lambda: '└' + bottom_border_char * content_width + '┘'),
                height=1,
                style='class:box-border'
            )
            content_components.append(bottom_border)

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
            content_components.append(status_window)

        # Create the final layout
        from prompt_toolkit.layout.layout import Layout
        self.layout = Layout(HSplit(content_components))

    def _create_style(self):
        """Create styling with box border styles."""
        base_style = super()._create_style()

        # Convert base style rules (list of tuples) to dict, then add box-specific styles
        base_dict = dict(base_style.style_rules)

        # Add box-specific styles
        box_styles = {
            'box-border': '#666666',
            'status': 'reverse',
        }

        # Merge and create new style
        return Style.from_dict({**base_dict, **box_styles})


# Convenience function
def box_constrained_vim_input(prompt="",
                             initial_text="",
                             placeholder_text="",
                             show_line_numbers=False,
                             show_status=True,
                             wrap_lines=True,
                             box_width=None,
                             box_height=None,
                             show_box_border=True):
    """
    Simple function interface for box-constrained vim_readline.

    Args:
        prompt: Prompt text shown at the start of each line
        initial_text: Pre-populated editable text
        placeholder_text: Hint text shown when buffer is empty
        show_line_numbers: Whether to show line numbers
        show_status: Whether to show mode status
        wrap_lines: Whether to wrap long lines
        box_width: Fixed width for text area (None = auto)
        box_height: Fixed height for text area (None = auto)
        show_box_border: Whether to draw box borders

    Returns:
        str: The edited text, or None if cancelled
    """
    readline = BoxConstrainedVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        box_width=box_width,
        box_height=box_height,
        show_box_border=show_box_border
    )
    return readline.run()