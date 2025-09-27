#!/usr/bin/env python3
"""
Standalone Rich demo that can be run directly without import issues.
"""

import sys
import os

# Add the current directory to the Python path so we can import vim_readline
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_rich_box_styles():
    """Demo Rich box styles without running the interactive editor."""
    print("🎨 Rich Box Styles Demonstration")
    print("=" * 50)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich import box

        console = Console()

        # Available Rich box styles
        styles = [
            ("ROUNDED", box.ROUNDED, "Rich's signature rounded corners"),
            ("SQUARE", box.SQUARE, "Clean square corners"),
            ("DOUBLE", box.DOUBLE, "Double lines for emphasis"),
            ("HEAVY", box.HEAVY, "Bold, thick lines"),
            ("ASCII", box.ASCII, "ASCII-only for compatibility"),
            ("MINIMAL", box.MINIMAL, "Minimal style"),
        ]

        console.print("\n🎯 Rich provides these professional box styles:")
        console.print()

        for style_name, box_style, description in styles:
            # Create sample content
            sample_content = f"This is a {style_name} box example.\n\nStyle: {style_name}\nDescription: {description}\n\nRich handles all the alignment automatically!"

            # Create Rich panel
            panel = Panel(
                sample_content,
                title=f"📦 {style_name} Style",
                box=box_style,
                width=60,
                expand=False,
                border_style="blue"
            )

            console.print(panel)
            console.print()

        console.print("✨ All boxes rendered perfectly by Rich!")
        console.print("Notice how there are no alignment issues - Rich handles everything!")

    except ImportError as e:
        print(f"❌ Rich not available: {e}")
        print("Install with: pip install rich")

def demo_rich_vs_manual():
    """Show Rich vs manual box drawing comparison."""
    print("\n🔄 Rich vs Manual Box Drawing")
    print("=" * 50)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich import box

        console = Console()

        print("MANUAL box drawing (what we were doing):")
        print("┌─── Manual Box ────┐")
        print("│ Manual borders    │")
        print("│ Error-prone math  │")
        print("│ Alignment issues  │")
        print("└───────────────────┘")
        print("❌ Required fixes for right border alignment")

        print("\nRICH box drawing (professional approach):")

        rich_panel = Panel(
            "Rich borders\nPerfect alignment\nZero calculation errors\nProfessional quality",
            title="Rich Box",
            box=box.ROUNDED,
            width=25,
            border_style="green"
        )

        console.print(rich_panel)
        print("✅ Perfect alignment guaranteed!")

        # Show Rich's character extraction
        print(f"\nRich's ROUNDED characters:")
        print(f"  top_left: '{box.ROUNDED.top_left}'")
        print(f"  top_right: '{box.ROUNDED.top_right}'")
        print(f"  bottom_left: '{box.ROUNDED.bottom_left}'")
        print(f"  bottom_right: '{box.ROUNDED.bottom_right}'")
        print(f"  horizontal: '{box.ROUNDED.top}'")
        print(f"  vertical: '{box.ROUNDED.mid_left}'")

    except ImportError:
        print("❌ Rich not available for comparison")

def test_vim_readline_import():
    """Test if vim_readline modules can be imported."""
    print("\n📦 VimReadline Module Import Test")
    print("=" * 50)

    modules_to_test = [
        ("vim_readline.core", "Core VimReadline"),
        ("vim_readline.full_box", "Full Box VimReadline"),
        ("vim_readline.rich_box_native", "Rich-Native Box"),
        ("vim_readline.rich_prompt_integration", "Rich-Prompt Integration")
    ]

    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description:<25} - Import successful")
        except ImportError as e:
            print(f"❌ {description:<25} - Import failed: {e}")

def demo_rich_integration_concept():
    """Show the concept of Rich integration."""
    print("\n💡 Rich Integration Concept")
    print("=" * 50)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.layout import Layout
        from rich.text import Text
        from rich import box

        console = Console()

        # Create concept layout
        layout = Layout()

        # Title
        title_panel = Panel(
            Text("Rich + Vim Integration", justify="center", style="bold blue"),
            box=box.DOUBLE,
            border_style="blue"
        )

        # Features
        features_text = Text()
        features_text.append("🎨 ", style="yellow")
        features_text.append("Beautiful Rich panels for display\n", style="white")
        features_text.append("⚡ ", style="green")
        features_text.append("Powerful vim editing capabilities\n", style="white")
        features_text.append("🔧 ", style="blue")
        features_text.append("Professional terminal interface\n", style="white")
        features_text.append("📦 ", style="magenta")
        features_text.append("Built-in components and styling", style="white")

        features_panel = Panel(
            features_text,
            title="Features",
            box=box.ROUNDED,
            border_style="green"
        )

        # Usage example
        usage_text = Text()
        usage_text.append("from vim_readline import rich_vim_input\n\n", style="dim")
        usage_text.append("result = rich_vim_input(\n", style="cyan")
        usage_text.append("    box_title='My Editor',\n", style="white")
        usage_text.append("    rich_box_style='ROUNDED',\n", style="white")
        usage_text.append("    show_rich_preview=True\n", style="white")
        usage_text.append(")", style="cyan")

        usage_panel = Panel(
            usage_text,
            title="Usage",
            box=box.SQUARE,
            border_style="yellow"
        )

        # Display
        console.print(title_panel)
        console.print()
        console.print(features_panel)
        console.print()
        console.print(usage_panel)

    except ImportError:
        print("Rich not available for concept demo")

def main():
    """Main demo function."""
    print("🚀 Rich Standalone Demo")
    print("This demo runs without relative import issues!")
    print()

    demo_rich_box_styles()
    demo_rich_vs_manual()
    test_vim_readline_import()
    demo_rich_integration_concept()

    print("\n" + "=" * 60)
    print("🎉 Rich Standalone Demo Complete!")
    print()
    print("To use the Rich interactive vim editors:")
    print("1. Import from the main package:")
    print("   from vim_readline import rich_vim_input")
    print("")
    print("2. Or run the specific demos:")
    print("   python demo_rich_interactive_complete.py")
    print("")
    print("3. Or test individual modules:")
    print("   python -m vim_readline.rich_box_native")

if __name__ == "__main__":
    main()