# Running Rich Interactive Demos 🚀

## ✅ **Recommended Ways to Run Demos**

### **1. Standalone Demo (No Import Issues)**
```bash
python demo_rich_standalone.py
```
- ✅ Works immediately
- ✅ Shows all Rich box styles
- ✅ No relative import problems
- ✅ Complete Rich capabilities demo

### **2. Complete Interactive Demo**
```bash
python demo_rich_interactive_complete.py
```
- 🎨 Full Rich + vim integration demo
- 📦 Multiple implementation approaches
- 🎯 Interactive editing sessions
- ✨ Professional workspace demo

### **3. Using as Python Module**
```python
# From Python script or interactive session
from vim_readline import rich_vim_input, RichVimWorkspace

# Basic Rich integration
result = rich_vim_input(
    box_title="My Rich Editor",
    rich_box_style="ROUNDED",
    initial_text="Hello Rich + Vim!"
)

# Advanced workspace
workspace = RichVimWorkspace("My Workspace")
session = workspace.create_editing_session(
    box_title="Code Editor",
    rich_box_style="DOUBLE"
)
```

### **4. Individual Module Testing**
```bash
# Test Rich box rendering directly
python -c "
import sys; sys.path.insert(0, '.')
from vim_readline.rich_box_native import demo_rich_native_direct
demo_rich_native_direct()
"
```

## ❌ **Avoid These (Relative Import Issues)**

### **Don't Run Module Files Directly**
```bash
# ❌ This will fail with relative import error:
python vim_readline/rich_box_native.py

# ❌ This will also fail:
cd vim_readline && python rich_box_native.py
```

**Why it fails:**
- Python modules with relative imports (like `from .core import VimReadline`)
- Cannot be run directly as scripts
- They need to be imported as part of a package

## 🎨 **Rich Interactive Features You Can Test**

### **Rich Box Styles Available:**
- `ROUNDED` - Rich's signature rounded corners (╭─╮╰─╯)
- `SQUARE` - Clean square corners (┌─┐└─┘)
- `DOUBLE` - Double lines for emphasis (╔═╗╚═╝)
- `HEAVY` - Bold, thick lines (┏━┓┗━┛)
- `ASCII` - ASCII-only compatibility (+-++-+)
- `MINIMAL` - Clean minimal style
- `SIMPLE` - Basic clean lines
- `SIMPLE_HEAVY` - Heavy horizontal lines

### **Interactive Demos Include:**
- 🎯 Rich box style comparisons
- ⚡ Rich vs manual border drawing
- 🔧 Rich + vim integration concepts
- 📊 Professional terminal interfaces
- 🚀 Multi-session workspace demos

## 📝 **Quick Start Examples**

### **Simple Rich Input**
```python
from vim_readline import rich_vim_input

text = rich_vim_input(
    box_title="Quick Note",
    rich_box_style="ROUNDED"
)
```

### **Professional Editor**
```python
from vim_readline import RichPromptIntegration

editor = RichPromptIntegration(
    box_title="Code Editor",
    rich_box_style="SQUARE",
    box_width=80,
    show_rich_preview=True,
    show_rich_result=True
)

result = editor.run()
```

### **Development Workspace**
```python
from vim_readline import RichVimWorkspace

workspace = RichVimWorkspace("Development Environment")
workspace.run_demo_sessions()
```

## 🎉 **Summary**

**For immediate testing:** Run `python demo_rich_standalone.py`

**For full experience:** Run `python demo_rich_interactive_complete.py`

**For development:** Import from the main package: `from vim_readline import rich_vim_input`

The Rich Interactive ecosystem provides beautiful, professional terminal interfaces with zero alignment issues thanks to Rich's proven box rendering system! 🎨✨