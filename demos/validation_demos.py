#!/usr/bin/env python3
"""
Comprehensive demo of ValidatedVimReadline with various validation types.

Demonstrates:
- Email validation
- Date validation
- Integer/Float validation with bounds
- Password input (hidden)
- Regex validation
- Length validation
- Custom validation functions
- Composite validation (multiple validators)
"""

import sys
import os

# Add parent directory to path so we can import vim_readline
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vim_readline import (
    validated_vim_input, ValidatedVimReadline,
    email, date, integer, float_num, regex, length, custom, combine
)


def demo_email_validation():
    """Demo email address validation."""
    print("=== Email Validation Demo ===")
    print("Enter an email address (try invalid formats to see validation)")
    print("Valid examples: user@example.com, test.email+tag@domain.co.uk")
    print("Invalid examples: invalid-email, @domain.com, user@")

    result = validated_vim_input(
        prompt="Email: ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid email entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_date_validation():
    """Demo date validation with specific format."""
    print("=== Date Validation Demo ===")
    print("Enter a date in YYYY-MM-DD format")
    print("Valid examples: 2024-12-25, 2023-01-01")
    print("Invalid examples: 12/25/2024, 2024-13-01, invalid-date")

    result = validated_vim_input(
        prompt="Date: ",
        placeholder_text="YYYY-MM-DD",
        validator=date(date_format="%Y-%m-%d", allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid date entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_integer_validation():
    """Demo integer validation with bounds."""
    print("=== Integer Validation Demo ===")
    print("Enter an integer between 1 and 100")
    print("Valid examples: 1, 50, 100")
    print("Invalid examples: 0, 101, 3.14, text")

    result = validated_vim_input(
        prompt="Number: ",
        placeholder_text="Enter integer 1-100...",
        validator=integer(min_value=1, max_value=100, allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid integer entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_float_validation():
    """Demo float validation with bounds."""
    print("=== Float Validation Demo ===")
    print("Enter a decimal number between 0.0 and 10.0")
    print("Valid examples: 0.0, 3.14, 10.0, 5")
    print("Invalid examples: -1.0, 10.1, text")

    result = validated_vim_input(
        prompt="Float: ",
        placeholder_text="Enter decimal 0.0-10.0...",
        validator=float_num(min_value=0.0, max_value=10.0, allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid float entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_password_validation():
    """Demo hidden password input with validation."""
    print("=== Password Validation Demo ===")
    print("Enter a password (input will be hidden)")
    print("Requirements: At least 8 characters, must contain uppercase, lowercase, and digit")

    # Custom validator for password strength
    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        return True, ""

    result = validated_vim_input(
        prompt="Password: ",
        placeholder_text="Enter secure password...",
        validator=custom(validate_password, allow_empty=False),
        hidden_input=True,
        mask_character='●',
        show_status=True
    )

    if result is not None:
        print("✓ Valid password entered (hidden)")
    else:
        print("✗ Cancelled")
    print()


def demo_regex_validation():
    """Demo regex pattern validation."""
    print("=== Regex Validation Demo ===")
    print("Enter a US phone number in format: (XXX) XXX-XXXX")
    print("Valid examples: (123) 456-7890, (555) 123-4567")
    print("Invalid examples: 123-456-7890, (123)456-7890, 555.123.4567")

    phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'

    result = validated_vim_input(
        prompt="Phone: ",
        placeholder_text="(XXX) XXX-XXXX",
        validator=regex(phone_pattern, "Invalid phone format. Use: (XXX) XXX-XXXX", allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid phone number entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_length_validation():
    """Demo length validation."""
    print("=== Length Validation Demo ===")
    print("Enter a username between 3-20 characters")
    print("Valid examples: bob, alice123, superlongusername")
    print("Invalid examples: ab, verylongusernamethatexceedslimit")

    result = validated_vim_input(
        prompt="Username: ",
        placeholder_text="3-20 characters...",
        validator=length(min_length=3, max_length=20, allow_empty=False),
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid username entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_composite_validation():
    """Demo combining multiple validators."""
    print("=== Composite Validation Demo ===")
    print("Enter a product code that is:")
    print("- Exactly 8 characters long")
    print("- Matches pattern: XX-NNNN (2 letters, dash, 4 digits)")
    print("Valid examples: AB-1234, XY-9999")
    print("Invalid examples: ABC-123, ab-1234, XX-ABCD, toolong")

    # Combine length and regex validation
    product_validator = combine(
        length(min_length=7, max_length=7, allow_empty=False),
        regex(r'^[A-Z]{2}-\d{4}$', "Format must be XX-NNNN (uppercase letters, dash, digits)", allow_empty=False)
    )

    result = validated_vim_input(
        prompt="Product Code: ",
        placeholder_text="XX-NNNN",
        validator=product_validator,
        show_status=True
    )

    if result is not None:
        print(f"✓ Valid product code entered: {result}")
    else:
        print("✗ Cancelled")
    print()


def demo_multiline_validation():
    """Demo validation with multiline input."""
    print("=== Multiline Validation Demo ===")
    print("Enter a short description (50-200 characters)")
    print("Use Ctrl-J for new lines, Enter to submit")
    print("Try entering text that's too short or too long to see validation")

    result = validated_vim_input(
        prompt="Description: ",
        placeholder_text="Enter description (use Ctrl-J for new lines)...",
        validator=length(min_length=50, max_length=200, allow_empty=False),
        show_status=True,
        show_line_numbers=True
    )

    if result is not None:
        print(f"✓ Valid description entered ({len(result)} characters)")
        print(f"Content: {repr(result)}")
    else:
        print("✗ Cancelled")
    print()


def main():
    """Run all validation demos."""
    print("VimReadline Validation Demos")
    print("============================")
    print("This demo showcases various validation types available in ValidatedVimReadline.")
    print("Use vim navigation (hjkl, insert mode with 'i', etc.)")
    print("Press Ctrl-C to cancel any input, or Enter to submit valid input.")
    print()

    demos = [
        demo_email_validation,
        demo_date_validation,
        demo_integer_validation,
        demo_float_validation,
        demo_password_validation,
        demo_regex_validation,
        demo_length_validation,
        demo_composite_validation,
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

    print("Demo completed! Thank you for trying ValidatedVimReadline.")


if __name__ == "__main__":
    main()