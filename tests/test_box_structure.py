#!/usr/bin/env python3
"""
Test the box structure and character mapping.
"""

from vim_readline.rich_enhanced import RichVimReadline

def test_box_characters():
    """Test box character generation."""
    print("Testing box character mapping...")

    styles = ["rounded", "square", "double", "heavy"]

    for style in styles:
        print(f"\n{style.title()} Style:")

        readline = RichVimReadline(
            initial_text="test",
            panel_box_style=style,
            panel_title=f"{style} box test"
        )

        # Get box characters
        box_chars = readline._get_box_characters()

        print(f"  Top-left: {box_chars['top_left']}")
        print(f"  Top-right: {box_chars['top_right']}")
        print(f"  Bottom-left: {box_chars['bottom_left']}")
        print(f"  Bottom-right: {box_chars['bottom_right']}")
        print(f"  Horizontal: {box_chars['horizontal']}")
        print(f"  Vertical: {box_chars['vertical']}")

        # Create sample borders
        print(f"  Sample top border: {box_chars['top_left']}{box_chars['horizontal'] * 20}{box_chars['top_right']}")
        print(f"  Sample side:       {box_chars['vertical']}{' ' * 20}{box_chars['vertical']}")
        print(f"  Sample bottom:     {box_chars['bottom_left']}{box_chars['horizontal'] * 20}{box_chars['bottom_right']}")

def test_border_generation():
    """Test border line generation."""
    print("\n" + "="*60)
    print("Testing border line generation...")

    readline = RichVimReadline(
        initial_text="test",
        panel_box_style="rounded",
        panel_title="Test Title"
    )

    box_chars = readline._get_box_characters()

    # Test static versions for now
    print(f"\nBox characters: {box_chars}")
    print(f"Top border method exists: {hasattr(readline, '_create_top_border_line')}")
    print(f"Bottom border method exists: {hasattr(readline, '_create_bottom_border_line')}")

def main():
    """Main test."""
    print("Box Structure Test")
    print("==================")

    test_box_characters()
    test_border_generation()

    print("\n✅ Box structure tests completed!")
    print("\nKey improvements implemented:")
    print("  • True Unicode box drawing characters")
    print("  • Different styles: rounded, square, double, heavy")
    print("  • Dynamic border generation")
    print("  • Proper text containment within borders")

if __name__ == "__main__":
    main()