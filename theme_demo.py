#!/usr/bin/env python3
"""
Theme Demo - Demonstrates the centralized theme system for VimReadline components.

This app shows how to:
1. Use default themes
2. Create custom themes
3. Override specific colors
4. Use pre-defined theme variants
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import (
    validated_vim_input,
    VimReadlineTheme,
    DarkTheme,
    LightTheme,
    MinimalTheme,
    create_custom_theme,
    email
)


def demo_default_theme():
    """Demo using the default theme."""
    print("=== Default Theme Demo ===")
    print("Using default dark theme optimized for dark terminals")

    result = validated_vim_input(
        prompt="Email (default): ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False)
    )

    if result:
        print(f"Result: {result}")
    else:
        print("Cancelled")
    print()


def demo_light_theme():
    """Demo using the light theme."""
    print("=== Light Theme Demo ===")
    print("Using light theme optimized for light terminals")

    light_theme = LightTheme()

    result = validated_vim_input(
        prompt="Email (light): ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        theme=light_theme
    )

    if result:
        print(f"Result: {result}")
    else:
        print("Cancelled")
    print()


def demo_minimal_theme():
    """Demo using the minimal theme."""
    print("=== Minimal Theme Demo ===")
    print("Using minimal theme with subtle colors")

    minimal_theme = MinimalTheme()

    result = validated_vim_input(
        prompt="Email (minimal): ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        theme=minimal_theme
    )

    if result:
        print(f"Result: {result}")
    else:
        print("Cancelled")
    print()


def demo_custom_theme():
    """Demo creating a custom theme."""
    print("=== Custom Theme Demo ===")
    print("Using custom cyan/magenta theme")

    custom_theme = create_custom_theme(
        placeholder='cyan italic',
        prompt='magenta bold',
        validation_error='yellow bold',
        border_active='cyan',
        border_valid='green',
        border_invalid='red'
    )

    result = validated_vim_input(
        prompt="Email (custom): ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        theme=custom_theme
    )

    if result:
        print(f"Result: {result}")
    else:
        print("Cancelled")
    print()


def demo_theme_override():
    """Demo overriding specific colors in existing theme."""
    print("=== Theme Override Demo ===")
    print("Dark theme with bright placeholder and green prompt")

    # Start with dark theme and override specific colors
    custom_theme = DarkTheme().override(
        placeholder='bright_cyan',
        prompt='green bold',
        validation_error='bright_red bold'
    )

    result = validated_vim_input(
        prompt="Email (override): ",
        placeholder_text="Enter your email address...",
        validator=email(allow_empty=False),
        theme=custom_theme
    )

    if result:
        print(f"Result: {result}")
    else:
        print("Cancelled")
    print()


def main():
    """Run all theme demos."""
    print("VimReadline Centralized Theme System Demo")
    print("=========================================")
    print("This demonstrates the new centralized theme system.")
    print("You can now easily customize colors without hunting through files!")
    print()

    demos = [
        ("Default Theme", demo_default_theme),
        ("Light Theme", demo_light_theme),
        ("Minimal Theme", demo_minimal_theme),
        ("Custom Theme", demo_custom_theme),
        ("Theme Override", demo_theme_override)
    ]

    try:
        for i, (name, demo_func) in enumerate(demos, 1):
            print(f"Demo {i}/5: {name}")
            demo_func()

            if i < len(demos):
                continue_demo = input("Press Enter to continue to next demo (or 'q' to quit): ")
                if continue_demo.lower() == 'q':
                    break
                print()

        print("Theme demos completed!")
        print()
        print("Key Benefits of Centralized Themes:")
        print("• All colors defined in one place (themes.py)")
        print("• Easy to create custom themes")
        print("• Override specific colors without changing others")
        print("• Pre-defined theme variants (Dark, Light, Minimal)")
        print("• Consistent styling across all VimReadline components")

    except KeyboardInterrupt:
        print("\nTheme demo interrupted. Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("This app requires running in a real terminal.")


if __name__ == "__main__":
    main()