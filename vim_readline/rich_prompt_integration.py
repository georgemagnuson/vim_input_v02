"""
Rich + prompt-toolkit Integration - Practical implementation.

This provides a working integration between Rich's rendering capabilities
and prompt-toolkit's vim editing, creating a professional terminal interface.
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
from prompt_toolkit.cursor_shapes import ModalCursorShapeConfig
from prompt_toolkit.filters import Condition

# Rich imports for enhanced display
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
import io
import os


class RichPromptIntegration(BaseVimReadline):
    """
    Integration of Rich's beautiful rendering with prompt-toolkit's vim editing.

    This approach uses Rich for pre/post display and status information,
    while prompt-toolkit handles the actual text editing interaction.
    """

    def __init__(self,
                 initial_text="",
                 placeholder_text="",
                 prompt="",
                 show_line_numbers=False,
                 show_status=True,
                 wrap_lines=True,
                 submit_key='c-m',
                 newline_key='c-j',
                 cancel_keys=None,
                 # Rich integration options
                 box_title="Text Editor",
                 rich_box_style="ROUNDED",
                 box_width=70,
                 box_height=15,
                 show_rich_preview=True,
                 show_rich_result=True):

        # Rich configuration
        self.box_title = box_title
        self.rich_box_style = rich_box_style
        self.box_width = box_width
        self.box_height = box_height
        self.show_rich_preview = show_rich_preview
        self.show_rich_result = show_rich_result

        # Rich setup
        self.console = Console()
        self.rich_box_styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII,
            "MINIMAL": box.MINIMAL
        }
        self.rich_box = self.rich_box_styles.get(rich_box_style, box.ROUNDED)

        # Initialize parent
        super().__init__(
            initial_text=initial_text,
            placeholder_text=placeholder_text,
            prompt=prompt,
            show_line_numbers=show_line_numbers,
            show_status=show_status,
            wrap_lines=wrap_lines,
            submit_key=submit_key,
            newline_key=newline_key,
            cancel_keys=cancel_keys
        )

    def _show_rich_preview(self):
        """Show Rich preview before editing starts."""
        if not self.show_rich_preview:
            return

        # Create preview content
        preview_text = self.initial_text or self.placeholder_text or "Ready to edit..."

        # Create Rich panel for preview
        preview_panel = Panel(
            preview_text,
            title=f"📝 {self.box_title}",
            box=self.rich_box,
            width=self.box_width,
            height=min(self.box_height, 10),  # Smaller for preview
            border_style="blue"
        )

        # Create instructions panel
        instructions = Text(
            "Press Enter to start editing with vim commands...\n"
            "ESC: Normal mode | i: Insert | Return: Submit | Ctrl+C: Cancel",
            style="dim italic"
        )
        instruction_panel = Panel(
            instructions,
            title="🔧 Instructions",
            box=box.MINIMAL,
            width=self.box_width,
            border_style="green"
        )

        # Display
        self.console.print()
        self.console.print(Align.center(preview_panel))
        self.console.print(Align.center(instruction_panel))

        # Wait for user to be ready
        input("\nPress Enter to start editing...")
        self.console.clear()

    def _show_rich_result(self, result):
        """Show Rich result after editing completes."""
        if not self.show_rich_result or result is None:
            return

        # Create result panel
        result_panel = Panel(
            result,
            title=f"✅ {self.box_title} - Result",
            box=self.rich_box,
            width=self.box_width,
            height=min(self.box_height, len(result.split('\n')) + 4),
            border_style="green"
        )

        # Create stats panel
        stats = Text(
            f"Length: {len(result)} characters | Lines: {len(result.split(chr(10)))}\n"
            f"Words: {len(result.split())} | Box style: {self.rich_box_style}",
            style="dim"
        )
        stats_panel = Panel(
            stats,
            title="📊 Statistics",
            box=box.MINIMAL,
            width=self.box_width,
            border_style="blue"
        )

        # Display results
        self.console.print()
        self.console.print(Align.center(result_panel))
        self.console.print(Align.center(stats_panel))

    def run(self):
        """Run the Rich-integrated vim editor."""

        # Show Rich preview
        self._show_rich_preview()

        try:
            # Run the standard vim editing session
            result = super().run()

            # Show Rich result
            if result is not None:
                self._show_rich_result(result)
            else:
                self.console.print("\n[dim]Editing cancelled[/dim]")

            return result

        except Exception as e:
            self.console.print(f"\n[red]Error during editing: {e}[/red]")
            return None


class RichVimWorkspace:
    """
    A Rich-powered workspace that can handle multiple vim editing sessions
    with beautiful Rich displays.
    """

    def __init__(self, workspace_title="Rich Vim Workspace"):
        self.workspace_title = workspace_title
        self.console = Console()
        self.sessions = []

    def show_workspace_intro(self):
        """Show the workspace introduction."""

        title_text = Text(self.workspace_title, style="bold blue")
        intro_panel = Panel(
            title_text,
            box=box.DOUBLE,
            width=80,
            border_style="blue"
        )

        description = Text(
            "Welcome to the Rich Vim Workspace!\n\n"
            "This workspace combines Rich's beautiful terminal rendering\n"
            "with full vim editing capabilities.\n\n"
            "Features:\n"
            "• Professional Rich panels and styling\n"
            "• Full vim editing modes (normal/insert/visual)\n"
            "• Multiple box styles and themes\n"
            "• Real-time status and statistics\n"
            "• Beautiful result presentation",
            style="white"
        )

        desc_panel = Panel(
            description,
            title="✨ Features",
            box=box.ROUNDED,
            width=80,
            border_style="green"
        )

        self.console.print()
        self.console.print(Align.center(intro_panel))
        self.console.print(Align.center(desc_panel))

    def create_editing_session(self, **kwargs):
        """Create a new Rich vim editing session."""

        session_defaults = {
            "box_title": f"Session {len(self.sessions) + 1}",
            "rich_box_style": "ROUNDED",
            "box_width": 70,
            "box_height": 12,
            "show_rich_preview": True,
            "show_rich_result": True
        }

        # Merge user options with defaults
        session_config = {**session_defaults, **kwargs}

        session = RichPromptIntegration(**session_config)
        self.sessions.append(session)

        return session

    def run_demo_sessions(self):
        """Run a series of demo editing sessions."""

        self.show_workspace_intro()
        input("\nPress Enter to start demo sessions...")

        # Demo sessions with different styles
        demo_configs = [
            {
                "box_title": "Code Editor",
                "rich_box_style": "SQUARE",
                "initial_text": "def hello_rich():\n    print('Hello from Rich + Vim!')\n    return 'success'",
                "box_width": 60,
                "box_height": 10
            },
            {
                "box_title": "Documentation",
                "rich_box_style": "DOUBLE",
                "initial_text": "# Rich Vim Integration\n\nThis demonstrates beautiful terminal editing.\n\n## Features\n- Vim editing\n- Rich displays\n- Professional UI",
                "box_width": 70,
                "box_height": 12
            },
            {
                "box_title": "Quick Note",
                "rich_box_style": "MINIMAL",
                "initial_text": "Quick notes:\n• Rich provides beautiful terminals\n• Vim gives powerful editing\n• Together they're amazing!",
                "box_width": 50,
                "box_height": 8
            }
        ]

        for i, config in enumerate(demo_configs):
            self.console.print(f"\n🚀 Demo Session {i + 1}/{len(demo_configs)}")

            session = self.create_editing_session(**config)
            result = session.run()

            if result:
                self.console.print(f"[green]✅ Session {i + 1} completed![/green]")
            else:
                self.console.print(f"[yellow]⚠️ Session {i + 1} cancelled[/yellow]")

            if i < len(demo_configs) - 1:
                input("\nPress Enter for next session...")

        self.console.print("\n🎉 All demo sessions complete!")

    def show_workspace_summary(self):
        """Show summary of the workspace session."""

        summary_text = Text(
            f"Workspace Summary:\n\n"
            f"Total sessions: {len(self.sessions)}\n"
            f"Rich integration: ✅ Enabled\n"
            f"Vim editing: ✅ Enabled\n"
            f"Professional UI: ✅ Active\n\n"
            f"Thank you for trying Rich + Vim integration!",
            style="white"
        )

        summary_panel = Panel(
            summary_text,
            title="📊 Workspace Summary",
            box=box.DOUBLE,
            width=60,
            border_style="green"
        )

        self.console.print()
        self.console.print(Align.center(summary_panel))


# Convenience functions
def rich_vim_input(**kwargs):
    """Create a Rich-integrated vim input session."""
    editor = RichPromptIntegration(**kwargs)
    return editor.run()


def demo_rich_vim_workspace():
    """Run a complete Rich vim workspace demo."""
    workspace = RichVimWorkspace("🎨 Rich Vim Demo Workspace")
    workspace.run_demo_sessions()
    workspace.show_workspace_summary()


if __name__ == "__main__":
    demo_rich_vim_workspace()