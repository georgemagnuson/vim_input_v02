# Textual Integration Research

## Overview

This document contains research findings on integrating VimReadline functionality with the Textual TUI framework, exploring the possibility of creating a VimReadline widget for Textual applications.

## Key Research Questions

1. Can Rich's input() function replace VimReadline? **Answer: No**
2. Can Textual's input system replace VimReadline? **Answer: Not directly**
3. Can we create a VimReadline widget for Textual? **Answer: Yes, feasible**

## Rich Input System Analysis

### Rich's Input Architecture
- Built on Python's standard `input()` function
- **Single-line prompts only** with validation
- Zero dependencies on prompt-toolkit or advanced input libraries
- Uses basic readline if available, but no modal editing capabilities

### Fundamental Limitations for Vim Integration
- **Single-line only** - Cannot handle multiline text buffers
- **No vim modes** - No support for normal/insert/visual modes
- **No advanced editing** - No cursor positioning, text selection, or complex operations
- **Different paradigm** - Built for simple prompts, not text editors

### Integration Assessment
**Technical architecture makes direct integration impossible:**
- Rich input: Single-line, blocking, built on `input()`
- VimReadline: Multiline, modal, built on prompt-toolkit

## Textual TUI Framework Analysis

### Textual's Input System

#### TextArea Widget
- ✅ **Multiline text editing**
- ✅ **Syntax highlighting**
- ✅ **Undo/redo**
- ✅ **Line numbers**
- ✅ **Selection, copy/paste**
- ✅ **Customizable themes**

#### Input Widget
- **Single-line input** only
- ✅ **Validation support**
- ✅ **Custom key bindings**
- ✅ **Password masking**

### Critical Limitations for Vim Replacement

#### No Native Vim Modes
- Textual has **no built-in vim mode support**
- No normal/insert/visual modes out of the box
- Standard text editing only (like most GUI text areas)

#### Modal Editing Challenges
- Key binding system allows **dynamic remapping**
- But requires **manual implementation** of modal editing logic
- No established patterns for vim-like modes

### Textual Vim Extended Project
- Third-party plugin attempting to add vim modes
- **Early stage** development
- Limited documentation and examples
- **Not production-ready**

### Comparison with VimReadline

| Feature | VimReadline | Textual |
|---------|-------------|---------|
| **Vim Modes** | ✅ Full native support | ❌ Manual implementation required |
| **Modal Editing** | ✅ Built on prompt-toolkit | ❌ Custom binding management |
| **Production Ready** | ✅ Mature, tested | ⚠️ Experimental vim support |
| **Integration** | ✅ Works with Rich styling | ✅ Native Rich integration |
| **Complexity** | ✅ Simple API | ❌ Complex TUI app framework |

## Textual Widget Development Research

### Creating Custom Widgets

#### Widget Architecture
- Extend base classes like `Widget`, `Static`, or `ScrollView`
- Implement key methods like `render()` or `render_line()`
- Use `DEFAULT_CSS` to define default styling
- Support CSS styling and component classes

#### Event Handling and Key Bindings
```python
class Counter(Static, can_focus=True):
    BINDINGS = [
        ("up", "change_count(1)", "Increment"),
        ("down", "change_count(-1)", "Decrement")
    ]
    def action_change_count(self, amount: int):
        self.count += amount
```

#### Reactive System
```python
count = reactive(0)  # Auto-updating attributes
```

### Event System for Vim-like Key Handling

#### Key Event Processing
```python
def on_key(self, event: events.Key) -> None:
    if event.key == 'j':
        # Handle 'j' key press
```

#### Modal Key Handling Pattern
```python
def on_key(self, event: events.Key) -> None:
    if self.mode == 'normal':
        # Normal mode key handling
    elif self.mode == 'insert':
        # Insert mode key handling
```

## Technical Feasibility Assessment

### Architecture Conflicts & Solutions

#### Potential Issues
- **Terminal Control Conflict**: Both Textual and prompt-toolkit want to control the terminal
- **Event Loop Competition**: Different async frameworks may conflict
- **Input Handling Overlap**: Both frameworks capture keyboard input

#### Solution Approaches

##### 1. Event Translation Approach (Recommended)
```python
class VimReadlineWidget(Widget):
    """
    Textual widget that implements vim editing using Textual's event system
    """

    def __init__(self):
        super().__init__()
        self.vim_state = VimState()  # Track vim modes
        self.buffer = TextBuffer()   # Text content
        self.cursor = CursorState()  # Cursor position

    def on_key(self, event: events.Key) -> None:
        """Translate Textual key events to vim commands"""
        if self.vim_state.mode == "normal":
            self._handle_normal_mode(event)
        elif self.vim_state.mode == "insert":
            self._handle_insert_mode(event)
```

##### 2. Embedded prompt-toolkit Approach (Complex)
```python
class EmbeddedVimWidget(Widget):
    """
    Embed a prompt-toolkit session within Textual widget
    """

    async def _run_embedded_vim(self):
        """Run prompt-toolkit in a separate thread/context"""
        # Careful terminal state management required
        result = await run_vim_readline_async()
        self.post_message(VimEditComplete(result))
```

## Recommended Implementation Strategy

### Approach 1: Pure Textual Implementation

