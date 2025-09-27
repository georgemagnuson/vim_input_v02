#!/usr/bin/env python3
"""
Test Rich integration with vim-readline.
"""

from vim_readline import rich_vim_input, RichVimReadline

def test_rich_imports():
    """Test that Rich components can be imported."""
    print("Testing Rich integration imports...")

    try:
        from vim_readline import RichVimReadline, rich_vim_input
        print("✓ Rich components imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Rich import failed: {e}")
        return False

def test_rich_creation():
    """Test Rich-enhanced VimReadline creation."""
    print("\nTesting Rich-enhanced VimReadline creation...")

    try:
        # Test different box styles
        styles = ["rounded", "square", "double", "heavy"]

        for style in styles:
            readline = RichVimReadline(
                initial_text=f"Testing {style} style box",
                panel_title=f"vim input ({style})",
                panel_box_style=style,
                show_rules=True,
                show_status=True,
                show_line_numbers=True
            )
            print(f"✓ Created RichVimReadline with {style} style")

        return True

    except Exception as e:
        print(f"✗ Rich creation failed: {e}")
        return False

def test_rich_function():
    """Test the rich_vim_input convenience function."""
    print("\nTesting rich_vim_input function...")

    try:
        # Test function creation (don't run interactively)
        from vim_readline import rich_vim_input
        print("✓ rich_vim_input function is available")
        return True

    except Exception as e:
        print(f"✗ rich_vim_input test failed: {e}")
        return False

def demo_rich_styles():
    """Demo what the Rich styles would look like."""
    print("\n=== Rich Style Preview ===")

    # Show what each style would render as
    from rich.console import Console
    from rich.panel import Panel
    from rich.rule import Rule
    from rich.box import ROUNDED, SQUARE, DOUBLE, HEAVY

    console = Console()

    styles = [
        ("rounded", ROUNDED, "Like Claude Code"),
        ("square", SQUARE, "Clean and simple"),
        ("double", DOUBLE, "Bold double lines"),
        ("heavy", HEAVY, "Heavy emphasis")
    ]

    sample_code = """def hello():
    print("Rich + vim-readline!")
    return True"""

    for name, box_style, desc in styles:
        print(f"\n{name.title()} style - {desc}:")

        # Top rule
        console.print(Rule("vim input", style="blue"))

        # Panel
        panel = Panel(
            sample_code,
            box=box_style,
            expand=False,
            padding=(0, 1)
        )
        console.print(panel)

        # Status bar simulation
        console.print("  ✏️ -- INSERT --")

        # Bottom rule
        console.print(Rule(style="blue"))

if __name__ == "__main__":
    print("Rich Integration Tests")
    print("=====================")

    success = True
    success &= test_rich_imports()
    success &= test_rich_creation()
    success &= test_rich_function()

    if success:
        print("\n🎉 All Rich integration tests passed!")
        demo_rich_styles()
    else:
        print("\n❌ Some tests failed. Check Rich installation:")
        print("   pip install rich")

    print("\nTo use Rich-enhanced vim-readline:")
    print("   from vim_readline import rich_vim_input")
    print("   result = rich_vim_input(panel_title='Code Input', panel_box_style='rounded')")