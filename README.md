# VimReadline

A vim-mode readline implementation for single-buffer text editing, built on `prompt-toolkit`. Perfect for interactive applications that need vim-style text input without file I/O operations.

Available in two variants:
- **Core VimReadline**: Clean, minimal vim text editor
- **Rich Box Style**: Same vim functionality with beautiful Rich-inspired box styling

## Features

- **Full vim navigation modes**: normal, insert, visual, replace
- **Configurable key bindings**: Return to submit, Ctrl-J/Shift-Return for newline
- **Cursor shape changes**: beam (insert), block (normal), underline (replace)
- **Optional UI elements**: line numbers, status indicators ("-- INSERT --")
- **Flexible text handling**: initial text (editable) or placeholder text (hint)
- **No file I/O**: pure in-memory text buffer editing
- **Terminal agnostic**: works across different terminal environments

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

### Rich Box Style VimReadline
```python
# Run the Rich box style demo
python demos/vim_rich_box_style_editor.py

# Features Rich-inspired box styling with:
# - Title on top border
# - Vim mode indicator on bottom border
# - Multiple box styles (ROUNDED, SQUARE, DOUBLE, HEAVY, ASCII)
# - Same vim functionality as core version
```

## Advanced Usage

```python
from vim_readline import VimReadline

# Full configuration
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

## Examples

Run the interactive examples:

```bash
# Core VimReadline demo (when available)
vim-readline-demo

# Rich Box Style demo
python demos/vim_rich_box_style_editor.py

# Other demos
python demos/demo_complete_rich_solution.py
python demos/interactive_rich_demo.py
```

## Use Cases

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

### Rich Box Style Interfaces
```python
# For applications requiring professional appearance
# Use the Rich Box Style variant:

python demos/vim_rich_box_style_editor.py

# Visual appearance:
# ╭───────── Code Editor ─────────╮
# │ def main():                   │
# │     print("Hello, World!")    │
# │                               │
# ╰ INSERT ──────────────────────╯
```

### Configuration Editing
```python
from vim_readline import VimReadline

def edit_config(current_config):
    editor = VimReadline(
        initial_text=current_config,
        show_line_numbers=True,
        prompt="config> "
    )

    return editor.run()
```

## API Reference

### `vim_input()`
Simple function interface for quick usage.

**Parameters:**
- `prompt` (str): Prompt text shown at start of lines
- `initial_text` (str): Pre-populated editable content
- `placeholder_text` (str): Hint text when buffer is empty
- `show_line_numbers` (bool): Display line numbers
- `show_status` (bool): Show vim mode status
- `wrap_lines` (bool): Enable line wrapping

**Returns:** `str` or `None` (if cancelled)

### `VimReadline` Class
Full-featured class for advanced usage.

**Constructor Parameters:**
- `initial_text` (str): Pre-populated content
- `placeholder_text` (str): Placeholder hint text
- `prompt` (str): Line prompt text
- `show_line_numbers` (bool): Display line numbers
- `show_status` (bool): Show mode indicators
- `wrap_lines` (bool): Enable line wrapping
- `submit_key` (str): Key binding for submit (default: 'c-m')
- `newline_key` (str): Key binding for newline (default: 'c-j')
- `cancel_keys` (list): Key bindings for cancel (default: ['c-c', 'c-d'])

**Methods:**
- `run()` → `str | None`: Run the interface and return result

## Project Structure

```
vim_input_v02/
├── vim_readline/           # Core VimReadline library
│   ├── core.py            # Main VimReadline implementation
│   └── ...                # Supporting modules
├── demos/                 # Interactive demonstrations
│   ├── vim_rich_box_style_editor.py  # Rich box style vim editor
│   ├── demo_complete_rich_solution.py
│   └── ...
├── tests/                 # Test suite
└── archive/              # Development history and experiments
```

## Variants

### 1. Core VimReadline
- **Location**: `vim_readline/core.py`
- **Style**: Clean, minimal interface
- **Usage**: `from vim_readline import vim_input`
- **Best for**: Embedded use in applications, simple interfaces

### 2. Rich Box Style VimReadline
- **Location**: `demos/vim_rich_box_style_editor.py`
- **Style**: Rich-inspired box styling with borders and mode indicators
- **Usage**: `python demos/vim_rich_box_style_editor.py`
- **Best for**: Standalone editors, professional appearance, demonstrations

Both variants provide identical vim functionality - the difference is visual presentation.

## Requirements

- Python 3.7+
- prompt-toolkit >= 3.0.0
- rich (for Rich box style variant)

## License

MIT License

## Contributing

Issues and pull requests welcome! This project was generated with Claude Code.