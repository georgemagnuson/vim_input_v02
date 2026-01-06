# VimReadline

A vim-mode readline implementation for single-buffer text editing, built on `prompt-toolkit`. Perfect for interactive applications that need vim-style text input with optional validation, Rich styling, and centralized theming - all without file I/O operations.

**Available Variants:**
- **VimReadline**: Clean, minimal vim text editor
- **ValidatedVimReadline**: Core + input validation and hidden input
- **ValidatedRichVimReadline**: Rich styling + validation + state-based border coloring
- **VimPrompt**: Extends Rich's `Prompt.ask()` API with vim modal editing

## Features

### Core Features
- **Full vim navigation modes**: normal, insert, visual, replace
- **Configurable key bindings**: Return to submit, Ctrl-J/Shift-Return for newline
- **Cursor shape changes**: beam (insert), block (normal), underline (replace)
- **Optional UI elements**: line numbers, status indicators ("-- INSERT --")
- **Flexible text handling**: initial text (editable) or placeholder text (hint)
- **No file I/O**: pure in-memory text buffer editing
- **Terminal agnostic**: works across different terminal environments

### Validation Features (ValidatedVimReadline)
- **Built-in validators**: email, date, integer, float, regex, length
- **Custom validators**: define your own validation logic
- **Composite validators**: combine multiple validators with AND logic
- **Hidden input**: password masking with configurable mask characters
- **Validation on exit**: validates on submit, prevents invalid input

### Rich Styling Features (ValidatedRichVimReadline)
- **State-based border coloring**: Blue (active) → Green (valid) / Red (invalid)
- **Rich box styles**: rounded, square, double, heavy borders
- **Validation messages**: displayed in bottom border (right-aligned)
- **Customizable themes**: configure colors for all validation states
- **Panel titles**: optional titles on top border

### Theming System
- **6 built-in themes**: Dark, Light, Minimal, HighContrast, Neon, custom
- **Centralized theming**: consistent color schemes across all variants
- **Fully customizable**: create your own themes with `create_custom_theme()`
- **Theme documentation**: see `THEMING.md` for details

### Rich Prompt API Integration
- **Extends Rich's Prompt**: `VimPrompt.ask_vim()` works like `Prompt.ask()` but with vim
- **Familiar API**: Same interface as Rich's standard prompts
- **Type variants**: `IntVimPrompt`, `FloatVimPrompt` for typed input
- **Seamless integration**: Works with Rich's validation, choices, and styling

## Installation

### From PyPI (when published)
```bash
pip install vim-readline
```

### Development installation
```bash
git clone <repository-url>
cd vim_input_v02
pip install -e .
```

## Quick Start

### Core VimReadline
```python
from vim_readline import vim_input

# Simple usage
result = vim_input(prompt=">>> ", placeholder_text="Type here...")
if result:
    print(f"You entered: {result}")

# With initial content
result = vim_input(
    initial_text="def hello():\n    pass",
    show_line_numbers=True,
    show_status=True
)
```

### ValidatedVimReadline (With Validation)
```python
from vim_readline import validated_vim_input, email, integer, custom

# Email validation
email_result = validated_vim_input(
    prompt="Email: ",
    placeholder_text="Enter your email...",
    validator=email(allow_empty=False)
)

# Age validation with bounds
age_result = validated_vim_input(
    prompt="Age: ",
    validator=integer(min_value=1, max_value=150, allow_empty=False)
)

# Password input (hidden)
password_result = validated_vim_input(
    prompt="Password: ",
    validator=custom(my_password_validator, allow_empty=False),
    hidden_input=True,
    mask_character='●'
)
```

### ValidatedRichVimReadline (Rich Styling + Validation)
```python
from vim_readline import validated_rich_vim_input, ValidatedRichTheme, email

# Email input with Rich styling and state-based borders
email_result = validated_rich_vim_input(
    prompt="Email: ",
    placeholder_text="Enter your email...",
    validator=email(allow_empty=False),
    panel_title="Email Input",
    panel_box_style="rounded"  # Border color changes based on validation
)

# Password with custom theme
purple_theme = ValidatedRichTheme(
    border_active="magenta",
    border_valid="bright_green",
    border_invalid="bright_red"
)

password_result = validated_rich_vim_input(
    prompt="Password: ",
    validator=custom(my_password_validator),
    hidden_input=True,
    mask_character='●',
    panel_title="Password Entry",
    panel_box_style="double",
    theme=purple_theme
)
```

