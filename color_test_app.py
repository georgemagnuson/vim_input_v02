#!/usr/bin/env python3
"""
Simple color test app to verify terminal color support.
Tests ValidatedVimReadline with different colored placeholder text.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import ValidatedVimReadline


def test_basic_colors():
    """Test basic ValidatedVimReadline with different placeholder colors."""

    # Test 1: Blue placeholder
    print("=== Test 1: Blue Placeholder ===")
    print("The placeholder text should appear in BLUE")

    readline1 = ValidatedVimReadline(
        prompt="Blue Test: ",
        placeholder_text="This should be BLUE text",
        show_status=False
    )

    result1 = readline1.run()
    print(f"Result: {result1 or 'Cancelled'}")
    print()

    # Test 2: Let's try a different approach - override the style completely
    print("=== Test 2: Custom Style Override ===")
    print("Testing with explicit blue color override")

    class BlueValidatedVimReadline(ValidatedVimReadline):
        def _create_style(self):
            from prompt_toolkit.styles import Style
            style_dict = {
                'prompt': 'bold',
                'line-number': '#666666',
                'line-number-separator': '#666666',
                'status': 'reverse',
                'placeholder': 'blue italic',  # Using color name instead of hex
                'validation-error': 'red bold',
            }
            return Style.from_dict(style_dict)

    readline2 = BlueValidatedVimReadline(
        prompt="Custom Blue: ",
        placeholder_text="This should definitely be BLUE",
        show_status=False
    )

    result2 = readline2.run()
    print(f"Result: {result2 or 'Cancelled'}")
    print()

    # Test 3: Different colors to verify color support
    print("=== Test 3: Rainbow Colors ===")
    print("Testing different colors to verify terminal support")

    colors = [
        ('red', 'RED placeholder'),
        ('green', 'GREEN placeholder'),
        ('yellow', 'YELLOW placeholder'),
        ('blue', 'BLUE placeholder'),
        ('magenta', 'MAGENTA placeholder'),
        ('cyan', 'CYAN placeholder')
    ]

    for color, text in colors:
        print(f"Testing {color}...")

        class ColorTestVimReadline(ValidatedVimReadline):
            def __init__(self, test_color, *args, **kwargs):
                self.test_color = test_color
                super().__init__(*args, **kwargs)

            def _create_style(self):
                from prompt_toolkit.styles import Style
                style_dict = {
                    'prompt': 'bold',
                    'placeholder': f'{self.test_color} italic',
                    'validation-error': 'red bold',
                }
                return Style.from_dict(style_dict)

        readline = ColorTestVimReadline(
            test_color=color,
            prompt=f"{color.title()}: ",
            placeholder_text=text,
            show_status=False
        )

        result = readline.run()
        print(f"  {color} result: {result or 'Cancelled'}")


if __name__ == "__main__":
    print("Color Test App")
    print("==============")
    print("This tests placeholder text colors in ValidatedVimReadline")
    print("Press 'i' to enter insert mode, then type or press Enter to submit")
    print("Press Ctrl-C to cancel each test")
    print()

    try:
        test_basic_colors()
        print("All color tests completed!")

    except KeyboardInterrupt:
        print("\nColor testing interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()