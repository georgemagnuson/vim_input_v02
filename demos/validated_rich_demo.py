#!/usr/bin/env python3
"""
Comprehensive demo of ValidatedRichVimReadline with state-based border coloring.

Demonstrates:
- Rich box styling with borders and titles
- State-based border coloring (blue=active, green=valid, red=invalid)
- Validation messages in bottom border (right-aligned)
- Validation on exit (not real-time to prevent bounceback)
- Custom theme configuration
- Different box styles and validation types
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vim_readline.validated_rich import (
    ValidatedRichVimReadline, validated_rich_vim_input, ValidatedRichTheme
)
from vim_readline import email, integer, regex, length, custom


def demo_email_validation():
    """Demo email validation with Rich styling."""
    print("=== Email Validation Demo (Rich Style) ===")
    print("Border colors: Blue=active, Green=valid, Red=invalid")
    print("Notice the border changes color based on validation state")
    print("Try entering invalid email first, then valid email")

    result = validated_rich_vim_input(
        prompt="Email: ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        panel_title="Email Input",
        panel_box_style="rounded"
    )

    if result is not None:
        print(f"✓ Email entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_password_input():
    """Demo hidden password input with custom theme."""
    print("=== Password Input Demo (Hidden + Custom Theme) ===")
    print("Hidden input with custom purple theme")
    print("Password requirements: 8+ chars, uppercase, lowercase, digit")

    # Custom purple theme
    purple_theme = ValidatedRichTheme(
        border_active="magenta",
        border_valid="bright_green",
        border_invalid="bright_red",
        border_title_active="bright_magenta",
        border_title_valid="bright_green",
        border_title_invalid="bright_red"
    )

    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Must contain uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Must contain lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Must contain digit"
        return True, ""

    result = validated_rich_vim_input(
        prompt="Password: ",
        placeholder_text="Enter secure password...",
        validator=custom(validate_password, allow_empty=False),
        hidden_input=True,
        mask_character='●',
        panel_title="Password Entry",
        panel_box_style="double",
        theme=purple_theme
    )

    if result is not None:
        print("✓ Password entered successfully (hidden)")
    else:
        print("✗ Cancelled")
    print()


def demo_box_styles():
    """Demo different box styles with validation."""
    print("=== Box Style Variations Demo ===")
    print("Testing different Rich box styles with validation")

    styles = [
        ("rounded", "Rounded corners (╭─╮)"),
        ("square", "Square corners (┌─┐)"),
        ("double", "Double lines (╔═╗)"),
        ("heavy", "Heavy lines (┏━┓)")
    ]

    for style, description in styles:
        print(f"\n{description}")
        result = validated_rich_vim_input(
            prompt="Input: ",
            placeholder_text=f"Enter text with {style} border...",
            validator=length(min_length=3, max_length=20, allow_empty=False),
            panel_title=f"Input ({style.title()})",
            panel_box_style=style
        )

        if result is not None:
            print(f"✓ Entered: {result}")
        else:
            print("✗ Cancelled")


def demo_complex_validation():
    """Demo complex validation with multiline input."""
    print("\n=== Complex Validation Demo ===")
    print("Product code validation: XX-NNNN format, exactly 7 characters")
    print("Watch the border color change when you submit")

    # Combine length and regex validation
    from vim_readline import combine
    product_validator = combine(
        length(min_length=7, max_length=7, allow_empty=False),
        regex(r'^[A-Z]{2}-\d{4}$', "Format must be XX-NNNN (uppercase letters, dash, digits)")
    )

    result = validated_rich_vim_input(
        prompt="Code: ",
        placeholder_text="XX-NNNN",
        validator=product_validator,
        panel_title="Product Code Entry",
        panel_box_style="heavy",
        show_line_numbers=False
    )

    if result is not None:
        print(f"✓ Valid product code: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_multiline_validation():
    """Demo multiline input with validation."""
    print("=== Multiline Validation Demo ===")
    print("Enter a description (50-200 characters)")
    print("Use Ctrl-J for new lines, Enter to submit")
    print("Notice validation message appears in bottom border")

    result = validated_rich_vim_input(
        prompt="Description: ",
        placeholder_text="Enter description (use Ctrl-J for new lines)...",
        validator=length(min_length=50, max_length=200, allow_empty=False),
        panel_title="Description Entry",
        panel_box_style="rounded",
        show_line_numbers=True
    )

    if result is not None:
        print(f"✓ Description entered ({len(result)} characters)")
        print(f"Content: {repr(result)}")
    else:
        print("✗ Cancelled")
    print()


def demo_age_validation():
    """Demo integer validation with custom theme."""
    print("=== Age Validation Demo (Custom Colors) ===")
    print("Enter age between 1 and 150")

    # Custom cyan/yellow theme
    custom_theme = ValidatedRichTheme(
        border_active="cyan",
        border_valid="yellow",
        border_invalid="red",
        border_title_active="bright_cyan",
        border_title_valid="bright_yellow",
        border_title_invalid="bright_red",
        validation_message_valid="bright_yellow",
        validation_message_invalid="bright_red"
    )

    result = validated_rich_vim_input(
        prompt="Age: ",
        placeholder_text="Enter your age...",
        validator=integer(min_value=1, max_value=150, allow_empty=False),
        panel_title="Age Entry",
        panel_box_style="square",
        theme=custom_theme
    )

    if result is not None:
        print(f"✓ Age entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def main():
    """Run all ValidatedRichVimReadline demos."""
    print("ValidatedRichVimReadline Demos")
    print("=============================")
    print("Rich-styled vim input with validation and state-based border colors")
    print()
    print("Key features:")
    print("• State-based border coloring (blue=active, green=valid, red=invalid)")
    print("• Validation messages in bottom border (right-aligned)")
    print("• Validation on exit (prevents real-time bounceback)")
    print("• Customizable themes and box styles")
    print("• Hidden input support for passwords")
    print()
    print("Use vim navigation (hjkl, insert mode with 'i', etc.)")
    print("Press Ctrl-C to cancel any input, or Enter to submit")
    print()

    demos = [
        demo_email_validation,
        demo_password_input,
        demo_age_validation,
        demo_complex_validation,
        demo_box_styles,
        demo_multiline_validation
    ]

    for i, demo_func in enumerate(demos, 1):
        try:
            demo_func()
            if i < len(demos):
                input("Press Enter to continue to next demo...")
                print()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break

    print("ValidatedRichVimReadline demos completed!")
    print("\nKey observations:")
    print("• Border color changes based on validation state")
    print("• Validation messages appear in bottom border")
    print("• No real-time validation bounce-back")
    print("• Rich visual styling with customizable themes")


if __name__ == "__main__":
    main()