### VimPrompt (Rich Prompt API Integration)
```python
from vim_readline import VimPrompt, IntVimPrompt, ask_vim

# Extends Rich's Prompt.ask() with vim editing!
name = VimPrompt.ask_vim("Enter your name:")

# Multiline code editor (Rich's Prompt can't do this!)
code = VimPrompt.ask_vim(
    "[bold cyan]Enter Python code:[/bold cyan]",
    panel_title="Code Editor",
    show_line_numbers=True,
    placeholder_text="def main():\n    pass"
)

# Typed prompts with vim editing
age = IntVimPrompt.ask_vim("Enter age:", default=25)

# Convenience function (shorthand)
bio = ask_vim("Enter bio:", panel_title="Biography")
```

## Validators

### Built-in Validators
```python
from vim_readline import email, date, integer, float_num, regex, length, custom, combine

# Email validation
validator = email(allow_empty=False)

# Date validation with custom format
validator = date(format="%Y-%m-%d", allow_empty=True)

# Integer with bounds
validator = integer(min_value=0, max_value=100, allow_empty=False)

# Float with bounds
validator = float_num(min_value=0.0, max_value=1.0, allow_empty=False)

# Regex pattern
validator = regex(r"^[A-Z]{3}-\d{4}$", error_msg="Format: ABC-1234")

# Text length
validator = length(min_length=3, max_length=20, allow_empty=False)

# Custom validation function
def validate_username(text):
    if len(text) < 3:
        return False, "Username must be at least 3 characters"
    if not text.isalnum():
        return False, "Username must be alphanumeric"
    return True, ""

validator = custom(validate_username, allow_empty=False)

# Combine multiple validators (AND logic)
validator = combine(
    length(min_length=8, max_length=20),
    regex(r".*[A-Z].*", error_msg="Must contain uppercase"),
    regex(r".*[0-9].*", error_msg="Must contain digit")
)
```

## Advanced Usage

### Full VimReadline Configuration
```python
from vim_readline import VimReadline

readline = VimReadline(
    initial_text="Edit this text...",
    placeholder_text="Start typing...",
    prompt="sql> ",
    show_line_numbers=True,
    show_status=True,
    wrap_lines=False,
    submit_key='c-m',        # Return key
    newline_key='c-j',       # Ctrl-J (or Shift-Return)
    cancel_keys=['c-c']      # Ctrl-C to cancel
)

result = readline.run()
if result is not None:
    print("Submitted:", repr(result))
else:
    print("Cancelled")
```

### Custom Themes
```python
from vim_readline import create_custom_theme, validated_rich_vim_input

# Create custom theme
my_theme = create_custom_theme(
    background="#1e1e2e",
    foreground="#cdd6f4",
    accent="#89b4fa",
    status_bg="#45475a",
    status_fg="#cdd6f4"
)

# Use custom theme with ValidatedRichVimReadline
result = validated_rich_vim_input(
    prompt="> ",
    theme=my_theme,
    panel_title="Custom Theme Editor"
)
```

## Key Bindings

### Submit/Cancel
- **Return** (`c-m`) → Submit text and exit
- **Ctrl-J** or **Shift-Return** → Insert newline (continue editing)
- **Ctrl-C** (`c-c`) → Cancel and return None

### Vim Navigation
- **ESC** → Switch to normal mode
- **i, a, o, I, A, O** → Enter insert mode
- **hjkl** → Move cursor
- **w, b, e** → Word movement
- **0, $** → Line start/end
- **gg, G** → Buffer start/end
- **v, V** → Visual selection modes
- **yy, p** → Yank and paste
- **dd, x** → Delete operations
- **u, Ctrl-R** → Undo/redo

### Search
- **/text** → Search forward
- **?text** → Search backward
- **n, N** → Next/previous match

For complete keybindings, see `VIM_HELP.md`.

## Examples

Run the interactive examples:

```bash
# Rich Prompt API integration demo (NEW!)
python demos/rich_prompt_api_demo.py

# ValidatedRichVimReadline demos (recommended)
python demos/validated_rich_demo.py

# Comprehensive validation demos
python demos/validation_demos.py

# Quick validation example
python demos/quick_validation_example.py

# Theme showcase
python demos/theme_showcase_rich.py

# Legacy Rich box style demo
python demos/vim_rich_box_style_editor.py
```

## Use Cases

