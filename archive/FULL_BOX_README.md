# Full Box VimReadline - Complete Border Implementation

This implementation creates a **complete drawn box** around the text input area, exactly like the screenshot you showed with "Type entry" borders.

## Features

✅ **Complete Box Borders** - Draws full borders on all sides
✅ **Title Support** - Shows titles in the top border
✅ **Multiple Border Styles** - Rounded, square, double, heavy
✅ **Auto-sizing** - Adapts to terminal dimensions
✅ **Full Vim Mode Support** - All vim commands work within the box

## Visual Examples

### Rounded Style (like screenshot)
```
┌─── Type entry ────────┐
│ Your text content    │
│ goes here...         │
│                      │
└──────────────────────┘
```

### Square Style
```
┌─── Code Input ───────┐
│ def example():       │
│     # Your code      │
│     pass             │
└──────────────────────┘
```

### Double Style
```
╔═══ Important Note ═══╗
║ This is emphasized   ║
║ content with double  ║
║ line borders         ║
╚══════════════════════╝
```

### Heavy Style
```
┏━━━ Bold Input ━━━━━━━┓
┃ Heavy borders for   ┃
┃ maximum emphasis    ┃
┃                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━┛
```

## Usage

### Simple Usage
```python
from vim_readline import full_box_vim_input

result = full_box_vim_input(
    initial_text="Type your content here...",
    box_title="Type entry",
    box_width=60,
    box_height=10
)
```

### Advanced Usage
```python
from vim_readline import FullBoxVimReadline

editor = FullBoxVimReadline(
    initial_text="Your content...",
    box_title="Custom Title",
    box_width=70,
    box_height=15,
    border_style="rounded",    # "rounded", "square", "double", "heavy"
    auto_size=True,           # Auto-fit to terminal
    show_line_numbers=True,
    show_status=True,
    wrap_lines=True
)

result = editor.run()
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `box_title` | str | `""` | Title shown in top border |
| `box_width` | int | `60` | Width of the box |
| `box_height` | int | `10` | Height of text area |
| `border_style` | str | `"rounded"` | Border style: rounded, square, double, heavy |
| `auto_size` | bool | `True` | Auto-fit to terminal dimensions |
| `show_line_numbers` | bool | `False` | Show line numbers inside box |
| `show_status` | bool | `True` | Show vim mode status |
| `wrap_lines` | bool | `True` | Wrap long lines within box |

## Border Styles

### Available Styles
- **`"rounded"`** - Standard rounded corners (┌─┐ │ └─┘)
- **`"square"`** - Clean square corners (┌─┐ │ └─┘)
- **`"double"`** - Double-line borders (╔═╗ ║ ╚═╝)
- **`"heavy"`** - Heavy/thick borders (┏━┓ ┃ ┗━┛)

## Key Features

### 1. Complete Border Drawing
Unlike other implementations, this draws **complete borders** on all four sides, creating a true "box" around your text.

### 2. Title Integration
Titles are embedded directly into the top border:
```
┌─── Your Title ────┐
│ content area      │
└───────────────────┘
```

### 3. Text Constraint
Text is **properly constrained** within the box boundaries:
- Long lines wrap within the box width
- Text cannot exceed the box dimensions
- Scrolling works when content is larger than the box

### 4. Auto-sizing
When `auto_size=True`, the box automatically adjusts to fit your terminal while respecting the maximum dimensions you specify.

## Vim Mode Support

All standard vim commands work within the box:

- **ESC** - Normal mode
- **i** - Insert mode
- **a** - Append
- **o** - New line below
- **A** - Append at end of line
- **Visual modes** - v, V, Ctrl-V
- **Navigation** - h, j, k, l, w, b, etc.
- **Editing** - d, c, y, p, etc.

## Examples

### Basic Text Entry (like screenshot)
```python
result = full_box_vim_input(
    box_title="Type entry",
    box_width=50,
    box_height=8,
    border_style="rounded"
)
```

### Code Editor Box
```python
result = full_box_vim_input(
    initial_text="def example():\n    pass",
    box_title="Code Input",
    box_width=70,
    box_height=15,
    border_style="square",
    show_line_numbers=True
)
```

### Important Message Box
```python
result = full_box_vim_input(
    placeholder_text="Enter important information...",
    box_title="Important",
    box_width=60,
    box_height=8,
    border_style="double"
)
```

## Implementation Details

This implementation uses pyvim-style window management to create true boundary constraints:

1. **Fixed Dimensions** - Uses `Dimension(min=X, max=X, preferred=X)` to create exact sizing
2. **Border Components** - Creates separate Window components for each border section
3. **Text Constraint** - The text area is slightly smaller than the box to account for borders
4. **Layout Hierarchy** - Uses HSplit/VSplit to compose the complete bordered layout

The result is a text input that behaves exactly like the screenshot - complete borders with properly constrained text editing inside.