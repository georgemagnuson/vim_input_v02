"""
ValidatedRichVimReadline - combines Rich box styling with input validation.

Features:
- Inherits from ValidatedVimReadline for validation functionality
- Rich box styling with borders and titles
- State-based border coloring (blue=active, green=valid, red=invalid)
- Validation messages displayed in bottom border (right-aligned)
- Validation occurs on exit/submit, not real-time (prevents bounceback)
- Customizable theme colors for different states
"""

from typing import Optional, Dict, Any
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor, PasswordProcessor
from prompt_toolkit.styles import Style
from rich.box import ROUNDED, SQUARE, DOUBLE, HEAVY
import io

from .validated import ValidatedVimReadline
from .validators import Validator, ValidationResult
from .themes import VimReadlineTheme


class ValidatedRichTheme:
    """Theme configuration for ValidatedRichVimReadline state-based coloring."""

    def __init__(self,
                 border_active: str = "blue",
                 border_valid: str = "green",
                 border_invalid: str = "red",
                 border_title_active: str = "blue",
                 border_title_valid: str = "green",
                 border_title_invalid: str = "red",
                 validation_message_valid: str = "green",
                 validation_message_invalid: str = "red"):
        self.border_active = border_active
        self.border_valid = border_valid
        self.border_invalid = border_invalid
        self.border_title_active = border_title_active
        self.border_title_valid = border_title_valid
        self.border_title_invalid = border_title_invalid
        self.validation_message_valid = validation_message_valid
        self.validation_message_invalid = validation_message_invalid


