#!/usr/bin/env python3
"""
Rich Theme Showcase - Demonstrates all available theme variants with ValidatedRichVimReadline.

This demo showcases how the different theme variants (Dark, Light, Minimal, HighContrast, Neon)
work harmoniously with Rich-styled vim input, providing consistent theming across all components.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vim_readline import (
    validated_rich_vim_input,
    DarkTheme, LightTheme, MinimalTheme, HighContrastTheme, NeonTheme,
    email, length
)


def demo_theme_variant(theme_class, theme_name, description):
    """Demo a specific theme variant."""
    print(f"\n=== {theme_name} ===")
    print(description)
    print("Notice the Rich border colors and overall theme harmony")

    theme = theme_class()

    try:
        result = validated_rich_vim_input(
            prompt="Input: ",
            placeholder_text=f"Testing {theme_name.lower()} theme...",
            validator=length(min_length=1, max_length=50, allow_empty=False),
            panel_title=f"{theme_name} Theme Demo",
            panel_box_style="rounded",
            show_mode_in_border=True,
            mode_style="initial",
            theme=theme
        )

        if result is not None:
            print(f"You entered: {result}")
        else:
            print("Cancelled")

    except KeyboardInterrupt:
        print("Cancelled")


def main():
    """Run the Rich theme showcase."""
    print("Rich Theme Showcase")
    print("===================")
    print("This demo showcases all available theme variants with ValidatedRichVimReadline.")
    print("Each theme provides harmonious colors for both basic interface and Rich components.")
    print()
    print("Features demonstrated:")
    print("• State-based border coloring (blue=active, green=valid, red=invalid)")
    print("• Theme-consistent colors across all components")
    print("• Mode indicators in bottom-left corner")
    print("• Validation messages in bottom-right corner")
    print("• Perfect border alignment")
    print()
    print("Use vim navigation in each demo. Press Enter to submit, Ctrl-C to skip.")
    print()

    # Define all theme variants to showcase
    themes = [
        (DarkTheme, "Dark Theme", "Optimized for dark terminal backgrounds with bright, visible colors"),
        (LightTheme, "Light Theme", "Optimized for light terminal backgrounds with darker, readable colors"),
        (MinimalTheme, "Minimal Theme", "Subtle, muted colors for a clean, understated appearance"),
        (HighContrastTheme, "High Contrast Theme", "Maximum contrast colors for accessibility"),
        (NeonTheme, "Neon Theme", "Vibrant neon colors for a cyberpunk aesthetic")
    ]

    for i, (theme_class, theme_name, description) in enumerate(themes):
        try:
            demo_theme_variant(theme_class, theme_name, description)

            if i < len(themes) - 1:
                input("\nPress Enter to continue to next theme...")

        except KeyboardInterrupt:
            print("\n\nTheme showcase interrupted by user.")
            break

    print("\n" + "="*50)
    print("Rich Theme Showcase Complete!")
    print("="*50)
    print()
    print("Key observations:")
    print("• Each theme provides consistent colors across all components")
    print("• Rich border colors are optimized for each theme's target environment")
    print("• All themes maintain perfect border alignment and functionality")
    print("• Themes work seamlessly with validation, mode display, and all Rich features")
    print()
    print("Usage in your code:")
    print("```python")
    print("from vim_readline import validated_rich_vim_input, DarkTheme, LightTheme")
    print("")
    print("# Use a specific theme")
    print("result = validated_rich_vim_input(")
    print("    prompt='Name: ',")
    print("    theme=DarkTheme(),  # or LightTheme(), MinimalTheme(), etc.")
    print("    # ... other parameters")
    print(")")
    print("```")


if __name__ == "__main__":
    main()