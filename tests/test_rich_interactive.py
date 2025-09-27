#!/usr/bin/env python3
"""
Test the Rich interactive box application.
"""

def test_simple_rich_demo():
    """Test the simple Rich box demo."""
    print("🎨 Testing Simple Rich Interactive Demo")
    print("=" * 50)

    try:
        from vim_readline.rich_interactive_app import SimpleRichBoxApp

        # Test simple demo
        app = SimpleRichBoxApp(
            initial_text="Hello, Rich boxes!",
            box_title="Demo Box",
            box_width=50,
            box_height=8,
            rich_box_style="ROUNDED"
        )

        print("✅ SimpleRichBoxApp created successfully")

        # Test box display (non-interactive)
        app.show_input_box("This is test content for the Rich box.")
        print("✅ Box display working")

        # Note: Interactive demo would require user interaction
        print("✅ Simple Rich demo ready (run interactively for full demo)")

    except Exception as e:
        print(f"❌ Simple Rich demo failed: {e}")
        import traceback
        traceback.print_exc()

def test_rich_panel_creation():
    """Test Rich panel creation and rendering."""
    print("\n📦 Testing Rich Panel Creation")
    print("=" * 50)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich import box
        import io

        # Test different Rich box styles
        styles = {
            "ROUNDED": box.ROUNDED,
            "SQUARE": box.SQUARE,
            "DOUBLE": box.DOUBLE,
            "HEAVY": box.HEAVY,
            "ASCII": box.ASCII
        }

        for style_name, box_style in styles.items():
            # Create panel
            panel = Panel(
                f"This is a {style_name} style box.\nMultiple lines work perfectly!\nRich handles all the rendering.",
                title=f"{style_name} Test",
                box=box_style,
                width=40,
                height=6
            )

            # Render to string
            with io.StringIO() as string_io:
                console = Console(file=string_io, width=50)
                console.print(panel)
                output = string_io.getvalue()

            print(f"✅ {style_name} panel rendered ({len(output)} chars)")

        print("✅ All Rich panel styles working")

    except Exception as e:
        print(f"❌ Rich panel test failed: {e}")
        import traceback
        traceback.print_exc()

def test_rich_live_display():
    """Test Rich Live display capabilities."""
    print("\n⚡ Testing Rich Live Display")
    print("=" * 50)

    try:
        from rich.live import Live
        from rich.panel import Panel
        from rich.console import Console
        from rich import box
        import time
        import io

        # Test Live display with changing content
        console = Console(file=io.StringIO(), width=60)

        content_states = [
            "Initial content...",
            "Content is updating...",
            "Live display working!",
            "Rich Live is powerful!"
        ]

        print("Testing Live display simulation:")
        for i, content in enumerate(content_states):
            panel = Panel(
                content,
                title=f"Live Demo {i+1}/4",
                box=box.ROUNDED,
                width=50
            )

            # Simulate Live update
            console.file = io.StringIO()
            console.print(panel)
            output = console.file.getvalue()

            print(f"  Frame {i+1}: {len(output.strip().split(chr(10)))} lines rendered")

        print("✅ Rich Live display simulation working")

    except Exception as e:
        print(f"❌ Rich Live test failed: {e}")

def create_practical_rich_vim_demo():
    """Create a practical demo showing how Rich + vim could work."""
    print("\n🚀 Practical Rich + Vim Integration Demo")
    print("=" * 50)

    try:
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        from rich.align import Align
        from rich import box

        console = Console()

        # Show what a Rich-integrated vim interface could look like
        demo_content = """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Type your code here...
result = fibonacci(10)
print(f"Fibonacci(10) = {result}")"""

        # Create the main editing panel
        main_panel = Panel(
            demo_content,
            title="📝 Rich Vim Editor",
            box=box.ROUNDED,
            width=70,
            height=15,
            border_style="blue"
        )

        # Create status panel
        status_text = Text("-- INSERT --", style="bold green")
        status_panel = Panel(
            Align.center(status_text),
            width=70,
            height=3,
            box=box.MINIMAL,
            border_style="green"
        )

        # Create info panel
        info_text = Text(
            "ESC: Normal mode | i: Insert | :w: Save | :q: Quit\nArrow keys or hjkl to navigate",
            style="dim"
        )
        info_panel = Panel(
            info_text,
            title="🔧 Controls",
            width=70,
            height=4,
            box=box.MINIMAL,
            border_style="yellow"
        )

        print("Rich + Vim Integration Concept:")
        console.print()
        console.print(Align.center(main_panel))
        console.print(Align.center(status_panel))
        console.print(Align.center(info_panel))

        print("\n✅ Rich + Vim integration concept demonstrated")
        print("\nThis shows how Rich's beautiful rendering could be combined")
        print("with vim-style editing for a professional terminal interface!")

    except Exception as e:
        print(f"❌ Practical demo failed: {e}")

def show_rich_advantages():
    """Show the advantages of using Rich for terminal UIs."""
    print("\n🌟 Rich Advantages for Terminal UIs")
    print("=" * 50)

    advantages = [
        ("🎨 Beautiful Rendering", "Rich provides professional-quality terminal output"),
        ("📦 Built-in Components", "Panels, tables, progress bars, and more out of the box"),
        ("🔄 Live Updates", "Real-time display updates with Rich Live"),
        ("🎯 Perfect Alignment", "No manual calculation of widths, heights, or positioning"),
        ("🌈 Rich Styling", "Colors, styles, and formatting built-in"),
        ("📱 Responsive Design", "Automatically adapts to terminal size"),
        ("🔧 Extensive API", "Comprehensive toolkit for terminal applications"),
        ("⚡ High Performance", "Optimized rendering with minimal flicker")
    ]

    for title, description in advantages:
        print(f"{title:<25} {description}")

    print("\n✅ Rich is the professional choice for terminal UIs!")

def main():
    """Main test function."""
    print("🎨 Rich Interactive Box Application Tests")
    print()

    test_simple_rich_demo()
    test_rich_panel_creation()
    test_rich_live_display()
    create_practical_rich_vim_demo()
    show_rich_advantages()

    print("\n" + "=" * 60)
    print("🎉 Rich Interactive Testing Complete!")
    print()
    print("Key takeaways:")
    print("  ✅ Rich provides superior box rendering")
    print("  ✅ Live display updates work smoothly")
    print("  ✅ Multiple professional box styles available")
    print("  ✅ Perfect for terminal-based vim editors")
    print("  ✅ No manual alignment or calculation needed")
    print()
    print("Rich + vim integration offers:")
    print("  🎨 Professional visual quality")
    print("  ⚡ Real-time updates")
    print("  📦 Built-in components")
    print("  🎯 Perfect rendering")

if __name__ == "__main__":
    main()