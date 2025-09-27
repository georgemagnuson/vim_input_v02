#!/usr/bin/env python3
"""
Simple Rich app demonstrating vim-readline integration.

This app showcases how to build a beautiful CLI application using Rich for layout
and vim-readline for text input, creating a Claude Code-like experience.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.columns import Columns
from rich.table import Table
from rich.prompt import Confirm
from rich.layout import Layout
from rich.align import Align
from rich import print as rprint

from vim_readline import rich_vim_input

console = Console()


def show_header():
    """Display the app header with Rich styling."""
    title = Text("📝 Rich + VimReadline Demo", style="bold blue")
    subtitle = Text("A beautiful CLI text editor experience", style="italic")

    console.print()
    console.print(Align.center(title))
    console.print(Align.center(subtitle))
    console.print()


def show_main_menu():
    """Display the main menu with Rich styling."""
    console.print(Rule("Main Menu", style="blue"))

    menu_table = Table.grid(padding=(0, 2))
    menu_table.add_row("1.", "[bold green]Code Editor[/bold green]", "- Edit Python code with vim controls")
    menu_table.add_row("2.", "[bold yellow]SQL Query Builder[/bold yellow]", "- Build SQL queries with syntax awareness")
    menu_table.add_row("3.", "[bold cyan]Note Taking[/bold cyan]", "- Take formatted notes with vim editing")
    menu_table.add_row("4.", "[bold magenta]Configuration Editor[/bold magenta]", "- Edit config files with line numbers")
    menu_table.add_row("5.", "[bold red]Text Art Creator[/bold red]", "- Create ASCII art and text designs")
    menu_table.add_row("q.", "[dim]Quit[/dim]", "- Exit the application")

    console.print(menu_table)
    console.print(Rule(style="blue"))


def code_editor():
    """Rich-enhanced Python code editor."""
    console.print("\n[bold green]🐍 Python Code Editor[/bold green]")
    console.print("Use vim controls to edit. Return to submit, Ctrl-J for newlines.")

    # Default Python template
    template = '''def main():
    """Your code here"""
    print("Hello, World!")
    return 0


if __name__ == "__main__":
    main()'''

    try:
        result = rich_vim_input(
            initial_text=template,
            panel_title="🐍 Python Code Editor",
            panel_box_style="rounded",
            show_rules=True,
            rule_style="green",
            show_line_numbers=True,
            show_status=True
        )

        if result is not None:
            # Display the result in a nice panel
            console.print("\n[bold green]✅ Code Saved![/bold green]")
            code_panel = Panel(
                result,
                title="📄 Your Python Code",
                border_style="green",
                expand=False
            )
            console.print(code_panel)

            # Ask if they want to save to file
            if Confirm.ask("\n💾 Save to file?"):
                filename = console.input("[bold]Filename[/bold] (e.g., script.py): ")
                if filename:
                    with open(filename, 'w') as f:
                        f.write(result)
                    console.print(f"[green]✅ Saved to {filename}[/green]")
        else:
            console.print("[yellow]📝 Edit cancelled[/yellow]")

    except KeyboardInterrupt:
        console.print("[red]❌ Interrupted[/red]")


def sql_query_builder():
    """SQL query builder with vim editing."""
    console.print("\n[bold yellow]🗃️  SQL Query Builder[/bold yellow]")
    console.print("Build your SQL queries with vim-style editing.")

    # SQL template
    template = '''SELECT
    users.id,
    users.name,
    users.email,
    COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE users.active = 1
GROUP BY users.id
ORDER BY order_count DESC
LIMIT 10;'''

    try:
        result = rich_vim_input(
            initial_text=template,
            panel_title="🗃️ SQL Query Builder",
            panel_box_style="double",
            show_rules=True,
            rule_style="yellow",
            show_line_numbers=True,
            show_status=True
        )

        if result is not None:
            console.print("\n[bold yellow]✅ Query Built![/bold yellow]")
            query_panel = Panel(
                result,
                title="📊 Your SQL Query",
                border_style="yellow",
                expand=False
            )
            console.print(query_panel)
        else:
            console.print("[yellow]📝 Query building cancelled[/yellow]")

    except KeyboardInterrupt:
        console.print("[red]❌ Interrupted[/red]")


def note_taking():
    """Simple note taking with Rich presentation."""
    console.print("\n[bold cyan]📝 Note Taking[/bold cyan]")
    console.print("Write your notes with vim controls. Perfect for documentation!")

    try:
        result = rich_vim_input(
            placeholder_text="Start typing your notes here...\n\nUse vim commands:\n- i/a/o for insert mode\n- ESC for normal mode\n- dd to delete lines\n- yy/p to copy/paste",
            panel_title="📝 Notes",
            panel_box_style="rounded",
            show_rules=True,
            rule_style="cyan",
            show_line_numbers=True,
            show_status=True
        )

        if result is not None and result.strip():
            console.print("\n[bold cyan]✅ Note Saved![/bold cyan]")

            # Create a nice presentation of the notes
            note_panel = Panel(
                result,
                title="📄 Your Notes",
                border_style="cyan",
                expand=False
            )
            console.print(note_panel)

            # Show word count
            words = len(result.split())
            lines = len(result.splitlines())
            console.print(f"[dim]📊 {words} words, {lines} lines[/dim]")
        else:
            console.print("[yellow]📝 Note cancelled[/yellow]")

    except KeyboardInterrupt:
        console.print("[red]❌ Interrupted[/red]")


def config_editor():
    """Configuration file editor."""
    console.print("\n[bold magenta]⚙️  Configuration Editor[/bold magenta]")
    console.print("Edit configuration with vim controls and line numbers.")

    # Config template
    config_template = '''# Application Configuration
[database]
host = localhost
port = 5432
username = admin
password = secret
database = myapp

[cache]
type = redis
host = localhost
port = 6379
ttl = 3600

[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
file = /var/log/app.log

[features]
enable_auth = true
enable_cache = true
debug_mode = false'''

    try:
        result = rich_vim_input(
            initial_text=config_template,
            panel_title="⚙️ Configuration Editor",
            panel_box_style="heavy",
            show_rules=True,
            rule_style="magenta",
            show_line_numbers=True,
            show_status=True
        )

        if result is not None:
            console.print("\n[bold magenta]✅ Configuration Updated![/bold magenta]")
            config_panel = Panel(
                result,
                title="📋 Your Configuration",
                border_style="magenta",
                expand=False
            )
            console.print(config_panel)
        else:
            console.print("[yellow]📝 Configuration edit cancelled[/yellow]")

    except KeyboardInterrupt:
        console.print("[red]❌ Interrupted[/red]")


def text_art_creator():
    """ASCII art and text design creator."""
    console.print("\n[bold red]🎨 Text Art Creator[/bold red]")
    console.print("Create ASCII art and text designs with vim editing!")

    # ASCII art template
    art_template = '''
    ┌─────────────────────────────────────┐
    │                                     │
    │     ██╗   ██╗██╗███╗   ███╗        │
    │     ██║   ██║██║████╗ ████║        │
    │     ██║   ██║██║██╔████╔██║        │
    │     ╚██╗ ██╔╝██║██║╚██╔╝██║        │
    │      ╚████╔╝ ██║██║ ╚═╝ ██║        │
    │       ╚═══╝  ╚═╝╚═╝     ╚═╝        │
    │                                     │
    │           Text Art Editor           │
    │                                     │
    └─────────────────────────────────────┘

    Create your design here:
    '''

    try:
        result = rich_vim_input(
            initial_text=art_template,
            panel_title="🎨 Text Art Creator",
            panel_box_style="square",
            show_rules=True,
            rule_style="red",
            show_line_numbers=False,  # No line numbers for art
            show_status=True
        )

        if result is not None:
            console.print("\n[bold red]✅ Art Created![/bold red]")
            art_panel = Panel(
                result,
                title="🖼️  Your Text Art",
                border_style="red",
                expand=False
            )
            console.print(art_panel)
        else:
            console.print("[yellow]📝 Art creation cancelled[/yellow]")

    except KeyboardInterrupt:
        console.print("[red]❌ Interrupted[/red]")


def main():
    """Main application loop."""
    show_header()

    while True:
        show_main_menu()

        try:
            choice = console.input("\n[bold]Enter your choice[/bold] (1-5, q): ").strip().lower()

            if choice == 'q' or choice == 'quit':
                console.print("\n[blue]👋 Thanks for using Rich + VimReadline![/blue]")
                break
            elif choice == '1':
                code_editor()
            elif choice == '2':
                sql_query_builder()
            elif choice == '3':
                note_taking()
            elif choice == '4':
                config_editor()
            elif choice == '5':
                text_art_creator()
            else:
                console.print("[red]❌ Invalid choice. Please try again.[/red]")

            # Pause before returning to menu
            if choice in ['1', '2', '3', '4', '5']:
                console.input("\n[dim]Press Enter to continue...[/dim]")
                console.clear()
                show_header()

        except KeyboardInterrupt:
            console.print("\n[blue]👋 Thanks for using Rich + VimReadline![/blue]")
            break
        except EOFError:
            console.print("\n[blue]👋 Thanks for using Rich + VimReadline![/blue]")
            break


if __name__ == "__main__":
    main()