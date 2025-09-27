"""
Vim-mode readline implementation based on prompt-toolkit.

A simplified vim editor interface for single-buffer text editing without file I/O.
Supports all standard vim navigation modes (normal/insert/visual) with customizable
exit behavior and optional line numbers.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import Condition, vi_insert_mode, vi_navigation_mode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor
from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig
from typing import Optional
from .themes import VimReadlineTheme, get_default_theme


class VimReadline:
    """
    A vim-mode readline editor for single buffer editing.

    Features:
    - Full vim navigation (normal/insert/visual modes)
    - Configurable submit/newline keys
    - Optional line numbers and status indicators
    - Cursor shape changes based on mode
    - Placeholder text support
    - Optional prompt display
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 prompt="",
                 show_line_numbers=False,
                 show_status=True,
                 wrap_lines=True,
                 submit_key='c-m',        # Return
                 newline_key='c-j',       # Ctrl-J (or Shift-Return on many terminals)
                 cancel_keys=None,
                 theme: Optional[VimReadlineTheme] = None):

        if cancel_keys is None:
            cancel_keys = ['c-c', 'c-d']

        self.initial_text = initial_text
        self.placeholder_text = placeholder_text
        self.prompt = prompt
        self.show_line_numbers = show_line_numbers
        self.show_status = show_status
        self.theme = theme or get_default_theme()
        self.wrap_lines = wrap_lines
        self.submit_key = submit_key
        self.newline_key = newline_key
        self.cancel_keys = cancel_keys

        # Result storage
        self._result = None
        self._cancelled = False
        self._is_placeholder_active = False

        # Initialize buffer
        self.buffer = Buffer(
            document=None,
            multiline=True,
            read_only=False
        )

        if initial_text:
            self.buffer.text = initial_text
            self.buffer.cursor_position = len(initial_text)
            self._is_placeholder_active = False
        elif placeholder_text:
            # Set placeholder as initial text but mark it as placeholder
            self.buffer.text = placeholder_text
            self.buffer.cursor_position = 0
            self._is_placeholder_active = True
        else:
            self._is_placeholder_active = False

        # Create layout
        self._create_layout()

        # Create application
        self.app = Application(
            layout=self.layout,
            editing_mode=EditingMode.VI,
            key_bindings=self._create_key_bindings(),
            style=self._create_style(),
            cursor=ModalCursorShapeConfig(),
            full_screen=False,
            mouse_support=True
        )

    def _create_layout(self):
        """Create the layout with optional prompt, line numbers and status bar."""

        # Main buffer control (simplified without custom placeholder processor)
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Main text window
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            dont_extend_width=False,
            dont_extend_height=True
        )

        # Optional prompt
        components_left = []
        if self.prompt:
            prompt_window = Window(
                content=FormattedTextControl(lambda: self.prompt),
                width=len(self.prompt),
                dont_extend_width=True,
                style='class:prompt'
            )
            components_left.append(prompt_window)

        # Optional line numbers
        if self.show_line_numbers:
            def get_line_numbers():
                doc = self.buffer.document
                line_count = doc.line_count
                width = len(str(line_count))

                lines = []
                for i in range(line_count):
                    line_num = str(i + 1).rjust(width)
                    lines.append(('class:line-number', f'{line_num} '))

                return '\n'.join([line[1] for line in lines])

            line_number_window = Window(
                content=FormattedTextControl(get_line_numbers),
                width=lambda: len(str(self.buffer.document.line_count)) + 1,
                dont_extend_width=True,
                style='class:line-number'
            )

            from prompt_toolkit.layout.containers import VSplit
            components_left.extend([
                line_number_window,
                Window(width=1, char='│', style='class:line-number-separator')
            ])

        components_left.append(text_window)

        if len(components_left) > 1:
            from prompt_toolkit.layout.containers import VSplit
            content = VSplit(components_left)
        else:
            content = text_window

        # Optional status bar
        components = [content]

        if self.show_status:
            def get_status():
                app = self.app
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
            components.append(status_window)

        self.layout = Layout(HSplit(components))

    def _create_key_bindings(self):
        """Create custom key bindings."""
        kb = KeyBindings()

        # Create a filter for placeholder state
        @Condition
        def placeholder_active():
            return self._is_placeholder_active

        # Clear placeholder on common editing keys
        placeholder_clearing_keys = [
            # Insert mode entries
            'i', 'a', 'o', 'I', 'A', 'O', 's', 'S', 'c-i',
            # Editing keys
            'backspace', 'delete', 'c-h',
            # Common printable characters
            'space'
        ]

        for key in placeholder_clearing_keys:
            def make_placeholder_clearer(k):
                @kb.add(k, filter=placeholder_active)
                def clear_placeholder(event):
                    if self._is_placeholder_active:
                        self.buffer.text = ''
                        self.buffer.cursor_position = 0
                        self._is_placeholder_active = False
                    # Don't consume the event - let default handling proceed
                    return False
                return clear_placeholder

            make_placeholder_clearer(key)

        # Clear placeholder on printable characters (a-z, A-Z, 0-9, common symbols)
        import string
        for char in string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?/`~"\'':
            def make_char_clearer(c):
                @kb.add(c, filter=placeholder_active)
                def clear_placeholder_char(event):
                    if self._is_placeholder_active:
                        self.buffer.text = ''
                        self.buffer.cursor_position = 0
                        self._is_placeholder_active = False
                        # Insert the typed character
                        self.buffer.insert_text(c)
                    return True  # Consume the event
                return clear_placeholder_char

            make_char_clearer(char)

        # Submit with Return key
        @kb.add(self.submit_key)
        def submit(event):
            self._result = self.buffer.text
            event.app.exit()

        # Insert newline with Ctrl-J (Shift-Return maps to this on many terminals)
        @kb.add(self.newline_key)
        def insert_newline(event):
            event.current_buffer.insert_text('\n')


        # Cancel keys
        for cancel_key in self.cancel_keys:
            @kb.add(cancel_key)
            def cancel(event):
                self._cancelled = True
                event.app.exit()

        return kb

    def _create_style(self):
        """Create styling for the interface using centralized theme."""
        return self.theme.get_prompt_toolkit_style()

    def run(self):
        """
        Run the vim readline interface.

        Returns:
            str: The edited text, or None if cancelled
        """
        self._result = None
        self._cancelled = False

        try:
            self.app.run()
        except (KeyboardInterrupt, EOFError):
            self._cancelled = True

        if self._cancelled:
            return None

        # If placeholder was active and never cleared, return empty string
        result_text = self._result if self._result is not None else self.buffer.text
        if self._is_placeholder_active and result_text == self.placeholder_text:
            return ""

        return result_text


# Convenience function
def vim_input(prompt="",
              initial_text="",
              placeholder_text="",
              show_line_numbers=False,
              show_status=True,
              wrap_lines=True):
    """
    Simple function interface for vim_readline.

    Args:
        prompt: Prompt text shown at the start of each line (e.g. ">>> ")
        initial_text: Pre-populated editable text
        placeholder_text: Hint text shown when buffer is empty
        show_line_numbers: Whether to show line numbers
        show_status: Whether to show mode status
        wrap_lines: Whether to wrap long lines

    Returns:
        str: The edited text, or None if cancelled
    """
    readline = VimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines
    )
    return readline.run()