#### Advantages
- Native Textual integration
- No framework conflicts
- Leverages Textual's event system
- Full control over rendering

#### Implementation Plan
```python
from textual.widget import Widget
from textual import events
from textual.reactive import reactive

class VimReadlineWidget(Widget):
    DEFAULT_CSS = """
    VimReadlineWidget {
        border: solid;
    }
    """

    # Reactive attributes
    mode = reactive("normal")  # normal, insert, visual
    content = reactive("")
    cursor_line = reactive(0)
    cursor_col = reactive(0)

    # Vim state
    BINDINGS = [
        ("escape", "set_normal_mode", "Normal mode"),
        ("i", "set_insert_mode", "Insert mode"),
        # Add all vim bindings
    ]

    def render(self) -> RenderResult:
        """Render vim editor with mode indicators"""
        return self._render_vim_buffer()

    def on_key(self, event: events.Key) -> None:
        """Handle vim key commands"""
        if self.mode == "normal":
            self._handle_normal_key(event.key)
        elif self.mode == "insert":
            self._handle_insert_key(event.key)

    def _handle_normal_key(self, key: str):
        """Implement vim normal mode commands"""
        if key == "j":
            self.cursor_line += 1
        elif key == "k":
            self.cursor_line -= 1
```

### Approach 2: Validation Integration
```python
class ValidatedVimWidget(VimReadlineWidget):
    """Add validation to vim widget"""

    validator = reactive(None)
    is_valid = reactive(True)

    def validate_content(self):
        """Validate current content"""
        if self.validator:
            self.is_valid = self.validator.validate(self.content)

    def render(self) -> RenderResult:
        """Render with validation state colors"""
        style = "valid" if self.is_valid else "invalid"
        return Panel(
            self._render_vim_buffer(),
            border_style=style
        )
```

### Approach 3: Hybrid Integration
```python
class TextualVimApp(App):
    """Textual app that uses VimReadline for editing"""

    def action_open_vim_editor(self):
        """Open VimReadline in modal overlay"""
        vim_result = await self.run_vim_session()
        self.update_content(vim_result)

    async def run_vim_session(self):
        """Run VimReadline externally and capture result"""
        # Temporarily suspend Textual
        with self.app.suspend():
            vim_readline = VimReadline(...)
            return vim_readline.run()
```

## Current Rich + VimReadline Integration Patterns

Your codebase already demonstrates excellent patterns for combining Rich display with ValidatedRichVimReadline input:

### 1. Pre/Post Display Pattern
- Rich panels for **preview** before editing
- ValidatedRichVimReadline for **actual input**
- Rich panels for **results** after editing
- Clean separation of concerns

### 2. Workspace Pattern
- Rich workspace introduction and navigation
- Multiple ValidatedRichVimReadline sessions
- Rich summary and statistics display

### 3. Demo Integration Pattern
- Rich preview with instructions
- Standard vim editing session
- Rich results with statistics

## Conclusions

### Rich Input Integration
**Rich cannot directly replace VimReadline** because:
1. **Architecture mismatch** - Rich input is single-line/blocking vs VimReadline's multiline/modal design
2. **Feature gap** - Rich lacks vim modes, text buffers, and advanced editing capabilities
3. **Design philosophy** - Rich input is for simple prompts, not text editors

**Your current ValidatedRichVimReadline approach is already optimal** - it leverages Rich's strengths (styling, theming, borders) while using prompt-toolkit for the complex vim functionality that Rich cannot provide.

### Textual Integration
**Textual cannot directly replace VimReadline** because:
1. **No native vim mode** - Would require significant custom implementation
2. **Different paradigm** - Textual is for full TUI apps, not simple input
3. **Complexity overhead** - Building a Textual app for simple text input is overkill
4. **Experimental vim support** - Third-party plugins are not mature

### VimReadline Widget for Textual
**✅ FEASIBLE** - Creating a VimReadline widget for Textual is technically possible and recommended:

#### Best Approach
Create a **pure Textual VimReadline widget** that:
1. **Reimplements vim logic** using Textual's event system
2. **Integrates seamlessly** with Textual apps
3. **Supports validation** like your current ValidatedRichVimReadline
4. **Avoids framework conflicts** by staying within Textual ecosystem

#### Benefits
- ✅ Full vim functionality within Textual
- ✅ Native Textual styling and theming
- ✅ No terminal control conflicts
- ✅ Validation and Rich-style features
- ✅ Reusable widget for any Textual app

#### Implementation Effort
**Moderate** - requires translating vim command logic to Textual's event system, but very achievable and would be a valuable addition to the Textual ecosystem.

## Next Steps

1. **Maintain current approach** for standalone vim input (ValidatedRichVimReadline)
2. **Consider Textual widget development** for TUI applications that need vim editing
3. **Leverage Rich for display/presentation** while keeping prompt-toolkit for vim functionality
4. **Explore hybrid patterns** that combine Rich display + VimReadline input + Textual apps

## References

- [Textual Documentation](https://textual.textualize.io/)
- [Rich Documentation](https://rich.readthedocs.io/)
- [prompt-toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/)
- [Textual Vim Extended Project](https://vedantasati.me/projects/textual-vim-extended/)