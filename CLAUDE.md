# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VimReadline** - A vim-mode readline implementation for single-buffer text editing without file I/O, based on `prompt-toolkit`.

Available in multiple variants:
- **Core VimReadline**: Clean, minimal vim text editor (`vim_readline/core.py`) [Legacy - will be replaced]
- **ValidatedVimReadline**: Core functionality plus input validation and hidden input (`vim_readline/validated.py`) [Primary interface]
- **ValidatedRichVimReadline**: Rich box styling + validation with state-based border coloring (`vim_readline/validated_rich.py`) [Primary Rich interface]
- **RichVimReadline**: Rich-inspired box styling (`vim_readline/rich_enhanced.py`) [Legacy - will be replaced]

## Key Features

- Full vim navigation modes (normal/insert/visual/replace)
- Configurable submit keys (Return to submit, Ctrl-J/Shift-Return for newline)
- Cursor shape changes by mode (beam/block/underline)
- Optional line numbers and status indicators ("-- INSERT --")
- Support for both initial_text (editable) and placeholder_text (hint)
- Input validation: Email, date, integer, float, regex, length, custom validators
- Hidden input: Password masking with configurable characters
- Rich styling: State-based border coloring (blue=active, green=valid, red=invalid)
- Validation on exit: Prevents real-time bounceback, validates on submit
- Customizable themes: Configurable colors for all validation states
- Validation messages: Right-aligned in bottom border
- No file I/O - pure in-memory text buffer editing

## Development Setup

The project uses direnv for local Python environment management:

```bash
# Install direnv if not already installed
# macOS: brew install direnv
# Add to your shell: eval "$(direnv hook bash)" or eval "$(direnv hook zsh)"

# Allow the .envrc file (first time only)
direnv allow

# Dependencies are automatically installed
# Run demos
python demos/vim_rich_box_style_editor.py  # Rich box style demo
python demos/demo_complete_rich_solution.py  # Complete solution demo
```

Manual setup (without direnv):
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Core Architecture

- `VimReadline` class: Main interface built on prompt-toolkit Application
- Uses prompt-toolkit's built-in vi-mode with custom key bindings
- Layout system with optional line numbers and status bar
- Modal cursor shapes configured via ModalCursorShapeConfig

## Key Files

### Core Library
- `vim_readline/core.py`: Main VimReadline implementation [Legacy]
- `vim_readline/validated.py`: ValidatedVimReadline with input validation [Primary]
- `vim_readline/validated_rich.py`: ValidatedRichVimReadline with Rich styling [Primary Rich]
- `vim_readline/validators.py`: Validation system and built-in validators
- `vim_readline/rich_enhanced.py`: RichVimReadline [Legacy]
- `vim_readline/__init__.py`: Package interface

### Demos
- `demos/validated_rich_demo.py`: ValidatedRichVimReadline state-based coloring demos
- `demos/validation_demos.py`: Comprehensive validation feature demos
- `demos/quick_validation_example.py`: Simple validation usage example
- `demos/vim_rich_box_style_editor.py`: Rich box style vim editor [Legacy demo]
- `demos/demo_complete_rich_solution.py`: Shows all solution approaches [Legacy]
- `demos/interactive_rich_demo.py`: Basic Rich interactive editor [Legacy]

### Project Files
- `requirements.txt`: prompt-toolkit>=3.0.0, rich
- `tests/`: Test suite
- `archive/`: Development history and experiments

## API Usage

### Core VimReadline
```python
from vim_readline import vim_input, VimReadline

# Simple usage
result = vim_input(placeholder_text="Enter code...")

# Advanced usage
readline = VimReadline(
    initial_text="def hello():\n    pass",
    show_line_numbers=True,
    show_status=True
)
result = readline.run()  # Returns edited text or None if cancelled
```

