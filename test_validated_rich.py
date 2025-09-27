#!/usr/bin/env python3
"""
Quick test for ValidatedRichVimReadline to ensure imports and basic functionality work.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Test that ValidatedRichVimReadline imports work correctly."""
    print("Testing ValidatedRichVimReadline imports...")

    try:
        from vim_readline import ValidatedRichVimReadline, validated_rich_vim_input, ValidatedRichTheme
        print("ValidatedRichVimReadline imports working")
    except ImportError as e:
        print(f"Import error: {e}")
        return False

    try:
        from vim_readline.validated_rich import ValidatedRichVimReadline
        print("Direct import from validated_rich module working")
    except ImportError as e:
        print(f"Direct import error: {e}")
        return False

    return True


def test_theme_creation():
    """Test theme creation and configuration."""
    print("Testing ValidatedRichTheme creation...")

    try:
        from vim_readline import ValidatedRichTheme

        # Default theme
        default_theme = ValidatedRichTheme()
        assert default_theme.border_active == "blue"
        assert default_theme.border_valid == "green"
        assert default_theme.border_invalid == "red"
        print("Default theme creation working")

        # Custom theme
        custom_theme = ValidatedRichTheme(
            border_active="cyan",
            border_valid="yellow",
            border_invalid="magenta",
            border_title_active="bright_cyan"
        )
        assert custom_theme.border_active == "cyan"
        assert custom_theme.border_valid == "yellow"
        assert custom_theme.border_title_active == "bright_cyan"
        print("Custom theme creation working")

    except Exception as e:
        print(f"Theme creation error: {e}")
        return False

    return True


def test_class_instantiation():
    """Test ValidatedRichVimReadline class instantiation."""
    print("Testing ValidatedRichVimReadline instantiation...")

    try:
        from vim_readline import ValidatedRichVimReadline, ValidatedRichTheme, email

        # Basic instantiation
        readline = ValidatedRichVimReadline(
            initial_text="test",
            panel_title="Test Input"
        )
        assert readline.panel_title == "Test Input"
        assert readline._validation_state == "active"
        print("Basic instantiation working")

        # With validator and theme
        custom_theme = ValidatedRichTheme(border_active="magenta")
        readline_with_validation = ValidatedRichVimReadline(
            validator=email(allow_empty=False),
            theme=custom_theme,
            panel_box_style="double",
            hidden_input=True
        )
        assert readline_with_validation.validator is not None
        assert readline_with_validation.theme.border_active == "magenta"
        assert readline_with_validation.panel_box_style == "double"
        assert readline_with_validation.hidden_input == True
        print("Instantiation with validation and theme working")

    except Exception as e:
        print(f"Instantiation error: {e}")
        return False

    return True


def test_box_characters():
    """Test box character generation for different styles."""
    print("Testing box character generation...")

    try:
        from vim_readline.validated_rich import ValidatedRichVimReadline

        readline = ValidatedRichVimReadline()

        # Test different box styles
        styles = ["rounded", "square", "double", "heavy"]
        for style in styles:
            readline.panel_box_style = style
            box_chars = readline._get_box_characters()

            required_keys = ['top_left', 'top_right', 'bottom_left', 'bottom_right', 'horizontal', 'vertical']
            for key in required_keys:
                assert key in box_chars, f"Missing key {key} for style {style}"
                assert len(box_chars[key]) > 0, f"Empty value for {key} in style {style}"

        print("Box character generation working for all styles")

    except Exception as e:
        print(f"Box character generation error: {e}")
        return False

    return True


def test_validation_state_changes():
    """Test validation state changes."""
    print("Testing validation state changes...")

    try:
        from vim_readline.validated_rich import ValidatedRichVimReadline
        from vim_readline import email

        readline = ValidatedRichVimReadline(validator=email())

        # Initial state should be active
        assert readline._validation_state == "active"

        # Test validation with valid email
        result = readline._perform_validation("test@example.com")
        assert result.is_valid == True
        assert readline._validation_state == "valid"
        assert "Valid" in readline._validation_message

        # Test validation with invalid email
        result = readline._perform_validation("invalid-email")
        assert result.is_valid == False
        assert readline._validation_state == "invalid"
        assert len(readline._validation_message) > 0

        print("Validation state changes working")

    except Exception as e:
        print(f"Validation state change error: {e}")
        return False

    return True


if __name__ == "__main__":
    print("ValidatedRichVimReadline Test Suite")
    print("==================================")

    tests = [
        test_imports,
        test_theme_creation,
        test_class_instantiation,
        test_box_characters,
        test_validation_state_changes
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"Test {test_func.__name__} failed with exception: {e}")
            failed += 1
        print()

    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("All tests passed! ValidatedRichVimReadline is ready to use.")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)