class ValidatedRichVimReadline(ValidatedVimReadline):
    """
    Rich-styled VimReadline with input validation and state-based theming.

    Features:
    - Rich box styling with customizable borders
    - State-based border coloring (active/valid/invalid)
    - Validation messages in bottom border (right-aligned)
    - Validation on exit/submit (not real-time)
    - Customizable theme configuration
    - Hidden input support for passwords
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
                 # Validation options
                 validator: Optional[Validator] = None,
                 hidden_input=False,
                 mask_character='*',
                 validate_on_exit=True,  # Validate on exit, not real-time
                 # Rich styling options
                 panel_title="vim input",
                 panel_box_style="rounded",  # "rounded", "square", "double", "heavy"
                 show_rules=False,  # Disabled by default for cleaner look
                 # Theme configuration
                 theme: Optional[ValidatedRichTheme] = None,
                 # Centralized theme system
                 base_theme: Optional[VimReadlineTheme] = None):

        # Rich options
        self.panel_title = panel_title
        self.panel_box_style = panel_box_style
        self.show_rules = show_rules
        self.validate_on_exit = validate_on_exit

        # Theme configuration
        self.theme = theme or ValidatedRichTheme()

        # Box style mapping
        self.box_styles = {
            "rounded": ROUNDED,
            "square": SQUARE,
            "double": DOUBLE,
            "heavy": HEAVY
        }

        # Validation state tracking
        self._validation_state = "active"  # "active", "valid", "invalid"
        self._validation_message = ""
        self._has_been_validated = False

        # Initialize parent ValidatedVimReadline
        # Disable real-time validation since we validate on exit
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
            validator=validator,
            hidden_input=hidden_input,
            mask_character=mask_character,
            show_validation_error=False,  # We handle validation display ourselves
            validate_on_change=False,  # Disable real-time validation
            theme=base_theme
        )

    def _get_current_border_color(self):
        """Get the current border color based on validation state."""
        if self._validation_state == "valid":
            return self.theme.border_valid
        elif self._validation_state == "invalid":
            return self.theme.border_invalid
        else:  # active
            return self.theme.border_active

    def _get_current_title_color(self):
        """Get the current title color based on validation state."""
        if self._validation_state == "valid":
            return self.theme.border_title_valid
        elif self._validation_state == "invalid":
            return self.theme.border_title_invalid
        else:  # active
            return self.theme.border_title_active

    def _get_box_characters(self):
        """Get the appropriate box drawing characters for the selected style."""
        box_style = self.box_styles.get(self.panel_box_style, ROUNDED)

        # Map Rich box styles to Unicode box drawing characters
        if box_style == ROUNDED:
            return {
                'top_left': '╭',
                'top_right': '╮',
                'bottom_left': '╰',
                'bottom_right': '╯',
                'horizontal': '─',
                'vertical': '│'
            }
        elif box_style == SQUARE:
            return {
                'top_left': '┌',
                'top_right': '┐',
                'bottom_left': '└',
                'bottom_right': '┘',
                'horizontal': '─',
                'vertical': '│'
            }
        elif box_style == DOUBLE:
            return {
                'top_left': '╔',
                'top_right': '╗',
                'bottom_left': '╚',
                'bottom_right': '╝',
                'horizontal': '═',
                'vertical': '║'
            }
        elif box_style == HEAVY:
            return {
                'top_left': '┏',
                'top_right': '┓',
                'bottom_left': '┗',
                'bottom_right': '┛',
                'horizontal': '━',
                'vertical': '┃'
            }
        else:
            # Fallback to square
            return {
                'top_left': '┌',
                'top_right': '┐',
                'bottom_left': '└',
                'bottom_right': '┘',
                'horizontal': '─',
                'vertical': '│'
            }

    def _create_top_border_line(self, box_chars):
        """Create the top border line with title and state-based coloring."""
        def get_top_border():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80

            available_width = max(terminal_width - 4, 36)

            if self.panel_title:
                title = f" {self.panel_title} "
                title_len = len(title)
                if title_len + 2 < available_width:
                    remaining_width = available_width - title_len - 2
                    left_padding = 1
                    right_padding = remaining_width - left_padding

                    # Apply state-based coloring using FormattedText
                    border_color = self._get_current_border_color()
                    title_color = self._get_current_title_color()

                    return [
                        (f'class:border-{self._validation_state}', box_chars['top_left']),
                        (f'class:border-{self._validation_state}', box_chars['horizontal'] * left_padding),
                        (f'class:title-{self._validation_state}', title),
                        (f'class:border-{self._validation_state}', box_chars['horizontal'] * right_padding),
                        (f'class:border-{self._validation_state}', box_chars['top_right'])
                    ]
                else:
                    # Title too long, truncate
                    truncated_title = f" {self.panel_title[:available_width-6]}... "
                    return [
                        (f'class:border-{self._validation_state}', box_chars['top_left']),
                        (f'class:title-{self._validation_state}', truncated_title),
                        (f'class:border-{self._validation_state}', box_chars['top_right'])
                    ]
            else:
                return [
                    (f'class:border-{self._validation_state}', box_chars['top_left']),
                    (f'class:border-{self._validation_state}', box_chars['horizontal'] * available_width),
                    (f'class:border-{self._validation_state}', box_chars['top_right'])
                ]

        return get_top_border

    def _create_bottom_border_line(self, box_chars):
        """Create the bottom border line with validation message (right-aligned)."""
        def get_bottom_border():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80

            available_width = max(terminal_width - 4, 36)

            # Get validation message if any
            if self._validation_message and self._has_been_validated:
                message = f" {self._validation_message} "
                message_len = len(message)

                if message_len + 2 < available_width:
                    # Right-align the message
                    left_padding = available_width - message_len - 2

                    # Color based on validation state
                    message_color = (self.theme.validation_message_valid
                                   if self._validation_state == "valid"
                                   else self.theme.validation_message_invalid)

                    return [
                        (f'class:border-{self._validation_state}', box_chars['bottom_left']),
                        (f'class:border-{self._validation_state}', box_chars['horizontal'] * left_padding),
                        (f'class:validation-message-{self._validation_state}', message),
                        (f'class:border-{self._validation_state}', box_chars['bottom_right'])
                    ]
                else:
                    # Message too long, truncate and still right-align
                    truncated_message = f" ...{self._validation_message[-(available_width-8):]} "
                    return [
                        (f'class:border-{self._validation_state}', box_chars['bottom_left']),
                        (f'class:validation-message-{self._validation_state}', truncated_message),
                        (f'class:border-{self._validation_state}', box_chars['bottom_right'])
                    ]
            else:
                # No message, just plain border
                return [
                    (f'class:border-{self._validation_state}', box_chars['bottom_left']),
                    (f'class:border-{self._validation_state}', box_chars['horizontal'] * available_width),
                    (f'class:border-{self._validation_state}', box_chars['bottom_right'])
                ]

        return get_bottom_border

    def _create_layout(self):
        """Create Rich-enhanced layout with validation state coloring."""
        # Get box characters for the selected style
        box_chars = self._get_box_characters()

        # Create components list
        components = []

        # Top border with title and state coloring
        top_border_window = Window(
            content=FormattedTextControl(self._create_top_border_line(box_chars)),
            height=1
        )
        components.append(top_border_window)

        # Middle section with side borders and content
        input_processors = [HighlightMatchingBracketProcessor()]
        if self.hidden_input:
            input_processors.append(PasswordProcessor(char=self.mask_character))

        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=input_processors
        )

        # Build the content area
        content_components = []

        # Left border
        content_components.append(Window(
            content=FormattedTextControl(lambda: [(f'class:border-{self._validation_state}', box_chars['vertical'])]),
            width=1
        ))

        # Optional prompt
        if self.prompt:
            content_components.append(Window(
                content=FormattedTextControl(lambda: self.prompt),
                width=len(self.prompt),
                style='class:prompt'
            ))

        # Optional line numbers
        if self.show_line_numbers:
            def get_line_numbers():
                doc = self.buffer.document
                line_count = max(doc.line_count, 1)
                width = len(str(line_count))

                lines = []
                for i in range(line_count):
                    line_num = str(i + 1).rjust(width)
                    lines.append(f'{line_num} ')

                return '\n'.join(lines)

            content_components.append(Window(
                content=FormattedTextControl(get_line_numbers),
                width=lambda: len(str(max(self.buffer.document.line_count, 1))) + 1,
                style='class:line-number'
            ))

            # Line number separator
            content_components.append(Window(
                content=FormattedTextControl(lambda: '│'),
                width=1,
                style='class:line-number-separator'
            ))

        # Main text input area
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            dont_extend_width=False
        )
        content_components.append(text_window)

        # Right border
        content_components.append(Window(
            content=FormattedTextControl(lambda: [(f'class:border-{self._validation_state}', box_chars['vertical'])]),
            width=1
        ))

        # Create middle content with width constraint
        def get_box_width():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80
            return max(terminal_width - 2, 40)

        middle_content = VSplit(content_components)
        components.append(middle_content)

        # Bottom border with validation message
        bottom_border_window = Window(
            content=FormattedTextControl(self._create_bottom_border_line(box_chars)),
            height=1
        )
        components.append(bottom_border_window)

        # Status bar
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

    def _perform_validation(self, text: str) -> ValidationResult:
        """Perform validation and update state."""
        if not self.validator:
            self._validation_state = "valid"
            self._validation_message = ""
            self._has_been_validated = True
            return ValidationResult(True)

        # Check if placeholder is active
        if self._is_placeholder_active and text == self.placeholder_text:
            text = ""

        result = self.validator.validate(text)
        self._has_been_validated = True

        if result.is_valid:
            self._validation_state = "valid"
            self._validation_message = "Valid"
        else:
            self._validation_state = "invalid"
            self._validation_message = result.error_message

        return result

    def _create_key_bindings(self):
        """Create key bindings with validation on submit."""
        kb = super()._create_key_bindings()

        # Override submit to validate on exit
        @kb.add(self.submit_key)
        def validated_submit(event):
            current_text = self.buffer.text

            # Handle placeholder
            if self._is_placeholder_active and current_text == self.placeholder_text:
                current_text = ""

            # Perform validation
            if self.validate_on_exit and self.validator:
                validation_result = self._perform_validation(current_text)
                if not validation_result.is_valid:
                    # Don't submit if invalid - just update display
                    return

            # If validation passed or no validator, submit
            self._result = current_text
            event.app.exit()

        return kb

    def _create_style(self):
        """Create styling with state-based border colors."""
        base_style_dict = {
            'prompt': 'bold',
            'line-number': '#666666',
            'line-number-separator': '#666666',
            'status': 'reverse',
            'placeholder': '#555555 italic',
        }

        # State-based border styles
        state_styles = {
            # Active state (blue)
            'border-active': self.theme.border_active,
            'title-active': f'bold {self.theme.border_title_active}',
            'validation-message-active': self.theme.border_active,

            # Valid state (green)
            'border-valid': self.theme.border_valid,
            'title-valid': f'bold {self.theme.border_title_valid}',
            'validation-message-valid': f'bold {self.theme.validation_message_valid}',

            # Invalid state (red)
            'border-invalid': self.theme.border_invalid,
            'title-invalid': f'bold {self.theme.border_title_invalid}',
            'validation-message-invalid': f'bold {self.theme.validation_message_invalid}',
        }

        return Style.from_dict({**base_style_dict, **state_styles})


# Convenience function for ValidatedRichVimReadline
def validated_rich_vim_input(prompt="",
                           initial_text="",
                           placeholder_text="",
                           show_line_numbers=False,
                           show_status=True,
                           wrap_lines=True,
                           validator: Optional[Validator] = None,
                           hidden_input=False,
                           mask_character='*',
                           panel_title="vim input",
                           panel_box_style="rounded",
                           theme: Optional[ValidatedRichTheme] = None):
    """
    Rich-styled vim input with validation.

    Args:
        prompt: Prompt text
        initial_text: Pre-populated text
        placeholder_text: Placeholder hint
        show_line_numbers: Show line numbers
        show_status: Show vim mode status
        wrap_lines: Enable line wrapping
        validator: Validator instance for input validation
        hidden_input: Hide input for passwords
        mask_character: Character for masking hidden input
        panel_title: Title for the Rich panel
        panel_box_style: Box style ("rounded", "square", "double", "heavy")
        theme: ValidatedRichTheme for customizing colors

    Returns:
        str: Edited and validated text, or None if cancelled
    """
    readline = ValidatedRichVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        validator=validator,
        hidden_input=hidden_input,
        mask_character=mask_character,
        panel_title=panel_title,
        panel_box_style=panel_box_style,
        theme=theme
    )
    return readline.run()