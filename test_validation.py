#!/usr/bin/env python3
"""
Quick test script to verify the validation system works correctly.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import (
    email, date, integer, float_num, regex, length, custom, combine,
    ValidationResult
)


def test_validators():
    """Test all validator types to ensure they work correctly."""
    print("Testing ValidatedVimReadline validators...")

    # Test email validator
    email_validator = email(allow_empty=False)

    # Valid emails
    assert email_validator.validate("test@example.com").is_valid
    assert email_validator.validate("user.name+tag@domain.co.uk").is_valid

    # Invalid emails
    assert not email_validator.validate("invalid-email").is_valid
    assert not email_validator.validate("@domain.com").is_valid
    assert not email_validator.validate("").is_valid

    print("✓ Email validator working")

    # Test date validator
    date_validator = date(date_format="%Y-%m-%d", allow_empty=False)

    # Valid dates
    assert date_validator.validate("2024-12-25").is_valid
    assert date_validator.validate("2023-01-01").is_valid

    # Invalid dates
    assert not date_validator.validate("2024-13-01").is_valid
    assert not date_validator.validate("12/25/2024").is_valid
    assert not date_validator.validate("").is_valid

    print("✓ Date validator working")

    # Test integer validator
    int_validator = integer(min_value=1, max_value=100, allow_empty=False)

    # Valid integers
    assert int_validator.validate("1").is_valid
    assert int_validator.validate("50").is_valid
    assert int_validator.validate("100").is_valid

    # Invalid integers
    assert not int_validator.validate("0").is_valid
    assert not int_validator.validate("101").is_valid
    assert not int_validator.validate("3.14").is_valid
    assert not int_validator.validate("text").is_valid
    assert not int_validator.validate("").is_valid

    print("✓ Integer validator working")

    # Test float validator
    float_validator = float_num(min_value=0.0, max_value=10.0, allow_empty=False)

    # Valid floats
    assert float_validator.validate("0.0").is_valid
    assert float_validator.validate("3.14").is_valid
    assert float_validator.validate("10.0").is_valid
    assert float_validator.validate("5").is_valid  # Integer should work too

    # Invalid floats
    assert not float_validator.validate("-1.0").is_valid
    assert not float_validator.validate("10.1").is_valid
    assert not float_validator.validate("text").is_valid
    assert not float_validator.validate("").is_valid

    print("✓ Float validator working")

    # Test regex validator
    phone_pattern = r'^\(\d{3}\) \d{3}-\d{4}$'
    regex_validator = regex(phone_pattern, "Invalid phone format", allow_empty=False)

    # Valid phone numbers
    assert regex_validator.validate("(123) 456-7890").is_valid
    assert regex_validator.validate("(555) 123-4567").is_valid

    # Invalid phone numbers
    assert not regex_validator.validate("123-456-7890").is_valid
    assert not regex_validator.validate("(123)456-7890").is_valid
    assert not regex_validator.validate("").is_valid

    print("✓ Regex validator working")

    # Test length validator
    length_validator = length(min_length=3, max_length=20, allow_empty=False)

    # Valid lengths
    assert length_validator.validate("bob").is_valid
    assert length_validator.validate("alice123").is_valid
    assert length_validator.validate("superlongusername").is_valid

    # Invalid lengths
    assert not length_validator.validate("ab").is_valid
    assert not length_validator.validate("verylongusernamethatexceedslimit").is_valid
    assert not length_validator.validate("").is_valid

    print("✓ Length validator working")

    # Test custom validator
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

    custom_validator = custom(validate_password, allow_empty=False)

    # Valid passwords
    assert custom_validator.validate("Password123").is_valid
    assert custom_validator.validate("MySecret1").is_valid

    # Invalid passwords
    assert not custom_validator.validate("password").is_valid  # No uppercase/digit
    assert not custom_validator.validate("PASSWORD123").is_valid  # No lowercase
    assert not custom_validator.validate("Password").is_valid  # No digit
    assert not custom_validator.validate("Pass1").is_valid  # Too short
    assert not custom_validator.validate("").is_valid

    print("✓ Custom validator working")

    # Test composite validator
    composite_validator = combine(
        length(min_length=7, max_length=7, allow_empty=False),
        regex(r'^[A-Z]{2}-\d{4}$', "Format must be XX-NNNN", allow_empty=False)
    )

    # Valid composite
    assert composite_validator.validate("AB-1234").is_valid
    assert composite_validator.validate("XY-9999").is_valid

    # Invalid composite
    assert not composite_validator.validate("ABC-123").is_valid  # Wrong length
    assert not composite_validator.validate("ab-1234").is_valid  # Wrong case
    assert not composite_validator.validate("XX-ABCD").is_valid  # Wrong format
    assert not composite_validator.validate("").is_valid

    print("✓ Composite validator working")

    print("\n🎉 All validators are working correctly!")


def test_import():
    """Test that all imports work correctly."""
    print("Testing imports...")

    try:
        from vim_readline import ValidatedVimReadline, validated_vim_input
        print("✓ ValidatedVimReadline imports working")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

    try:
        from vim_readline.validators import (
            Validator, ValidationResult,
            EmailValidator, DateValidator, IntegerValidator, FloatValidator
        )
        print("✓ Validator class imports working")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

    return True


if __name__ == "__main__":
    if test_import():
        test_validators()
        print("\n✅ All tests passed! Validation system is ready to use.")
    else:
        print("\n❌ Import tests failed!")
        sys.exit(1)