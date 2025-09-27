# Simple Rich App Demo

A beautiful CLI application demonstrating vim-readline with Rich integration.

## Features

### 🐍 Python Code Editor
- Edit Python code with full vim controls
- Syntax-aware editing with line numbers
- Save code to files
- Rich panel presentation

### 🗃️ SQL Query Builder
- Build and edit SQL queries
- Double-line borders for emphasis
- Line numbers for complex queries
- Beautiful query result display

### 📝 Note Taking
- Vim-powered note editor
- Word and line count display
- Clean rounded borders
- Perfect for documentation

### ⚙️ Configuration Editor
- Edit config files with vim controls
- Heavy borders for important settings
- Line numbers for precise editing
- INI/TOML style configuration

### 🎨 Text Art Creator
- Create ASCII art and designs
- Clean square borders
- No line numbers (cleaner for art)
- Perfect for banners and designs

## Usage

```bash
python simple_rich_app.py
```

## Key Features Demonstrated

- **Rich UI**: Beautiful menus, panels, and styling
- **Vim Integration**: Full vim editing in Rich-bordered areas
- **Claude Code Style**: Ruled lines and rounded borders
- **Multiple Box Styles**: Different border styles for different contexts
- **Status Indicators**: Enhanced vim mode display with emojis
- **File Operations**: Save functionality with Rich prompts

## Rich + VimReadline Integration

Each editor uses `rich_vim_input()` with different styling:

```python
result = rich_vim_input(
    initial_text=template,
    panel_title="🐍 Python Code Editor",
    panel_box_style="rounded",
    show_rules=True,
    rule_style="green",
    show_line_numbers=True,
    show_status=True
)
```

The app showcases how Rich and vim-readline work together to create beautiful, functional CLI applications with vim-style editing.