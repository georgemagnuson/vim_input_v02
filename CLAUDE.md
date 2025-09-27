# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VimReadline** - A vim-mode readline implementation for single-buffer text editing without file I/O, based on `prompt-toolkit`.

Available in multiple variants:
- **Core VimReadline**: Clean, minimal vim text editor (`vim_readline/core.py`)
- **ValidatedVimReadline**: Core functionality plus input validation and hidden input (`vim_readline/validated.py`)
- **Rich Box Style**: Same vim functionality with Rich-inspired box styling (`demos/vim_rich_box_style_editor.py`)

## Key Features

- Full vim navigation modes (normal/insert/visual/replace)
- Configurable submit keys (Return to submit, Ctrl-J/Shift-Return for newline)
- Cursor shape changes by mode (beam/block/underline)
- Optional line numbers and status indicators ("-- INSERT --")
- Support for both initial_text (editable) and placeholder_text (hint)
- **Input validation**: Email, date, integer, float, regex, length, custom validators
- **Hidden input**: Password masking with configurable characters
- **Real-time validation feedback**: Visual error messages and status indicators
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
- `vim_readline/core.py`: Main VimReadline implementation
- `vim_readline/validated.py`: ValidatedVimReadline with input validation
- `vim_readline/validators.py`: Validation system and built-in validators
- `vim_readline/__init__.py`: Package interface

### Demos
- `demos/vim_rich_box_style_editor.py`: Rich box style vim editor (main demo)
- `demos/validation_demos.py`: Comprehensive validation feature demos
- `demos/quick_validation_example.py`: Simple validation usage example
- `demos/demo_complete_rich_solution.py`: Shows all solution approaches
- `demos/interactive_rich_demo.py`: Basic Rich interactive editor

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

### ValidatedVimReadline
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
# Run comprehensive validation demos
python demos/validation_demos.py

# Run quick validation example
python demos/quick_validation_example.py

# Test validation system
python test_validation.py
```

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