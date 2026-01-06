#!/usr/bin/env python3
"""
Demo: VimPrompt - Rich Prompt API Integration

Shows how VimPrompt extends Rich's Prompt.ask() API to provide
vim-mode text input with the familiar Rich interface.

Usage:
    python demos/rich_prompt_api_demo.py
"""

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Import VimPrompt - extends Rich's Prompt API
from vim_readline import VimPrompt, IntVimPrompt, FloatVimPrompt, ask_vim


def demo_basic_vim_prompt():
    """Demo 1: Basic vim-mode prompt (like Prompt.ask but with vim)"""
    console = Console()

    console.print("\n[bold cyan]Demo 1: Basic VimPrompt.ask_vim()[/bold cyan]")
    console.print("Just like Rich's Prompt.ask(), but with vim modal editing!")
    console.print()

    # Simple vim prompt
    name = VimPrompt.ask_vim(
        "[bold]Enter your name:[/bold]",
        placeholder_text="John Doe"
    )

    console.print(f"\n[green]✓[/green] You entered: [bold]{name}[/bold]")


def demo_vim_prompt_with_choices():
    """Demo 2: VimPrompt with validation choices"""
    console = Console()

    console.print("\n[bold cyan]Demo 2: VimPrompt with Choices[/bold cyan]")
    console.print("Vim editing + Rich validation!")
    console.print()

    language = VimPrompt.ask_vim(
        "[bold]Select your favorite language:[/bold]",
        choices=["Python", "JavaScript", "Rust", "Go"],
        panel_title="Language Selection",
        panel_box_style="rounded"
    )

    console.print(f"\n[green]✓[/green] You selected: [bold]{language}[/bold]")


def demo_vim_prompt_multiline():
    """Demo 3: Multiline vim editing (unlike Rich's single-line Prompt)"""
    console = Console()

    console.print("\n[bold cyan]Demo 3: Multiline Code Editor[/bold cyan]")
    console.print("This is what VimReadline adds - Rich can't do multiline!")
    console.print()

    code = VimPrompt.ask_vim(
        "[bold magenta]Enter Python code:[/bold magenta]",
        panel_title="Code Editor",
        panel_box_style="double",
        show_line_numbers=True,
        placeholder_text="def main():\n    print('Hello, World!')\n    return 0"
    )

    console.print("\n[green]✓[/green] Code entered:")
    console.print(Panel(code, title="Your Code", border_style="green"))


def demo_int_float_prompts():
    """Demo 4: Typed prompts (IntVimPrompt, FloatVimPrompt)"""
    console = Console()

    console.print("\n[bold cyan]Demo 4: Typed Vim Prompts[/bold cyan]")
    console.print("IntVimPrompt and FloatVimPrompt - just like Rich's IntPrompt/FloatPrompt!")
    console.print()

    # Integer prompt with vim editing
    age = IntVimPrompt.ask_vim(
        "[bold]Enter your age:[/bold]",
        panel_title="Age",
        default=25
    )

    console.print(f"[green]✓[/green] Age: {age} (type: {type(age).__name__})")

    # Float prompt with vim editing
    price = FloatVimPrompt.ask_vim(
        "[bold]Enter price:[/bold]",
        panel_title="Price",
        default=19.99
    )

    console.print(f"[green]✓[/green] Price: ${price:.2f} (type: {type(price).__name__})")


def demo_comparison():
    """Demo 5: Show Rich Prompt vs VimPrompt side-by-side"""
    console = Console()

    console.print("\n[bold cyan]Demo 5: API Comparison[/bold cyan]")
    console.print()

    comparison_md = """
## Rich Prompt API vs VimPrompt API

### Rich's Standard Prompt (single-line, no vim)
```python
from rich.prompt import Prompt
name = Prompt.ask("Enter your name", default="John")
```

### VimPrompt (multiline, vim modes, same API!)
```python
from vim_readline import VimPrompt
name = VimPrompt.ask_vim("Enter your name",
                         panel_title="Name",
                         show_line_numbers=True)
```

### Key Differences

| Feature | Rich Prompt | VimPrompt |
|---------|-------------|-----------|
| **Vim Modes** | ❌ No | ✅ Yes (normal/insert/visual) |
| **Multiline** | ❌ No | ✅ Yes |
| **Line Numbers** | ❌ No | ✅ Yes |
| **Validation** | ✅ Yes | ✅ Yes |
| **Choices** | ✅ Yes | ✅ Yes |
| **Rich Styling** | ✅ Yes | ✅ Yes |
| **API Compatibility** | ✅ Rich API | ✅ Compatible + Extended |

### Use Cases

**Use Rich Prompt for:**
- Simple single-line input
- Quick prompts in scripts
- When vim mode is not needed

**Use VimPrompt for:**
- Multiline text editing
- Code input
- Complex text manipulation
- Users who prefer vim keybindings
"""

    console.print(Markdown(comparison_md))


def demo_convenience_functions():
    """Demo 6: Convenience functions (like Prompt.ask shorthand)"""
    console = Console()

    console.print("\n[bold cyan]Demo 6: Convenience Functions[/bold cyan]")
    console.print("Shorthand functions for quick use!")
    console.print()

    # Instead of VimPrompt.ask_vim(), use ask_vim()
    from vim_readline import ask_vim, ask_vim_int, ask_vim_float

    console.print("[bold]Using ask_vim() shorthand:[/bold]")
    description = ask_vim(
        "Enter a description:",
        placeholder_text="Type something...",
        panel_title="Description"
    )

    console.print(f"\n[green]✓[/green] Description: {description}")


def main():
    """Run all demos"""
    console = Console()

    # Welcome message
    console.print(Panel.fit(
        "[bold magenta]VimPrompt - Rich Prompt API Integration[/bold magenta]\n\n"
        "Extends Rich's Prompt.ask() with vim modal editing!\n"
        "Same familiar API, now with vim superpowers! ⚡",
        border_style="magenta"
    ))

    console.print("\n[dim]Press Enter to continue through demos...[/dim]")
    input()

    try:
        # Run demos
        demo_basic_vim_prompt()
        input("\n[dim]Press Enter for next demo...[/dim]")

        demo_vim_prompt_with_choices()
        input("\n[dim]Press Enter for next demo...[/dim]")

        demo_vim_prompt_multiline()
        input("\n[dim]Press Enter for next demo...[/dim]")

        demo_int_float_prompts()
        input("\n[dim]Press Enter for next demo...[/dim]")

        demo_comparison()
        input("\n[dim]Press Enter for next demo...[/dim]")

        demo_convenience_functions()

        # Summary
        console.print("\n" + "="*60)
        console.print("[bold green]✓ All demos complete![/bold green]")
        console.print("\n[bold]Key Takeaways:[/bold]")
        console.print("1. VimPrompt.ask_vim() extends Rich's Prompt.ask()")
        console.print("2. Same API style, familiar to Rich users")
        console.print("3. Adds vim modal editing + multiline support")
        console.print("4. Works with Rich validation and styling")
        console.print("5. IntVimPrompt and FloatVimPrompt for typed input")
        console.print("\n[bold cyan]Usage in your code:[/bold cyan]")
        console.print("[dim]from vim_readline import VimPrompt, ask_vim")
        console.print("result = VimPrompt.ask_vim('Enter text:', panel_title='Editor')[/dim]")

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()
