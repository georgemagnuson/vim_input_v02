"""
Rich-enhanced version of VimReadline with bordered text areas and styled output.

This module provides an enhanced version that uses Rich for better visual presentation,
including bordered text areas, ruled lines, and enhanced status indicators.
"""

from .core import VimReadline as BaseVimReadline
from prompt_toolkit.application import Application
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.formatted_text import FormattedText
from rich.console import Console, ConsoleDimensions
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text
from rich.box import ROUNDED, SQUARE, DOUBLE, HEAVY
import io


class RichVimReadline(BaseVimReadline):
    """
    Enhanced VimReadline with Rich integration for better visual presentation.

    Features:
    - Bordered text areas using Rich Panel
    - Claude Code-style ruled lines above/below
    - Enhanced status indicators with icons and colors
    - Rich-styled error messages and output
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
                 # Rich-specific options
                 use_rich_panel=True,
                 panel_title="vim input",
                 panel_box_style="rounded",  # "rounded", "square", "double", "heavy"
                 show_rules=True,
                 rule_style="blue",
                 enhanced_status=True):

        # Rich options (initialize BEFORE parent constructor)
        self.use_rich_panel = use_rich_panel
        self.panel_title = panel_title
        self.panel_box_style = panel_box_style
        self.show_rules = show_rules
        self.rule_style = rule_style
        self.enhanced_status = enhanced_status

        # Rich console for rendering
        self.rich_console = Console(file=io.StringIO(), width=80)

        # Box style mapping
        self.box_styles = {
            "rounded": ROUNDED,
            "square": SQUARE,
            "double": DOUBLE,
            "heavy": HEAVY
        }

        # Initialize base class (this will call _create_layout)
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

    def _get_rich_panel_borders(self):
        """Generate Rich panel border characters for prompt-toolkit display."""

        # Get box style
        box_style = self.box_styles.get(self.panel_box_style, ROUNDED)

        # Create a sample panel to extract border characters
        sample_panel = Panel(
            "content",
            title=self.panel_title,
            box=box_style,
            width=60
        )

        # Render the panel to get border characters
        with io.StringIO() as string_io:
            temp_console = Console(file=string_io, width=60, legacy_windows=False)
            temp_console.print(sample_panel)
            panel_output = string_io.getvalue()

        lines = panel_output.strip().split('\n')

        if len(lines) >= 3:
            top_border = lines[0]
            bottom_border = lines[-1]

            # Extract border characters (simplified)
            return {
                'top': top_border,
                'bottom': bottom_border,
                'left': '│' if box_style == ROUNDED else ('║' if box_style == DOUBLE else '┃' if box_style == HEAVY else '│'),
                'right': '│' if box_style == ROUNDED else ('║' if box_style == DOUBLE else '┃' if box_style == HEAVY else '│')
            }

        # Fallback
        return {
            'top': '─' * 60,
            'bottom': '─' * 60,
            'left': '│',
            'right': '│'
        }

    def _create_rich_status_text(self):
        """Create Rich-enhanced status text with icons and colors."""

        if not self.enhanced_status:
            return ""

        # Get app safely - use self.app if available, otherwise get current app
        app = getattr(self, 'app', None)
        if not app:
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
            except:
                return ""

        if not app or not hasattr(app, 'vi_state'):
            return ""

        mode_info = {
            'vi-insert': ('INSERT', 'green', ''),
            'vi-replace': ('REPLACE', 'red', ''),
            'vi-navigation': {
                # Normal mode returns empty string (standard vim behavior)
                'normal': ('', 'blue', ''),
                'visual': ('VISUAL', 'yellow', ''),
                'visual-line': ('VISUAL LINE', 'yellow', ''),
                'visual-block': ('VISUAL BLOCK', 'yellow', '')
            }
        }

        input_mode = app.vi_state.input_mode

        if input_mode == 'vi-navigation':
            selection = self.buffer.selection_state
            if selection:
                from prompt_toolkit.selection import SelectionType
                if selection.type == SelectionType.LINES:
                    mode, color, icon = mode_info['vi-navigation']['visual-line']
                elif selection.type == SelectionType.BLOCK:
                    mode, color, icon = mode_info['vi-navigation']['visual-block']
                else:
                    mode, color, icon = mode_info['vi-navigation']['visual']
            else:
                mode, color, icon = mode_info['vi-navigation']['normal']
        else:
            mode, color, icon = mode_info.get(input_mode, ('UNKNOWN', 'white', '❓'))

        # Format with standard vim styling
        # For empty mode (normal), return empty string like standard vim
        if not mode or mode.strip() == "":
            return ""

        # Standard vim format without icons
        return f"-- {mode} --"

    def _create_layout(self):
        """Create Rich-enhanced layout with true bordered input area."""

        if not self.use_rich_panel:
            # Use standard layout
            return super()._create_layout()

        # Create components list
        components = []

        # Top rule
        if self.show_rules:
            rule_text = self._create_rule_line("top")
            top_rule_window = Window(
                content=FormattedTextControl(lambda: rule_text),
                height=1,
                dont_extend_width=True
            )
            components.append(top_rule_window)

        # Create the actual bordered box using prompt-toolkit's Frame-like layout
        from prompt_toolkit.layout.containers import VSplit
        from prompt_toolkit.layout.controls import BufferControl
        from prompt_toolkit.layout.processors import HighlightMatchingBracketProcessor

        # Get box characters for the selected style
        box_chars = self._get_box_characters()

        # Top border of the box
        top_border_content = self._create_top_border_line(box_chars)
        top_border_window = Window(
            content=FormattedTextControl(lambda: top_border_content),
            height=1
        )
        components.append(top_border_window)

        # Middle section with side borders and content
        buffer_control = BufferControl(
            buffer=self.buffer,
            include_default_input_processors=True,
            input_processors=[
                HighlightMatchingBracketProcessor()
            ]
        )

        # Build the content area with proper constraints
        content_components = []

        # Left border
        content_components.append(Window(
            content=FormattedTextControl(lambda: box_chars['vertical']),
            width=1,
            style='class:rich-border'
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

                # Calculate width based on line count
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

        # Main text input area - constrained within the box
        text_window = Window(
            content=buffer_control,
            wrap_lines=self.wrap_lines,
            dont_extend_width=False,
            left_margins=[],
            right_margins=[]
        )
        content_components.append(text_window)

        # Right border
        content_components.append(Window(
            content=FormattedTextControl(lambda: box_chars['vertical']),
            width=1,
            style='class:rich-border'
        ))

        # Create the middle content area with width constraint
        def get_box_width():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80
            # Use most of terminal width but leave some margin
            return max(terminal_width - 2, 40)

        middle_content = Window(
            content=VSplit(content_components),
            width=get_box_width,
            dont_extend_width=True
        )
        components.append(middle_content)

        # Bottom border of the box
        bottom_border_content = self._create_bottom_border_line(box_chars)
        bottom_border_window = Window(
            content=FormattedTextControl(lambda: bottom_border_content),
            height=1
        )
        components.append(bottom_border_window)

        # Enhanced status bar
        if self.show_status:
            status_window = Window(
                content=FormattedTextControl(lambda: self._create_rich_status_text()),
                height=1,
                style='class:rich-status'
            )
            components.append(status_window)

        # Bottom rule
        if self.show_rules:
            rule_text = self._create_rule_line("bottom")
            bottom_rule_window = Window(
                content=FormattedTextControl(lambda: rule_text),
                height=1,
                dont_extend_width=True
            )
            components.append(bottom_rule_window)

        self.layout = Layout(HSplit(components))

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
        """Create the top border line with optional title."""
        def get_top_border():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80

            # Match the width calculation from middle_content
            available_width = max(terminal_width - 4, 36)

            if self.panel_title:
                title = f" {self.panel_title} "
                title_len = len(title)
                if title_len + 2 < available_width:
                    remaining_width = available_width - title_len - 2
                    left_padding = 1
                    right_padding = remaining_width - left_padding
                    return f"{box_chars['top_left']}{box_chars['horizontal'] * left_padding}{title}{box_chars['horizontal'] * right_padding}{box_chars['top_right']}"
                else:
                    # Title too long, truncate
                    truncated_title = f" {self.panel_title[:available_width-6]}... "
                    return f"{box_chars['top_left']}{truncated_title}{box_chars['top_right']}"
            else:
                return f"{box_chars['top_left']}{box_chars['horizontal'] * available_width}{box_chars['top_right']}"

        return get_top_border()

    def _create_bottom_border_line(self, box_chars):
        """Create the bottom border line."""
        def get_bottom_border():
            try:
                from prompt_toolkit.application.current import get_app
                app = get_app()
                terminal_width = app.output.get_size().columns
            except:
                terminal_width = 80

            available_width = max(terminal_width - 4, 36)
            return f"{box_chars['bottom_left']}{box_chars['horizontal'] * available_width}{box_chars['bottom_right']}"

        return get_bottom_border()

    def _create_rule_line(self, position="top"):
        """Create a Rich-style rule line."""

        # Create rule with Rich
        if position == "top" and self.panel_title:
            rule = Rule(self.panel_title, style=self.rule_style)
        else:
            rule = Rule(style=self.rule_style)

        # Render rule to string
        with io.StringIO() as string_io:
            temp_console = Console(file=string_io, width=80, legacy_windows=False)
            temp_console.print(rule)
            rule_output = string_io.getvalue().strip()

        return rule_output

    def _create_style(self):
        """Create Rich-enhanced styling."""
        base_style = super()._create_style()

        # Add Rich-specific styles with better visibility
        rich_styles = {
            'rich-border': '#666666',
            'rich-status': 'bold bg:#2d3748 fg:#e2e8f0',  # Better contrast status bar
            'rich-rule': f'{self.rule_style}',
        }

        # Get base style dict safely
        if hasattr(base_style, 'style_rules'):
            # Convert list of tuples to dict
            base_dict = dict(base_style.style_rules)
        else:
            # Fallback for different prompt-toolkit versions
            base_dict = {
                'prompt': 'bold',
                'line-number': '#666666',
                'line-number-separator': '#666666',
                'status': 'bg:#2d3748 fg:#e2e8f0',  # Improved status visibility
                'placeholder': '#888888 italic',
            }

        # Merge styles
        from prompt_toolkit.styles import Style
        return Style.from_dict({**base_dict, **rich_styles})


# Convenience function for Rich-enhanced vim input
def rich_vim_input(prompt="",
                   initial_text="",
                   placeholder_text="",
                   show_line_numbers=False,
                   show_status=True,
                   wrap_lines=True,
                   submit_key='c-m',
                   newline_key='c-j',
                   cancel_keys=None,
                   # Rich-specific options
                   use_rich_panel=True,
                   panel_title="vim input",
                   panel_box_style="rounded",
                   show_rules=True,
                   rule_style="blue",
                   enhanced_status=True):
    """
    Rich-enhanced vim input function.

    Args:
        prompt: Prompt text
        initial_text: Pre-populated text
        placeholder_text: Placeholder hint
        show_line_numbers: Show line numbers
        show_status: Show vim mode status
        wrap_lines: Enable line wrapping
        submit_key: Key binding for submit
        newline_key: Key binding for newline
        cancel_keys: Key bindings for cancel
        use_rich_panel: Use Rich panel borders
        panel_title: Title for Rich panel
        panel_box_style: Box style ("rounded", "square", "double", "heavy")
        show_rules: Show ruled lines above/below
        rule_style: Style for ruled lines
        enhanced_status: Use enhanced status with icons

    Returns:
        str: Edited text or None if cancelled
    """

    readline = RichVimReadline(
        initial_text=initial_text,
        placeholder_text=placeholder_text,
        prompt=prompt,
        show_line_numbers=show_line_numbers,
        show_status=show_status,
        wrap_lines=wrap_lines,
        submit_key=submit_key,
        newline_key=newline_key,
        cancel_keys=cancel_keys,
        use_rich_panel=use_rich_panel,
        panel_title=panel_title,
        panel_box_style=panel_box_style,
        show_rules=show_rules,
        rule_style=rule_style,
        enhanced_status=enhanced_status
    )

    return readline.run()