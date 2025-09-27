# Vim-Rich Interactive Demos

This directory contains the main working demos for vim editing inside Rich boxes.

## 🎯 Main Demo (Recommended)

**`vim_rich_box_style_editor.py`** - The complete solution!
```bash
python demos/vim_rich_box_style_editor.py
```

✅ **Vim editor with Rich box style appearance**
✅ **No extra dependencies** (uses prompt-toolkit styled with Rich characters)
✅ **Title on top border, mode on bottom border**
✅ **All vim modes: NORMAL, INSERT, VISUAL, etc.**

Visual appearance:
```
╭────────── Vim Inside ROUNDED Rich Box ──────────╮
│ # Your vim editing happens here                 │
│                                                 │
│ def example():                                  │
│     return "editing inside Rich boundaries"     │
│                                                 │
╰ INSERT ─────────────────────────────────────────╯
```

## 🚀 Alternative Demos

**`demo_complete_rich_solution.py`** - Shows all approaches
- Demonstrates the problem and multiple solutions
- Good for understanding the evolution to the final solution

**`interactive_rich_demo.py`** - Basic Rich interactive editor
- Simple text editing inside Rich boxes (not vim)
- Shows the concept without vim complexity

**`vim_rich_prompt.py`** - Rich-styled vim interface
- Full vim functionality with Rich preview/results
- Editing happens in prompt-toolkit, Rich for display only

## 🎮 Usage

All demos are self-contained:
```bash
cd demos
python vim_rich_box_style_editor.py  # Main solution
python [other_demo_name].py          # Other demos
```

## 🎨 Rich Box Styles

All demos support multiple Rich box styles:
- ROUNDED (default) - `╭─╮╰─╯`
- SQUARE - `┌─┐└─┘`
- DOUBLE - `╔═╗╚═╝`
- HEAVY - `┏━┓┗━┛`
- ASCII - `+--++--+`

The main solution (`vim_rich_box_style_editor.py`) is the complete vim editor styled to look like Rich boxes with no extra dependencies!