### ValidatedRichVimReadline (Recommended)
```python
from vim_readline import validated_rich_vim_input, ValidatedRichTheme, email, integer

# Email validation with Rich styling and state-based border colors
email_result = validated_rich_vim_input(
    prompt="Email: ",
    placeholder_text="Enter your email...",
    validator=email(allow_empty=False),
    panel_title="Email Input",
    panel_box_style="rounded"  # Border changes: blue→green/red based on validation
)

# Password input with custom theme
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

# Age validation with custom colors
age_result = validated_rich_vim_input(
    prompt="Age: ",
    validator=integer(min_value=1, max_value=150, allow_empty=False),
    panel_title="Age Entry",
    panel_box_style="heavy"
)
```

### ValidatedVimReadline (Basic Validation)
```python
from vim_readline import validated_vim_input, email, integer, regex

# Email validation
email_result = validated_vim_input(
    prompt="Email: ",
    placeholder_text="Enter your email...",
    validator=email(allow_empty=False)
)

# Age validation
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

# Custom validation
def validate_username(text):
    if len(text) < 3:
        return False, "Username must be at least 3 characters"
    if not text.isalnum():
        return False, "Username must be alphanumeric"
    return True, ""

username = validated_vim_input(
    prompt="Username: ",
    validator=custom(validate_username, allow_empty=False)
)
```

### Available Validators
- `email()`: Email address validation
- `date(format="%Y-%m-%d")`: Date validation with custom format
- `integer(min_value=None, max_value=None)`: Integer validation with bounds
- `float_num(min_value=None, max_value=None)`: Float validation with bounds
- `regex(pattern, error_msg)`: Regular expression validation
- `length(min_length=None, max_length=None)`: Text length validation
- `custom(validator_func)`: Custom validation function
- `combine(*validators)`: Combine multiple validators with AND logic

### Demo Usage
```bash
# Run ValidatedRichVimReadline demos (recommended)
python demos/validated_rich_demo.py

# Run comprehensive validation demos
python demos/validation_demos.py

# Run quick validation example
python demos/quick_validation_example.py

# Test validation systems
python test_validation.py
python test_validated_rich.py
```

### ValidatedRichTheme Configuration
```python
# Default theme
default_theme = ValidatedRichTheme()
# border_active="blue", border_valid="green", border_invalid="red"

# Custom theme
custom_theme = ValidatedRichTheme(
    border_active="cyan",           # Active input border color
    border_valid="yellow",          # Valid input border color
    border_invalid="red",           # Invalid input border color
    border_title_active="bright_cyan",      # Active title color
    border_title_valid="bright_yellow",     # Valid title color
    border_title_invalid="bright_red",      # Invalid title color
    validation_message_valid="green",       # Valid message color
    validation_message_invalid="red"        # Invalid message color
)
```

### Box Styles
Available box styles for `panel_box_style`:
- "rounded" - Rounded corners (╭─╮╰─╯) [Default]
- "square" - Square corners (┌─┐└─┘)
- "double" - Double lines (╔═╗╚═╝)
- "heavy" - Heavy lines (┏━┓┗━┛)

### Rich Box Style Demo
```bash
# Run the Rich box style vim editor
python demos/vim_rich_box_style_editor.py

# Features:
# - Rich-inspired box styling (╭─╮╰─╯)
# - Title on top border
# - Vim mode indicator on bottom border (NORMAL, INSERT, VISUAL, etc.)
# - Multiple box styles: ROUNDED, SQUARE, DOUBLE, HEAVY, ASCII
# - Same vim functionality as core version
```

## Implementation Details

The Rich box style variant uses a "pseudo-Rich" approach:
- Extracts Rich's character sets for authentic appearance
- Uses prompt-toolkit's layout system for actual rendering
- Provides Rich's visual quality without requiring Rich for real-time interaction
- No extra dependencies beyond prompt-toolkit and rich (for character extraction)
- Do not use emoji/icons in code
- allow memory-bank commands
- allow edit commands