"""
True Rich Interactive Box - Editing actually happens INSIDE the Rich box.

This implementation creates a real interactive Rich application where the
text editing and cursor movement happens within the Rich box boundaries,
not in a separate prompt-toolkit window.
"""

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import ModalCursorShapeConfig

# Rich imports for true integration
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich import box
from rich.align import Align
import asyncio
import threading
import time


class TrueRichInteractiveBox:
    """
    True Rich interactive box where editing happens INSIDE the Rich box.

    This uses Rich Live to continuously update the display, showing the
    text content with cursor position within the Rich box boundaries.
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 box_title="Interactive Box",
                 box_width=60,
                 box_height=12,
                 rich_box_style="ROUNDED",
                 submit_key='c-m',
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
        self.submit_key = submit_key
        self.cancel_keys = cancel_keys

        # Rich setup
        self.console = Console()
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII
        }
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # State
        self._result = None
        self._cancelled = False
        self._running = False
        self._current_mode = "INSERT"

        # Text editing state
        self.text_lines = (initial_text or placeholder_text or "").split('\n')
        self.cursor_row = 0
        self.cursor_col = 0
        self.is_placeholder_active = bool(placeholder_text and not initial_text)

        # Ensure we have at least one line
        if not self.text_lines:
            self.text_lines = [""]

        # Set cursor to end of text if we have initial text
        if initial_text:
            self.cursor_row = len(self.text_lines) - 1
            self.cursor_col = len(self.text_lines[self.cursor_row])

    def _create_rich_display(self):
        """Create the Rich display showing text content with cursor inside the box."""

        # Prepare text content with cursor indication
        display_lines = []
        content_height = self.box_height - 2  # Account for top/bottom borders

        # Show up to content_height lines, with scrolling if needed
        start_row = max(0, self.cursor_row - content_height + 1) if self.cursor_row >= content_height else 0
        end_row = min(start_row + content_height, len(self.text_lines))

        for i in range(content_height):
            actual_row = start_row + i

            if actual_row < len(self.text_lines):
                line_text = self.text_lines[actual_row]

                # Add cursor indication if this is the cursor row
                if actual_row == self.cursor_row:
                    if self.cursor_col <= len(line_text):
                        # Insert cursor marker
                        cursor_line = line_text[:self.cursor_col] + "│" + line_text[self.cursor_col:]
                        display_lines.append(cursor_line)
                    else:
                        # Cursor at end
                        display_lines.append(line_text + "│")
                else:
                    display_lines.append(line_text)
            else:
                # Empty line
                if actual_row == self.cursor_row:
                    display_lines.append("│")  # Cursor on empty line
                else:
                    display_lines.append("")

        # Pad lines to fit box height
        while len(display_lines) < content_height:
            display_lines.append("")

        # Truncate lines to fit box width
        content_width = self.box_width - 2  # Account for left/right borders
        for i in range(len(display_lines)):
            if len(display_lines[i]) > content_width:
                display_lines[i] = display_lines[i][:content_width]

        display_content = '\n'.join(display_lines)

        # Create the Rich panel
        panel = Panel(
            display_content,
            title=f"{self.box_title} - {self._current_mode}",
            box=self.rich_box,
            width=self.box_width,
            height=self.box_height,
            border_style="blue" if self._current_mode == "INSERT" else "green"
        )

        # Add instructions
        instructions = Text(
            "ESC: Normal mode | i: Insert | Enter: Submit | Ctrl+C: Cancel\n"
            "Arrow keys: Navigate | Type to edit",
            style="dim"
        )

        # Create layout with panel and instructions
        from rich.layout import Layout as RichLayout
        layout = RichLayout()
        layout.split_column(
            Align.center(panel),
            Align.center(instructions)
        )

        return layout

    def _handle_key_input(self, key_name):
        """Handle key input for editing inside the Rich box."""

        if key_name in self.cancel_keys:
            self._cancelled = True
            self._running = False
            return

        if key_name == self.submit_key:
            self._result = '\n'.join(self.text_lines)
            self._running = False
            return

        # Clear placeholder if active
        if self.is_placeholder_active:
            self.text_lines = [""]
            self.cursor_row = 0
            self.cursor_col = 0
            self.is_placeholder_active = False

        # Handle navigation
        if key_name == 'up':
            if self.cursor_row > 0:
                self.cursor_row -= 1
                self.cursor_col = min(self.cursor_col, len(self.text_lines[self.cursor_row]))
        elif key_name == 'down':
            if self.cursor_row < len(self.text_lines) - 1:
                self.cursor_row += 1
                self.cursor_col = min(self.cursor_col, len(self.text_lines[self.cursor_row]))
        elif key_name == 'left':
            if self.cursor_col > 0:
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                self.cursor_row -= 1
                self.cursor_col = len(self.text_lines[self.cursor_row])
        elif key_name == 'right':
            if self.cursor_col < len(self.text_lines[self.cursor_row]):
                self.cursor_col += 1
            elif self.cursor_row < len(self.text_lines) - 1:
                self.cursor_row += 1
                self.cursor_col = 0

        # Handle editing
        elif key_name == 'enter' or key_name == 'c-j':
            # Split line at cursor
            current_line = self.text_lines[self.cursor_row]
            left_part = current_line[:self.cursor_col]
            right_part = current_line[self.cursor_col:]

            self.text_lines[self.cursor_row] = left_part
            self.text_lines.insert(self.cursor_row + 1, right_part)
            self.cursor_row += 1
            self.cursor_col = 0

        elif key_name == 'backspace':
            if self.cursor_col > 0:
                # Delete character before cursor
                line = self.text_lines[self.cursor_row]
                self.text_lines[self.cursor_row] = line[:self.cursor_col-1] + line[self.cursor_col:]
                self.cursor_col -= 1
            elif self.cursor_row > 0:
                # Join with previous line
                current_line = self.text_lines[self.cursor_row]
                previous_line = self.text_lines[self.cursor_row - 1]
                self.cursor_col = len(previous_line)
                self.text_lines[self.cursor_row - 1] = previous_line + current_line
                del self.text_lines[self.cursor_row]
                self.cursor_row -= 1

        elif key_name == 'delete':
            line = self.text_lines[self.cursor_row]
            if self.cursor_col < len(line):
                self.text_lines[self.cursor_row] = line[:self.cursor_col] + line[self.cursor_col+1:]
            elif self.cursor_row < len(self.text_lines) - 1:
                # Join with next line
                next_line = self.text_lines[self.cursor_row + 1]
                self.text_lines[self.cursor_row] += next_line
                del self.text_lines[self.cursor_row + 1]

        # Handle vim mode switching
        elif key_name == 'escape':
            self._current_mode = "NORMAL" if self._current_mode == "INSERT" else "NORMAL"
        elif key_name == 'i' and self._current_mode == "NORMAL":
            self._current_mode = "INSERT"

        # Handle regular character input
        elif len(key_name) == 1 and key_name.isprintable():
            line = self.text_lines[self.cursor_row]
            self.text_lines[self.cursor_row] = line[:self.cursor_col] + key_name + line[self.cursor_col:]
            self.cursor_col += 1

    def run_with_keyboard_input(self):
        """Run the Rich interactive box with keyboard input handling."""

        self._running = True

        try:
            import keyboard

            with Live(self._create_rich_display(), console=self.console, refresh_per_second=30) as live:

                def on_key_event(event):
                    if not self._running:
                        return

                    if event.event_type == keyboard.KEY_DOWN:
                        key_name = event.name
                        self._handle_key_input(key_name)

                        if self._running:
                            live.update(self._create_rich_display())
                        else:
                            return False  # Stop the hook

                # Set up keyboard hook
                keyboard.hook(on_key_event)

                # Keep running until done
                while self._running:
                    time.sleep(0.1)

        except ImportError:
            self.console.print("[red]keyboard library not available. Install with: pip install keyboard[/red]")
            return None
        except Exception as e:
            self.console.print(f"[red]Error: {e}[/red]")
            return None
        finally:
            try:
                keyboard.unhook_all()
            except:
                pass

        return None if self._cancelled else self._result

    def run_simple_demo(self):
        """Run a simple demo showing the Rich box with simulated interaction."""

        self.console.print("\n🎨 True Rich Interactive Box Demo")
        self.console.print("=" * 50)

        # Show what the interactive box would look like
        demo_stages = [
            ("Initial State", ""),
            ("User typing 'H'", "H│"),
            ("User typing 'ello'", "Hello│"),
            ("User presses Enter", "Hello\n│"),
            ("User types 'World!'", "Hello\nWorld!│"),
        ]

        for stage_name, demo_text in demo_stages:
            self.console.print(f"\n📝 {stage_name}:")

            # Create demo panel
            panel = Panel(
                demo_text,
                title=f"{self.box_title} - INSERT",
                box=self.rich_box,
                width=self.box_width,
                height=8,
                border_style="blue"
            )

            self.console.print(Align.center(panel))

            if stage_name != demo_stages[-1][0]:  # Not last stage
                time.sleep(1.5)  # Pause between stages

        self.console.print("\n✨ This shows editing happening INSIDE the Rich box!")
        self.console.print("The cursor (│) moves within the Rich box boundaries.")
        self.console.print("\n💡 For actual keyboard interaction, use run_with_keyboard_input()")
        self.console.print("   (Requires: pip install keyboard)")


# Convenience function
def true_rich_interactive_input(**kwargs):
    """Create a true Rich interactive box input."""
    app = TrueRichInteractiveBox(**kwargs)
    return app.run_with_keyboard_input()


def demo_true_rich_interactive():
    """Demo the true Rich interactive box."""
    app = TrueRichInteractiveBox(
        box_title="True Interactive Rich Box",
        box_width=50,
        box_height=10,
        rich_box_style="ROUNDED"
    )

    app.run_simple_demo()


if __name__ == "__main__":
    demo_true_rich_interactive()