#!/usr/bin/env python3
"""
Validator Test App - Interactive application to test all ValidatedVimReadline validators.

Tests all built-in validators: email, date, integer, float, regex, length, custom, composite.
Demonstrates validation functionality with real user input.

Usage:
    python validator_test_app.py
"""

import sys
import os
import re
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import (
    validated_vim_input,
    email, date, integer, float_num, regex, length, custom, combine
)


def test_email_validator():
    """Test email validation."""
    print("=== Email Validator Test ===")
    print("Enter a valid email address")
    print("Valid examples: user@example.com, test.email+tag@domain.co.uk")

    result = validated_vim_input(
        prompt="Email: ",
        placeholder_text="Enter email address...",
        validator=email(allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid email: {result}")
    else:
        print("Cancelled")
    print()


def test_date_validator():
    """Test date validation."""
    print("=== Date Validator Test ===")
    print("Enter a date in YYYY-MM-DD format")
    print("Valid examples: 2024-12-25, 2023-01-01")

    result = validated_vim_input(
        prompt="Date: ",
        placeholder_text="YYYY-MM-DD",
        validator=date(date_format="%Y-%m-%d", allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid date: {result}")
    else:
        print("Cancelled")
    print()


def test_integer_validator():
    """Test integer validation with bounds."""
    print("=== Integer Validator Test ===")
    print("Enter an integer between 1 and 100")
    print("Valid examples: 1, 50, 100")

    result = validated_vim_input(
        prompt="Number: ",
        placeholder_text="Enter integer 1-100...",
        validator=integer(min_value=1, max_value=100, allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid integer: {result}")
    else:
        print("Cancelled")
    print()


def test_float_validator():
    """Test float validation with bounds."""
    print("=== Float Validator Test ===")
    print("Enter a decimal number between 0.0 and 10.0")
    print("Valid examples: 0.0, 3.14, 10.0, 5")

    result = validated_vim_input(
        prompt="Float: ",
        placeholder_text="Enter decimal 0.0-10.0...",
        validator=float_num(min_value=0.0, max_value=10.0, allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid float: {result}")
    else:
        print("Cancelled")
    print()


def test_regex_validator():
    """Test regex pattern validation."""
    print("=== Regex Validator Test ===")
    print("Enter a US phone number in format: (XXX) XXX-XXXX")
    print("Valid examples: (123) 456-7890, (555) 123-4567")

    phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'

    result = validated_vim_input(
        prompt="Phone: ",
        placeholder_text="(XXX) XXX-XXXX",
        validator=regex(phone_pattern, "Invalid phone format. Use: (XXX) XXX-XXXX", allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid phone number: {result}")
    else:
        print("Cancelled")
    print()


def test_length_validator():
    """Test length validation."""
    print("=== Length Validator Test ===")
    print("Enter a username between 3-20 characters")
    print("Valid examples: bob, alice123, superlongusername")

    result = validated_vim_input(
        prompt="Username: ",
        placeholder_text="3-20 characters...",
        validator=length(min_length=3, max_length=20, allow_empty=False),
        show_status=False
    )

    if result:
        print(f"Valid username: {result}")
    else:
        print("Cancelled")
    print()


def test_custom_validator():
    """Test custom function validation."""
    print("=== Custom Validator Test ===")
    print("Enter a password that meets these requirements:")
    print("- At least 8 characters long")
    print("- Contains uppercase letter")
    print("- Contains lowercase letter")
    print("- Contains digit")

    def validate_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isupper() for c in password):
            return False, "Password must contain uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain digit"
        return True, ""

    result = validated_vim_input(
        prompt="Password: ",
        placeholder_text="Enter secure password...",
        validator=custom(validate_password, allow_empty=False),
        hidden_input=True,
        mask_character='*',
        show_status=False
    )

    if result:
        print("Valid password entered (hidden)")
    else:
        print("Cancelled")
    print()


def test_composite_validator():
    """Test combining multiple validators."""
    print("=== Composite Validator Test ===")
    print("Enter a product code that is:")
    print("- Exactly 7 characters long")
    print("- Matches pattern: XX-NNNN (2 letters, dash, 4 digits)")
    print("Valid examples: AB-1234, XY-9999")

    # Combine length and regex validation
    product_validator = combine(
        length(min_length=7, max_length=7, allow_empty=False),
        regex(r'^[A-Z]{2}-\d{4}$', "Format must be XX-NNNN (uppercase letters, dash, digits)", allow_empty=False)
    )

    result = validated_vim_input(
        prompt="Product Code: ",
        placeholder_text="XX-NNNN",
        validator=product_validator,
        show_status=False
    )

    if result:
        print(f"Valid product code: {result}")
    else:
        print("Cancelled")
    print()


def main():
    """Run all validator tests."""
    print("Validator Test App")
    print("==================")
    print("This app tests all ValidatedVimReadline validators")
    print("(Press 'i' for insert mode, hjkl for navigation, Enter to submit, Ctrl-C to exit)")
    print()

    validators = [
        ("Email", test_email_validator),
        ("Date", test_date_validator),
        ("Integer", test_integer_validator),
        ("Float", test_float_validator),
        ("Regex (Phone)", test_regex_validator),
        ("Length (Username)", test_length_validator),
        ("Custom (Password)", test_custom_validator),
        ("Composite (Product Code)", test_composite_validator)
    ]

    try:
        for i, (name, test_func) in enumerate(validators, 1):
            print(f"Test {i}/8: {name}")
            test_func()

            if i < len(validators):
                continue_test = input("Press Enter to continue to next test (or 'q' to quit): ")
                if continue_test.lower() == 'q':
                    break
                print()

        print("All validator tests completed!")

    except KeyboardInterrupt:
        print("\nValidator testing interrupted. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("This app requires running in a real terminal.")


if __name__ == "__main__":
    main()