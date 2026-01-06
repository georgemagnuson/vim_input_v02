# Rich Prompt API Integration

## Overview

**VimPrompt** extends Rich's `Prompt.ask()` API to provide vim-mode text editing within the familiar Rich interface.

## The Problem

Rich provides `Prompt.ask()` for user input, but it:
- ❌ Only supports single-line input
- ❌ Has no vim modal editing
- ❌ Cannot handle multiline text

## The Solution

**VimPrompt** extends `PromptBase` to provide:
- ✅ Vim modal editing (normal/insert/visual modes)
- ✅ Multiline text editing
- ✅ Compatible with Rich's validation system
- ✅ Same API style as `Prompt.ask()`

## Usage

### Basic Example

```python
from vim_readline import VimPrompt

# Just like Prompt.ask(), but with vim!
name = VimPrompt.ask_vim("Enter your name:")
```

### With Validation (Choices)

```python
language = VimPrompt.ask_vim(
    "Select language:",
    choices=["Python", "Rust", "Go"],
    panel_title="Language Selection"
)
```

### Multiline Code Editor

```python
code = VimPrompt.ask_vim(
    "Enter Python code:",
    panel_title="Code Editor",
    show_line_numbers=True,
    placeholder_text="def main():\n    pass"
)
```

### Typed Prompts

```python
from vim_readline import IntVimPrompt, FloatVimPrompt

# Integer input with vim editing
age = IntVimPrompt.ask_vim("Enter age:", default=25)

# Float input with vim editing
price = FloatVimPrompt.ask_vim("Enter price:", default=19.99)
```

### Convenience Functions

```python
from vim_readline import ask_vim, ask_vim_int, ask_vim_float

# Shorthand for VimPrompt.ask_vim()
name = ask_vim("Enter name:")
age = ask_vim_int("Enter age:")
price = ask_vim_float("Enter price:")
```

## API Reference

### `VimPrompt.ask_vim()`

```python
VimPrompt.ask_vim(
    prompt: str = "",
    *,
    # Rich Prompt parameters
    console: Optional[Console] = None,
    password: bool = False,
    choices: Optional[List[str]] = None,
    show_default: bool = True,
    show_choices: bool = True,
    default: Any = ...,

    # VimReadline parameters
    panel_title: Optional[str] = None,
    panel_box_style: str = "rounded",  # rounded/square/double/heavy
    theme: Optional[ValidatedRichTheme] = None,
    show_line_numbers: bool = False,
    show_status: bool = True,
    placeholder_text: str = "",
) -> str
```

### Parameters

**From Rich Prompt:**
- `prompt`: Prompt text (supports Rich markup)
- `console`: Rich Console instance
- `password`: Enable password masking
- `choices`: List of valid choices (validated)
- `show_default`: Show default value in prompt
- `show_choices`: Show available choices
- `default`: Default value if empty input

**VimReadline Extensions:**
- `panel_title`: Title shown on editor panel
- `panel_box_style`: Border style (rounded/square/double/heavy)
- `theme`: Custom ValidatedRichTheme for colors
- `show_line_numbers`: Display line numbers
- `show_status`: Show vim mode status
- `placeholder_text`: Hint text when empty

## Comparison with Rich's Prompt

| Feature | `Prompt.ask()` | `VimPrompt.ask_vim()` |
|---------|----------------|----------------------|
| **API Style** | ✅ Rich standard | ✅ Rich compatible |
| **Single-line** | ✅ Yes | ✅ Yes |
| **Multiline** | ❌ No | ✅ Yes |
| **Vim Modes** | ❌ No | ✅ Yes (normal/insert/visual) |
| **Validation** | ✅ Yes | ✅ Yes |
| **Choices** | ✅ Yes | ✅ Yes |
| **Line Numbers** | ❌ No | ✅ Yes |
| **Rich Styling** | ✅ Yes | ✅ Yes |
| **Password Input** | ✅ Yes | ✅ Yes |

## When to Use What

### Use `Prompt.ask()` (Rich standard)
- Simple single-line prompts
- Quick input in scripts
- When vim mode is not needed
- Minimal dependencies

### Use `VimPrompt.ask_vim()`
- Multiline text editing
- Code input
- Complex text manipulation
- Users who prefer vim keybindings
- When you need line numbers or vim modes

## Implementation Details

### How It Works

`VimPrompt` extends Rich's `PromptBase` class and overrides the `get_input()` method:

```python
class VimPrompt(PromptBase[str]):
    def get_input(self, console, prompt, password, stream):
        # Uses VimReadline instead of Python's input()
        return validated_rich_vim_input(
            validator=self._build_validator(),
            hidden_input=password,
            panel_title=self.vim_panel_title,
            ...
        )
```

This means:
- ✅ Rich handles validation loop and error display
- ✅ Rich handles choices validation
- ✅ Rich handles prompt rendering
- ✅ VimReadline handles text input with vim modes
- ✅ Full integration between both systems

## Examples

### Form with Multiple Fields

```python
from vim_readline import VimPrompt, IntVimPrompt
from rich.console import Console

console = Console()

console.print("[bold]User Registration[/bold]\n")

name = VimPrompt.ask_vim("Name:", panel_title="Name")
age = IntVimPrompt.ask_vim("Age:", panel_title="Age", default=18)
bio = VimPrompt.ask_vim(
    "Bio:",
    panel_title="Biography",
    show_line_numbers=True,
    placeholder_text="Tell us about yourself..."
)

console.print(f"\n[green]✓[/green] Registration complete!")
console.print(f"Name: {name}, Age: {age}")
```

### Code Snippet Input

```python
from vim_readline import VimPrompt
from rich.syntax import Syntax
from rich.console import Console

console = Console()

code = VimPrompt.ask_vim(
    "[bold cyan]Enter Python code:[/bold cyan]",
    panel_title="Python Editor",
    show_line_numbers=True,
    placeholder_text="def example():\n    return 42"
)

# Display with syntax highlighting
console.print("\n[green]Code entered:[/green]")
syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
console.print(syntax)
```

## Demo

Run the demo to see all features:

```bash
python demos/rich_prompt_api_demo.py
```

## Related Documentation

- [README.md](README.md) - Main project documentation
- [VIM_HELP.md](VIM_HELP.md) - Vim keybindings reference
- [THEMING.md](THEMING.md) - Theming system documentation

## Acknowledgments

Built on:
- [Rich](https://github.com/Textualize/rich) by Textualize - Beautiful terminal output
- [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - Vim mode engine
