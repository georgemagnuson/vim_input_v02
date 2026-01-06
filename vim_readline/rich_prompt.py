"""
Rich Prompt integration with VimReadline.

Extends Rich's Prompt API to provide vim-mode text input.
"""
from typing import Optional, List, Any, TextIO
from rich.prompt import PromptBase
from rich.console import Console
from rich.text import Text, TextType

from .validated_rich import validated_rich_vim_input, ValidatedRichTheme
from .validators import Validator, custom


class VimPrompt(PromptBase[str]):
    """
    A Rich Prompt that uses VimReadline for input with vim modal editing.

    Extends Rich's standard Prompt to provide vim-mode text entry while
    maintaining compatibility with Rich's validation and styling system.

    Example:
        >>> from vim_readline.rich_prompt import VimPrompt
        >>> name = VimPrompt.ask("Enter your name")
        >>> code = VimPrompt.ask_vim(
        ...     "Enter code",
        ...     panel_title="Python Editor",
        ...     show_line_numbers=True
        ... )
    """

    response_type = str
    validate_error_message = "[prompt.invalid]Please enter a valid value"

    # VimReadline specific options
    vim_panel_title: Optional[str] = None
    vim_panel_box_style: str = "rounded"
    vim_theme: Optional[ValidatedRichTheme] = None
    vim_show_line_numbers: bool = False
    vim_show_status: bool = True
    vim_placeholder_text: str = ""

    @classmethod
    def ask_vim(
        cls,
        prompt: TextType = "",
        *,
        console: Optional[Console] = None,
        password: bool = False,
        choices: Optional[List[str]] = None,
        show_default: bool = True,
        show_choices: bool = True,
        default: Any = ...,
        # VimReadline specific parameters
        panel_title: Optional[str] = None,
        panel_box_style: str = "rounded",
        theme: Optional[ValidatedRichTheme] = None,
        show_line_numbers: bool = False,
        show_status: bool = True,
        placeholder_text: str = "",
    ) -> str:
        """
        Ask for input using vim-mode editing.

        This extends Rich's standard Prompt.ask() with vim modal editing
        capabilities through VimReadline integration.

        Args:
            prompt: Prompt text (supports Rich markup)
            console: Rich Console instance (optional)
            password: Enable password masking
            choices: List of valid choices
            show_default: Show default value in prompt
            show_choices: Show available choices
            default: Default value if user enters nothing
            panel_title: Title for vim editor panel
            panel_box_style: Box style (rounded/square/double/heavy)
            theme: ValidatedRichTheme for colors
            show_line_numbers: Show line numbers in editor
            show_status: Show vim mode status
            placeholder_text: Placeholder hint text

        Returns:
            User input as string

        Example:
            >>> code = VimPrompt.ask_vim(
            ...     "[bold cyan]Enter Python code:[/bold cyan]",
            ...     panel_title="Code Editor",
            ...     show_line_numbers=True,
            ...     placeholder_text="def main():\\n    pass"
            ... )
        """
        _prompt = cls(
            prompt,
            console=console,
            password=password,
            choices=choices,
            show_default=show_default,
            show_choices=show_choices,
        )

        # Store VimReadline options
        _prompt.vim_panel_title = panel_title or str(prompt)
        _prompt.vim_panel_box_style = panel_box_style
        _prompt.vim_theme = theme
        _prompt.vim_show_line_numbers = show_line_numbers
        _prompt.vim_show_status = show_status
        _prompt.vim_placeholder_text = placeholder_text

        return _prompt(default=default)

    def get_input(
        self,
        console: Console,
        prompt: TextType,
        password: bool,
        stream: Optional[TextIO] = None,
    ) -> str:
        """
        Override get_input to use VimReadline instead of standard input().

        This is the key integration point - replaces Rich's default input
        with vim-mode editing via VimReadline.
        """
        # Build validator from choices if provided
        validator = None
        if self.choices:
            def validate_choice(text: str) -> tuple[bool, str]:
                if not text:
                    return True, ""  # Allow empty for default

                # Check if valid choice
                choices_to_check = self.choices
                if not self.case_sensitive:
                    text = text.lower()
                    choices_to_check = [c.lower() for c in self.choices]

                if text in choices_to_check:
                    return True, ""

                return False, f"Please select from: {', '.join(self.choices)}"

            validator = custom(validate_choice, allow_empty=bool(self.default != ...))

        # Display the prompt text using Rich Console
        if prompt:
            console.print(prompt, end="")

        # Use VimReadline for input
        result = validated_rich_vim_input(
            prompt="",  # Already displayed above
            placeholder_text=self.vim_placeholder_text,
            validator=validator,
            hidden_input=password,
            panel_title=self.vim_panel_title,
            panel_box_style=self.vim_panel_box_style,
            theme=self.vim_theme,
            show_line_numbers=self.vim_show_line_numbers,
            show_status=self.vim_show_status,
        )

        return result if result is not None else ""


class IntVimPrompt(VimPrompt):
    """
    Vim-mode prompt that returns an integer.

    Example:
        >>> age = IntVimPrompt.ask_vim("Enter your age", panel_title="Age")
    """
    response_type = int
    validate_error_message = "[prompt.invalid]Please enter a valid integer"

    def process_response(self, value: str) -> int:
        """Convert string response to integer."""
        try:
            return int(value)
        except ValueError:
            raise self.validate_error_class(self.validate_error_message)


class FloatVimPrompt(VimPrompt):
    """
    Vim-mode prompt that returns a float.

    Example:
        >>> price = FloatVimPrompt.ask_vim("Enter price", panel_title="Price")
    """
    response_type = float
    validate_error_message = "[prompt.invalid]Please enter a valid number"

    def process_response(self, value: str) -> float:
        """Convert string response to float."""
        try:
            return float(value)
        except ValueError:
            raise self.validate_error_class(self.validate_error_message)


# Convenience aliases
ask_vim = VimPrompt.ask_vim
ask_vim_int = IntVimPrompt.ask_vim
ask_vim_float = FloatVimPrompt.ask_vim
