#!/usr/bin/env python3
"""
Color Identification Test App - Tests what colors users actually see in ValidatedVimReadline.

This app displays prompts and placeholder text in different colors and asks the user
to identify what color they see. This helps debug terminal color display issues.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import ValidatedVimReadline
from prompt_toolkit.styles import Style


class ColorTestVimReadline(ValidatedVimReadline):
    """Custom ValidatedVimReadline with configurable prompt and placeholder colors."""

    def __init__(self, prompt_color, placeholder_color, *args, **kwargs):
        self.prompt_color = prompt_color
        self.placeholder_color = placeholder_color
        super().__init__(*args, **kwargs)

    def _create_style(self):
        """Create style with custom colors for prompt and placeholder."""
        style_dict = {
            'prompt': f'{self.prompt_color} bold',
            'placeholder': self.placeholder_color,
            'line-number': '#666666',
            'line-number-separator': '#666666',
            'status': 'reverse',
            'validation-error': 'red bold',
        }
        return Style.from_dict(style_dict)


def test_color_identification():
    """Test user's ability to identify colors displayed in the terminal."""

    print("Color Identification Test")
    print("=========================")
    print("You will see prompts and placeholder text in different colors.")
    print("Type the color name you see (e.g., 'red', 'blue', 'white', etc.)")
    print("Press 'i' to enter insert mode, type your answer, then Enter to submit.")
    print("Press Ctrl-C to skip a test.")
    print()

    # List of colors to test
    test_colors = [
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white'
    ]

    results = {}

    # Test each color for both prompt and placeholder
    for color in test_colors:
        print(f"=== Testing {color.upper()} ===")

        # Test 1: Colored prompt with white placeholder
        print(f"Test: The prompt 'COLOR: ' should appear in {color.upper()}")
        print("The placeholder text should appear in WHITE")

        try:
            readline = ColorTestVimReadline(
                prompt_color=color,
                placeholder_color='white',
                prompt="COLOR: ",
                placeholder_text="WHITE",
                show_status=False
            )

            user_input = readline.run()
            if user_input:
                results[f"{color}_prompt"] = user_input.strip().lower()
                print(f"You said the prompt color was: {user_input}")
            else:
                results[f"{color}_prompt"] = "skipped"
                print("Skipped")

        except KeyboardInterrupt:
            results[f"{color}_prompt"] = "cancelled"
            print("Cancelled")
        except Exception as e:
            results[f"{color}_prompt"] = f"error: {e}"
            print(f"Error: {e}")

        print()

        # Test 2: White prompt with colored placeholder
        print(f"Test: The prompt 'COLOR: ' should appear in WHITE")
        print(f"The placeholder text should appear in {color.upper()}")

        try:
            readline = ColorTestVimReadline(
                prompt_color='white',
                placeholder_color=color,
                prompt="COLOR: ",
                placeholder_text=color.upper(),
                show_status=False
            )

            user_input = readline.run()
            if user_input:
                results[f"{color}_placeholder"] = user_input.strip().lower()
                print(f"You said the placeholder color was: {user_input}")
            else:
                results[f"{color}_placeholder"] = "skipped"
                print("Skipped")

        except KeyboardInterrupt:
            results[f"{color}_placeholder"] = "cancelled"
            print("Cancelled")
        except Exception as e:
            results[f"{color}_placeholder"] = f"error: {e}"
            print(f"Error: {e}")

        print()
        print("-" * 50)
        print()

    # Summary
    print("=== TEST RESULTS SUMMARY ===")
    print()

    for color in test_colors:
        prompt_result = results.get(f"{color}_prompt", "not tested")
        placeholder_result = results.get(f"{color}_placeholder", "not tested")

        print(f"{color.upper()}:")
        print(f"  Prompt: Expected '{color}', you saw '{prompt_result}'")
        print(f"  Placeholder: Expected '{color}', you saw '{placeholder_result}'")

        # Check accuracy
        prompt_correct = prompt_result == color
        placeholder_correct = placeholder_result == color

        if prompt_correct and placeholder_correct:
            print(f"  ✓ Both correct")
        elif prompt_correct:
            print(f"  ✓ Prompt correct, ✗ Placeholder incorrect")
        elif placeholder_correct:
            print(f"  ✗ Prompt incorrect, ✓ Placeholder correct")
        else:
            print(f"  ✗ Both incorrect")
        print()


if __name__ == "__main__":
    try:
        test_color_identification()
    except KeyboardInterrupt:
        print("\nColor identification test interrupted. Goodbye!")
    except Exception as e:
        print(f"Error running color identification test: {e}")
        print("This app requires running in a real terminal.")