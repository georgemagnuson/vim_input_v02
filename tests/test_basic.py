#!/usr/bin/env python3
"""
Basic test of VimReadline functionality without interactive input.
"""

from vim_readline import VimReadline

def test_creation():
    """Test that VimReadline objects can be created."""
    print("Testing VimReadline creation...")

    # Test with placeholder
    readline1 = VimReadline(
        placeholder_text="Test placeholder",
        show_status=True
    )
    print("✓ Created with placeholder")

    # Test with initial text
    readline2 = VimReadline(
        initial_text="Initial content",
        show_line_numbers=True
    )
    print("✓ Created with initial text")

    # Test with prompt
    readline3 = VimReadline(
        prompt=">>> ",
        placeholder_text="Type here...",
        show_status=True
    )
    print("✓ Created with prompt")

    print("All creation tests passed!")

if __name__ == "__main__":
    test_creation()
    print("\nBasic functionality test completed.")
    print("To test interactively, run: python example.py")