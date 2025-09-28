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
                 # Mode display options
                 show_mode_in_border=True,  # Show vim mode in bottom border
                 mode_style="initial",  # "initial" (I/V/N), "full" (INSERT/VISUAL/NORMAL), "none"
                 # Centralized theme system
                 theme: Optional[VimReadlineTheme] = None):

        # Rich options
        self.panel_title = panel_title
        self.panel_box_style = panel_box_style
        self.show_rules = show_rules
        self.validate_on_exit = validate_on_exit
        self.show_mode_in_border = show_mode_in_border
        self.mode_style = mode_style

        # Import default theme if none provided
        from .themes import get_default_theme
        self.theme = theme or get_default_theme()

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
            show_status=False,  # Disable regular status line - we'll show mode in border
            wrap_lines=wrap_lines,
            submit_key=submit_key,
            newline_key=newline_key,
            cancel_keys=cancel_keys,
            validator=validator,
            hidden_input=hidden_input,
            mask_character=mask_character,
            show_validation_error=False,  # We handle validation display ourselves
            validate_on_change=False,  # Disable real-time validation
            theme=self.theme
        )

    def _get_current_border_color(self):
        """Get the current border color based on validation state."""
        if self._validation_state == "valid":
            return self.theme.get_color('border-valid', 'green')
        elif self._validation_state == "invalid":
            return self.theme.get_color('border-invalid', 'red')
        else:  # active
            return self.theme.get_color('border-active', 'blue')

    def _get_current_title_color(self):
        """Get the current title color based on validation state."""
        if self._validation_state == "valid":
            return self.theme.get_color('border-title-valid', 'green')
        elif self._validation_state == "invalid":
            return self.theme.get_color('border-title-invalid', 'red')
        else:  # active
            return self.theme.get_color('border-title-active', 'blue')

    def _get_current_mode(self):
        """Get the current vim mode string for display."""
        if not self.show_mode_in_border or self.mode_style == "none":
            return ""

        try:
            app = self.app
            if app.vi_state.input_mode == 'vi-insert':
                if app.vi_state.temporary_navigation_mode:
                    mode = "INSERT" if self.mode_style == "full" else "I"
                else:
                    mode = "INSERT" if self.mode_style == "full" else "I"
            elif app.vi_state.input_mode == 'vi-replace':
                mode = "REPLACE" if self.mode_style == "full" else "R"
            elif app.vi_state.input_mode == 'vi-navigation':
                selection = self.buffer.selection_state
                if selection:
                    from prompt_toolkit.selection import SelectionType
                    if selection.type == SelectionType.LINES:
                        mode = "VISUAL LINE" if self.mode_style == "full" else "V"
                    elif selection.type == SelectionType.BLOCK:
                        mode = "VISUAL BLOCK" if self.mode_style == "full" else "V"
                    else:
                        mode = "VISUAL" if self.mode_style == "full" else "V"
                else:
                    # Normal mode - return empty string or "NORMAL"/"N" based on preference
                    mode = "NORMAL" if self.mode_style == "full" else ""
            else:
                mode = ""
            return mode
        except:
            return ""

    def _get_content_width(self):
        """Calculate the total width of content inside the border."""
        content_width = 0

        # Prompt width
        if self.prompt:
            content_width += len(self.prompt)

        # Line numbers width
        if self.show_line_numbers:
            try:
                line_count = max(self.buffer.document.line_count, 1)
                line_number_width = len(str(line_count)) + 1  # +1 for space
                content_width += line_number_width + 1  # +1 for separator
            except:
                content_width += 3  # fallback for "1 |"

        # Minimum text area width
        content_width += 20  # minimum space for text input

        return content_width

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
                # Keep border width reasonable but not too wide
                available_width = terminal_width - 10
            except:
                available_width = 70

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
        """Create the bottom border line with mode (left) and validation message (right)."""
        def get_bottom_border():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
                # Keep border width reasonable but not too wide (same as top)
                available_width = terminal_width - 10
            except:
                available_width = 70

            # Get current mode and validation message
            mode = self._get_current_mode()
            mode_text = f" {mode} " if mode else ""

            validation_message = ""
            if self._validation_message and self._has_been_validated:
                validation_message = f" {self._validation_message} "

            # Calculate available space for middle padding
            mode_len = len(mode_text)
            message_len = len(validation_message)
            middle_padding = available_width - mode_len - message_len - 2

            if middle_padding < 0:
                # Not enough space, prioritize validation message
                if validation_message:
                    # Truncate validation message if needed
                    max_message_len = available_width - mode_len - 6  # Leave some space
                    if max_message_len > 0 and message_len > max_message_len:
                        validation_message = f" ...{self._validation_message[-(max_message_len-7):]} "
                        message_len = len(validation_message)
                    middle_padding = available_width - mode_len - message_len - 2
                else:
                    middle_padding = available_width - mode_len - 2

            # Ensure minimum padding
            middle_padding = max(middle_padding, 0)

            # Build the bottom border
            result = [(f'class:border-{self._validation_state}', box_chars['bottom_left'])]

            # Add mode text (left-aligned)
            if mode_text:
                result.append((f'class:mode-{self._validation_state}', mode_text))

            # Add middle padding
            if middle_padding > 0:
                result.append((f'class:border-{self._validation_state}', box_chars['horizontal'] * middle_padding))

            # Add validation message (right-aligned)
            if validation_message:
                result.append((f'class:validation-message-{self._validation_state}', validation_message))

            # Add right border
            result.append((f'class:border-{self._validation_state}', box_chars['bottom_right']))

            return result

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

        # Main text input area - constrain width to exactly match border calculation
        def get_text_width():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
                # Match the border calculation exactly
                available_width = terminal_width - 10

                # Calculate exact remaining space after all other components
                used_width = 2  # left and right borders
                if self.prompt:
                    used_width += len(self.prompt)
                if self.show_line_numbers:
                    try:
                        line_count = max(self.buffer.document.line_count, 1)
                        used_width += len(str(line_count)) + 2  # +2 for space and separator
                    except:
                        used_width += 3

                # Text area gets exactly what's left
                text_width = available_width - used_width
                return max(text_width, 20)
            except:
                return 50

        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            width=get_text_width
        )
        content_components.append(text_window)

        # Right border
        content_components.append(Window(
            content=FormattedTextControl(lambda: [(f'class:border-{self._validation_state}', box_chars['vertical'])]),
            width=1
        ))

        # Create middle content - let VSplit size naturally, borders will adapt
        middle_content = VSplit(content_components)
        components.append(middle_content)

        # Bottom border with validation message
        bottom_border_window = Window(
            content=FormattedTextControl(self._create_bottom_border_line(box_chars)),
            height=1
        )
        components.append(bottom_border_window)

        # Status bar removed - mode is now shown in bottom border

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
        """Create styling with state-based border colors using centralized theme."""
        # Get base style from centralized theme
        style_dict = self.theme.get_style_dict().copy()

        # Add state-based border styles
        state_styles = {
            # Active state
            'border-active': self.theme.get_color('border-active', '#4a9eff'),
            'title-active': f'bold {self.theme.get_color("border-title-active", "#4a9eff")}',
            'validation-message-active': self.theme.get_color('border-active', '#4a9eff'),
            'mode-active': f'bold {self.theme.get_color("border-title-active", "#4a9eff")}',

            # Valid state
            'border-valid': self.theme.get_color('border-valid', '#00ff88'),
            'title-valid': f'bold {self.theme.get_color("border-title-valid", "#00ff88")}',
            'validation-message-valid': f'bold {self.theme.get_color("validation-message-valid", "#00ff88")}',
            'mode-valid': f'bold {self.theme.get_color("border-title-valid", "#00ff88")}',

            # Invalid state
            'border-invalid': self.theme.get_color('border-invalid', '#ff4444'),
            'title-invalid': f'bold {self.theme.get_color("border-title-invalid", "#ff4444")}',
            'validation-message-invalid': f'bold {self.theme.get_color("validation-message-invalid", "#ff4444")}',
            'mode-invalid': f'bold {self.theme.get_color("border-title-invalid", "#ff4444")}',
        }

        return Style.from_dict({**style_dict, **state_styles})


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
                           show_mode_in_border=True,
                           mode_style="initial",
                           theme: Optional[VimReadlineTheme] = None):
    """
    Rich-styled vim input with validation.

    Args:
        prompt: Prompt text
        initial_text: Pre-populated text
        placeholder_text: Placeholder hint
        show_line_numbers: Show line numbers
        show_status: Show vim mode status (deprecated - mode now shown in border)
        wrap_lines: Enable line wrapping
        validator: Validator instance for input validation
        hidden_input: Hide input for passwords
        mask_character: Character for masking hidden input
        panel_title: Title for the Rich panel
        panel_box_style: Box style ("rounded", "square", "double", "heavy")
        show_mode_in_border: Show vim mode in bottom left of border
        mode_style: Mode display style ("initial", "full", "none")
        theme: VimReadlineTheme for customizing colors

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
        show_mode_in_border=show_mode_in_border,
        mode_style=mode_style,
        theme=theme
    )
    return readline.run()