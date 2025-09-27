"""
ValidatedVimReadline - extends VimReadline with input validation and hidden input support.
"""
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window, VSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor, PasswordProcessor
from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import ModalCursorShapeConfig
from typing import Optional, Union

from .validators import Validator, ValidationResult
from .core import VimReadline
from .themes import VimReadlineTheme


class ValidatedVimReadline(VimReadline):
    """
    A vim-mode readline editor with input validation and hidden input support.

    Features (in addition to VimReadline):
    - Real-time input validation with visual feedback
    - Prevents submission of invalid input
    - Hidden input mode for passwords
    - Configurable validation error display
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
                 validator: Optional[Validator] = None,
                 hidden_input=False,
                 mask_character='*',
                 show_validation_error=True,
                 validate_on_change=True,
                 theme: Optional[VimReadlineTheme] = None):

        self.validator = validator
        self.hidden_input = hidden_input
        self.mask_character = mask_character
        self.show_validation_error = show_validation_error
        self.validate_on_change = validate_on_change

        # Current validation state
        self._current_validation = ValidationResult(True)
        self._validation_message = ""

        # Initialize parent class
        super().__init__(
            initial_text=initial_text,
            placeholder_text=placeholder_text,
            prompt=prompt,
            show_line_numbers=show_line_numbers,
            show_status=show_status,
            wrap_lines=wrap_lines,
            submit_key=submit_key,
            newline_key=newline_key,
            cancel_keys=cancel_keys,
            theme=theme
        )

        # Add validation on text change if enabled
        if self.validator and self.validate_on_change:
            self.buffer.on_text_changed += self._on_text_changed

    def _on_text_changed(self, buffer):
        """Called when buffer text changes - triggers validation."""
        if self.validator:
            text = buffer.text
            # Don't validate placeholder text
            if self._is_placeholder_active and text == self.placeholder_text:
                self._current_validation = ValidationResult(True)
                self._validation_message = ""
            else:
                self._current_validation = self.validator.validate(text)
                self._validation_message = self._current_validation.error_message

    def _create_placeholder_aware_buffer_control(self, input_processors):
        """Create a simple buffer control - we'll handle styling differently."""
        return BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=input_processors
        )

    def _create_layout(self):
        """Create the layout with validation error display."""
        # Main buffer control with optional password masking
        input_processors = [HighlightMatchingBracketProcessor()]

        if self.hidden_input:
            input_processors.append(PasswordProcessor(char=self.mask_character))

        # Create custom buffer control that handles placeholder styling
        buffer_control = self._create_placeholder_aware_buffer_control(input_processors)

        # Main text window with conditional styling
        def get_text_style():
            if self._is_placeholder_active:
                return 'class:placeholder'
            return ''

        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            dont_extend_width=False,
            dont_extend_height=True,
            style=get_text_style
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

            components_left.extend([
                line_number_window,
                Window(width=1, char='│', style='class:line-number-separator')
            ])

        components_left.append(text_window)

        if len(components_left) > 1:
            content = VSplit(components_left)
        else:
            content = text_window

        # Build vertical layout components
        components = [content]

        # Optional validation error display
        if self.show_validation_error and self.validator:
            def get_validation_message():
                if not self._current_validation.is_valid and self._validation_message:
                    return f"Error: {self._validation_message}"
                return ""

            validation_window = Window(
                content=FormattedTextControl(get_validation_message),
                height=lambda: 1 if (not self._current_validation.is_valid and self._validation_message) else 0,
                style='class:validation-error'
            )
            components.append(validation_window)

        # Optional status bar
        if self.show_status:
            def get_status():
                app = self.app
                if app.vi_state.input_mode == 'vi-insert':
                    if app.vi_state.temporary_navigation_mode:
                        status = '-- (insert) --'
                    else:
                        status = '-- INSERT --'
                elif app.vi_state.input_mode == 'vi-replace':
                    status = '-- REPLACE --'
                elif app.vi_state.input_mode == 'vi-navigation':
                    selection = self.buffer.selection_state
                    if selection:
                        from prompt_toolkit.selection import SelectionType
                        if selection.type == SelectionType.LINES:
                            status = '-- VISUAL LINE --'
                        elif selection.type == SelectionType.BLOCK:
                            status = '-- VISUAL BLOCK --'
                        else:
                            status = '-- VISUAL --'
                    else:
                        status = ''
                else:
                    status = ''

                # Add validation indicator
                if self.validator and not self._current_validation.is_valid:
                    if status:
                        status += ' [INVALID]'
                    else:
                        status = '[INVALID]'

                return status

            status_window = Window(
                content=FormattedTextControl(get_status),
                height=1,
                style='class:status'
            )
            components.append(status_window)

        self.layout = Layout(HSplit(components))

    def _create_key_bindings(self):
        """Create custom key bindings with validation-aware submit."""
        kb = super()._create_key_bindings()

        # Override submit to check validation
        @kb.add(self.submit_key)
        def validated_submit(event):
            current_text = self.buffer.text

            # Check if placeholder is active and handle appropriately
            if self._is_placeholder_active and current_text == self.placeholder_text:
                current_text = ""

            # Validate before submitting
            if self.validator:
                validation_result = self.validator.validate(current_text)
                if not validation_result.is_valid:
                    # Update validation state and don't submit
                    self._current_validation = validation_result
                    self._validation_message = validation_result.error_message
                    return

            # If validation passed or no validator, submit normally
            self._result = current_text
            event.app.exit()

        return kb

    def validate_current_input(self) -> ValidationResult:
        """Manually validate the current input."""
        if not self.validator:
            return ValidationResult(True)

        current_text = self.buffer.text
        if self._is_placeholder_active and current_text == self.placeholder_text:
            current_text = ""

        return self.validator.validate(current_text)


# Convenience function for validated input
def validated_vim_input(prompt="",
                       initial_text="",
                       placeholder_text="",
                       show_line_numbers=False,
                       show_status=True,
                       wrap_lines=True,
                       validator: Optional[Validator] = None,
                       hidden_input=False,
                       mask_character='*',
                       theme: Optional[VimReadlineTheme] = None):
    """
    Simple function interface for validated vim_readline.

    Args:
        prompt: Prompt text shown at the start of each line
        initial_text: Pre-populated editable text
        placeholder_text: Hint text shown when buffer is empty
        show_line_numbers: Whether to show line numbers
        show_status: Whether to show mode status
        wrap_lines: Whether to wrap long lines
        validator: Validator instance to use for input validation
        hidden_input: Whether to mask input (for passwords)
        mask_character: Character to use for masking when hidden_input=True
        theme: VimReadlineTheme instance for custom styling

    Returns:
        str: The edited and validated text, or None if cancelled
    """
    readline = ValidatedVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        validator=validator,
        hidden_input=hidden_input,
        mask_character=mask_character,
        theme=theme
    )
    return readline.run()