### Rich Prompt Integration (NEW!)
```python
from vim_readline import VimPrompt, IntVimPrompt
from rich.console import Console

console = Console()
console.print("[bold]User Registration[/bold]\n")

# Use VimPrompt like Rich's Prompt.ask()!
name = VimPrompt.ask_vim("Name:", panel_title="Name")
age = IntVimPrompt.ask_vim("Age:", panel_title="Age", default=18)
bio = VimPrompt.ask_vim(
    "Bio:",
    panel_title="Biography",
    show_line_numbers=True
)

console.print(f"\n[green]✓[/green] Registration complete!")
```

### Form Input with Validation
```python
from vim_readline import validated_rich_vim_input, email, integer

def registration_form():
    email = validated_rich_vim_input(
        prompt="Email: ",
        validator=email(allow_empty=False),
        panel_title="Registration - Email"
    )

    age = validated_rich_vim_input(
        prompt="Age: ",
        validator=integer(min_value=18, max_value=150),
        panel_title="Registration - Age"
    )

    return {"email": email, "age": age}
```

### Interactive CLI Applications
```python
from vim_readline import vim_input

def get_sql_query():
    return vim_input(
        prompt="sql> ",
        placeholder_text="SELECT * FROM table_name;",
        show_line_numbers=True
    )

query = get_sql_query()
if query:
    execute_sql(query)
```

### Password Input
```python
from vim_readline import validated_rich_vim_input, length, regex, combine

password_validator = combine(
    length(min_length=8, max_length=128),
    regex(r".*[A-Z].*", error_msg="Must contain uppercase"),
    regex(r".*[a-z].*", error_msg="Must contain lowercase"),
    regex(r".*[0-9].*", error_msg="Must contain digit")
)

password = validated_rich_vim_input(
    prompt="Password: ",
    validator=password_validator,
    hidden_input=True,
    mask_character='●',
    panel_title="Create Password",
    panel_box_style="double"
)
```

### Code Input Interfaces
```python
from vim_readline import vim_input

def code_editor():
    template = '''def main():
    """Your code here"""
    pass'''

    code = vim_input(
        initial_text=template,
        show_line_numbers=True,
        show_status=True
    )

    return code
```

## API Reference

### `vim_input()`
Simple function interface for basic vim text editing.

**Parameters:**
- `prompt` (str): Prompt text shown at start of lines
- `initial_text` (str): Pre-populated editable content
- `placeholder_text` (str): Hint text when buffer is empty
- `show_line_numbers` (bool): Display line numbers
- `show_status` (bool): Show vim mode status
- `wrap_lines` (bool): Enable line wrapping

**Returns:** `str` or `None` (if cancelled)

### `validated_vim_input()`
Vim text editing with input validation.

**Parameters:**
- All parameters from `vim_input()` plus:
- `validator` (Validator): Validator instance for input validation
- `hidden_input` (bool): Enable password masking (default: False)
- `mask_character` (str): Character for masking (default: '*')

**Returns:** `str` or `None` (if cancelled or validation fails)

### `validated_rich_vim_input()`
Vim text editing with Rich styling, validation, and state-based borders.

**Parameters:**
- All parameters from `validated_vim_input()` plus:
- `panel_title` (str): Title shown on top border
- `panel_box_style` (str): Box style - "rounded", "square", "double", "heavy" (default: "rounded")
- `theme` (ValidatedRichTheme): Custom theme for colors

**Returns:** `str` or `None` (if cancelled or validation fails)

### `ValidatedRichTheme`
Theme configuration for ValidatedRichVimReadline.

**Parameters:**
- `border_active` (str): Border color when active (default: "blue")
- `border_valid` (str): Border color when valid (default: "green")
- `border_invalid` (str): Border color when invalid (default: "red")
- `border_title_active` (str): Title color when active
- `border_title_valid` (str): Title color when valid
- `border_title_invalid` (str): Title color when invalid
- `validation_message_valid` (str): Valid message color
- `validation_message_invalid` (str): Invalid message color

### `VimPrompt` (Rich Prompt API)
Extends Rich's `Prompt.ask()` with vim modal editing.

**Methods:**
- `VimPrompt.ask_vim(prompt, *, console=None, password=False, choices=None, ...)` → `str`
- `IntVimPrompt.ask_vim(...)` → `int`
- `FloatVimPrompt.ask_vim(...)` → `float`

