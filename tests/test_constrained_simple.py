#!/usr/bin/env python3
"""
Simple test for the box-constrained VimReadline implementation.
"""

def test_simple_box():
    """Simple test of box constraints."""
    print("Testing box-constrained VimReadline...")
    print("Box size: 50x8 with borders")
    print("Try typing long lines to see text wrapping within the box boundaries.")
    print()

    try:
        from vim_readline.constrained import box_constrained_vim_input

        result = box_constrained_vim_input(
            initial_text="This is a test of the box-constrained input.\n\nType some long lines and see how they wrap within the 50-character box width.\n\nUse vim commands: ESC for normal mode, i for insert mode.",
            box_width=50,
            box_height=8,
            show_box_border=True,
            show_line_numbers=True,
            show_status=True,
            wrap_lines=True
        )

        if result is not None:
            print("✅ Box constraint test successful!")
            print(f"Result length: {len(result)} characters")
            print("Result preview:")
            print("─" * 50)
            print(result)
            print("─" * 50)
        else:
            print("❌ Test cancelled")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_box()