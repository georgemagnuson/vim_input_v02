"""
Interactive Rich Box App - Full Rich application with vim editing capabilities.

This creates a complete Rich application that handles both the UI rendering
and the interactive vim-style text editing within Rich panels.
"""

from .core import VimReadline as BaseVimReadline
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig

# Rich imports
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box
from rich.layout import Layout as RichLayout
from rich.align import Align
import asyncio
import threading
import time


class RichInteractiveBoxApp:
    """
    A complete Rich application that provides vim-style editing within Rich panels.

    This combines:
    - Rich's beautiful rendering and panel system
    - prompt-toolkit's vim editing capabilities
    - Real-time updates using Rich Live
    - Interactive terminal application
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 box_title="",
                 box_width=60,
                 box_height=10,
                 rich_box_style="ROUNDED",
                 show_status=True,
                 show_line_numbers=False,
                 submit_key='c-m',
                 newline_key='c-j',
                 cancel_keys=None):

        if cancel_keys is None:
            cancel_keys = ['c-c', 'c-d']

        # Configuration
        self.initial_text = initial_text
        self.placeholder_text = placeholder_text
        self.box_title = box_title
        self.box_width = box_width
        self.box_height = box_height
        self.rich_box_style = rich_box_style
        self.show_status = show_status
        self.show_line_numbers = show_line_numbers
        self.submit_key = submit_key
        self.newline_key = newline_key
        self.cancel_keys = cancel_keys

        # Rich box styles
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII,
            "MINIMAL": box.MINIMAL,
            "SIMPLE": box.SIMPLE,
            "SIMPLE_HEAVY": box.SIMPLE_HEAVY,
        }

        # State
        self._result = None
        self._cancelled = False
        self._running = False

        # Rich console and live display
        self.console = Console()
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # Initialize buffer and application
        self._setup_buffer()
        self._setup_application()

    def _setup_buffer(self):
        """Set up the text buffer."""
        self.buffer = Buffer(
            document=None,
            multiline=True,
            read_only=False
        )

        if self.initial_text:
            self.buffer.text = self.initial_text
            self.buffer.cursor_position = len(self.initial_text)
        elif self.placeholder_text:
            self.buffer.text = self.placeholder_text
            # Could implement placeholder clearing logic here

    def _setup_application(self):
        """Set up the prompt-toolkit application for vim editing."""

        # Create key bindings
        kb = KeyBindings()

        @kb.add(self.submit_key)
        def submit(event):
            self._result = self.buffer.text
            self._running = False
            event.app.exit()

        @kb.add(self.newline_key)
        def newline(event):
            event.current_buffer.insert_text('\n')

        for cancel_key in self.cancel_keys:
            @kb.add(cancel_key)
            def cancel(event):
                self._cancelled = True
                self._running = False
                event.app.exit()

        # Create simple layout for the editing component
        # The Rich rendering will handle the visual display
        buffer_control = BufferControl(buffer=self.buffer)

        self.app = Application(
            layout=Layout(Window(buffer_control, wrap_lines=True)),
            editing_mode=EditingMode.VI,
            key_bindings=kb,
            cursor=ModalCursorShapeConfig(),
            full_screen=False,
            mouse_support=False  # Keep it simple for text editing
        )

    def _create_rich_panel(self):
        """Create the Rich panel with current buffer content."""

        # Get current text from buffer
        text_content = self.buffer.text

        # Add line numbers if requested
        if self.show_line_numbers:
            lines = text_content.split('\n') if text_content else ['']
            numbered_lines = []
            width = len(str(len(lines)))

            for i, line in enumerate(lines):
                line_num = str(i + 1).rjust(width)
                numbered_lines.append(f"{line_num} │ {line}")

            display_content = '\n'.join(numbered_lines)
        else:
            display_content = text_content or self.placeholder_text

        # Create Rich panel
        panel = Panel(
            display_content,
            title=self.box_title if self.box_title else None,
            box=self.rich_box,
            width=self.box_width,
            height=self.box_height + 2,  # +2 for borders
            expand=False
        )

        return panel

    def _create_status_display(self):
        """Create status information display."""
        if not self.show_status:
            return ""

        # Get vim mode info
        if hasattr(self.app, 'vi_state') and self.app.vi_state:
            mode = self.app.vi_state.input_mode
            if mode == 'vi-insert':
                status = "-- INSERT --"
            elif mode == 'vi-replace':
                status = "-- REPLACE --"
            elif mode == 'vi-navigation':
                # Check for visual mode
                selection = self.buffer.selection_state
                if selection:
                    from prompt_toolkit.selection import SelectionType
                    if selection.type == SelectionType.LINES:
                        status = "-- VISUAL LINE --"
                    elif selection.type == SelectionType.BLOCK:
                        status = "-- VISUAL BLOCK --"
                    else:
                        status = "-- VISUAL --"
                else:
                    status = "-- NORMAL --"
            else:
                status = f"-- {mode.upper()} --"
        else:
            status = "-- NORMAL --"

        return status

    def _create_full_display(self):
        """Create the complete Rich display."""

        # Main panel
        panel = self._create_rich_panel()

        # Status
        status = self._create_status_display()

        # Instructions
        instructions = Text(
            "ESC: Normal mode | i: Insert | Return: Submit | Ctrl+C: Cancel",
            style="dim"
        )

        # Combine elements
        display_elements = [panel]

        if status:
            display_elements.append(Text(status, style="bold"))

        display_elements.append(instructions)

        # Create Rich layout
        rich_layout = RichLayout()
        rich_layout.split_column(
            *[Align.center(element) for element in display_elements]
        )

        return rich_layout

    async def _run_rich_display(self):
        """Run the Rich live display that updates the UI."""

        with Live(self._create_full_display(), console=self.console, refresh_per_second=10) as live:
            while self._running:
                # Update the display with current buffer state
                live.update(self._create_full_display())
                await asyncio.sleep(0.1)  # 10 FPS update rate

    def run(self):
        """Run the interactive Rich box application."""

        self._running = True
        self._result = None
        self._cancelled = False

        # Show initial display
        initial_display = self._create_full_display()
        self.console.print(initial_display)

        try:
            # Create event loop if one doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Start Rich display updates in background
            rich_task = asyncio.create_task(self._run_rich_display())

            # Run the prompt-toolkit application
            # Note: This is a simplified version - in practice, you'd need more
            # sophisticated integration between Rich and prompt-toolkit
            app_task = asyncio.create_task(self._run_pt_app())

            # Wait for either task to complete
            loop.run_until_complete(asyncio.gather(rich_task, app_task, return_exceptions=True))

        except (KeyboardInterrupt, EOFError):
            self._cancelled = True
        finally:
            self._running = False

        return None if self._cancelled else self._result

    async def _run_pt_app(self):
        """Run the prompt-toolkit application asynchronously."""
        # This is a simplified integration
        # In practice, you'd need more sophisticated async integration
        self.app.run()


class SimpleRichBoxApp:
    """
    Simplified Rich box application that shows content in Rich panels.

    This is a simpler approach that uses Rich for display but standard
    input methods for text collection.
    """

    def __init__(self,
                 initial_text="",
                 box_title="Rich Input",
                 box_width=60,
                 box_height=10,
                 rich_box_style="ROUNDED"):

        self.initial_text = initial_text
        self.box_title = box_title
        self.box_width = box_width
        self.box_height = box_height

        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII,
        }

        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)
        self.console = Console()

    def show_input_box(self, content=""):
        """Display the input box with given content."""

        panel = Panel(
            content or self.initial_text or "Type your content here...",
            title=self.box_title,
            box=self.rich_box,
            width=self.box_width,
            height=self.box_height,
            expand=False
        )

        self.console.clear()
        self.console.print(Align.center(panel))

    def run_interactive_demo(self):
        """Run an interactive demo showing Rich box capabilities."""

        self.console.print("\n🎨 Rich Interactive Box Demo", style="bold blue")
        self.console.print("=" * 50)

        # Show different box styles
        styles = [
            ("ROUNDED", "Rich's signature rounded corners"),
            ("SQUARE", "Clean square corners"),
            ("DOUBLE", "Double-line emphasis"),
            ("HEAVY", "Bold, thick lines"),
            ("ASCII", "Maximum compatibility"),
        ]

        for style_name, description in styles:
            self.console.print(f"\n📦 {style_name}: {description}")

            # Create panel with this style
            box_style = self.rich_box_styles[style_name]
            panel = Panel(
                f"This is a {style_name.lower()} box demonstration.\n\nIt shows how Rich handles beautiful\nbox rendering automatically!",
                title=f"{style_name} Demo",
                box=box_style,
                width=50,
                expand=False
            )

            self.console.print(Align.center(panel))

            if style_name != styles[-1][0]:  # Not the last one
                input("\nPress Enter to see next style...")

        self.console.print("\n✨ Rich provides perfect box rendering out of the box!")


# Convenience functions
def rich_interactive_box_input(**kwargs):
    """Create an interactive Rich box for text input."""
    app = RichInteractiveBoxApp(**kwargs)
    return app.run()


def demo_rich_interactive_boxes():
    """Demo function showing Rich interactive box capabilities."""
    app = SimpleRichBoxApp()
    app.run_interactive_demo()


if __name__ == "__main__":
    demo_rich_interactive_boxes()