**Parameters:**
- All parameters from Rich's `Prompt.ask()` plus:
- `panel_title` (str): Title for editor panel
- `panel_box_style` (str): Box style (rounded/square/double/heavy)
- `theme` (ValidatedRichTheme): Custom theme
- `show_line_numbers` (bool): Display line numbers
- `show_status` (bool): Show vim mode status
- `placeholder_text` (str): Placeholder hint text

**Convenience Functions:**
- `ask_vim(prompt, ...)` → Shorthand for `VimPrompt.ask_vim()`
- `ask_vim_int(prompt, ...)` → Shorthand for `IntVimPrompt.ask_vim()`
- `ask_vim_float(prompt, ...)` → Shorthand for `FloatVimPrompt.ask_vim()`

**Example:**
```python
from vim_readline import VimPrompt, ask_vim

# Extends Rich's Prompt.ask()
code = VimPrompt.ask_vim(
    "Enter code:",
    panel_title="Editor",
    show_line_numbers=True
)

# Or use shorthand
result = ask_vim("Enter text:")
```

## Project Structure

```
vim_input_v02/
├── vim_readline/              # Core library
│   ├── __init__.py           # Package interface
│   ├── core.py               # Core VimReadline implementation
│   ├── validated.py          # ValidatedVimReadline with validation
│   ├── validated_rich.py     # ValidatedRichVimReadline with Rich styling
│   ├── validators.py         # Validation system
│   ├── themes.py             # Centralized theming system
│   ├── constrained.py        # Box-constrained variant
│   ├── full_box.py           # Full box variant
│   └── rich_enhanced.py      # Rich-enhanced variant (legacy)
├── demos/                    # Interactive demonstrations
│   ├── validated_rich_demo.py         # ValidatedRichVimReadline demos
│   ├── validation_demos.py            # Comprehensive validation demos
│   ├── quick_validation_example.py    # Simple validation example
│   ├── theme_showcase_rich.py         # Theme showcase
│   └── vim_rich_box_style_editor.py   # Legacy Rich demo
├── tests/                    # Test suite
├── archive/                  # Development history
├── CLAUDE.md                 # Claude Code project instructions
├── README.md                 # This file
├── THEMING.md               # Theming system documentation
├── VIM_HELP.md              # Vim keybindings reference
├── TEXTUAL_INTEGRATION_RESEARCH.md  # Textual integration research
└── setup.py                  # Package installation
```

## Variants Comparison

### 1. VimReadline (Core)
- **Location**: `vim_readline/core.py`
- **Style**: Clean, minimal interface
- **Usage**: `from vim_readline import vim_input`
- **Features**: Basic vim editing, no validation
- **Best for**: Simple text input, embedded use

### 2. ValidatedVimReadline
- **Location**: `vim_readline/validated.py`
- **Style**: Minimal interface with validation
- **Usage**: `from vim_readline import validated_vim_input`
- **Features**: Vim editing + validation + hidden input
- **Best for**: Form inputs, validated text entry

### 3. ValidatedRichVimReadline (Recommended)
- **Location**: `vim_readline/validated_rich.py`
- **Style**: Rich box styling with state-based borders
- **Usage**: `from vim_readline import validated_rich_vim_input`
- **Features**: Vim editing + validation + Rich styling + border colors
- **Best for**: Professional UIs, form inputs, password entry, interactive applications

### 4. VimPrompt (Rich Prompt API - NEW!)
- **Location**: `vim_readline/rich_prompt.py`
- **Style**: Extends Rich's `Prompt.ask()` API
- **Usage**: `from vim_readline import VimPrompt, ask_vim`
- **Features**: Vim editing + Rich's Prompt API + validation + multiline
- **Best for**: Rich users wanting vim mode, familiar API, seamless integration with Rich apps

## Requirements

- Python 3.7+
- prompt-toolkit >= 3.0.0
- rich >= 12.0.0

## Documentation

- **README.md** - This file (project overview and API)
- **RICH_PROMPT_INTEGRATION.md** - Rich Prompt API integration guide (NEW!)
- **CLAUDE.md** - Claude Code project instructions
- **THEMING.md** - Theming system documentation
- **VIM_HELP.md** - Complete vim keybindings reference
- **TEXTUAL_INTEGRATION_RESEARCH.md** - Textual widget integration research

## License

MIT License

## Contributing

Issues and pull requests welcome! This project was generated with Claude Code.

## Acknowledgments

Built on the excellent [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) library and [Rich](https://github.com/Textualize/rich) for beautiful terminal output.
