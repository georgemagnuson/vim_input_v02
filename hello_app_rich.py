#!/usr/bin/env python3
"""
Simple interactive Hello app using ValidatedRichVimReadline.

Rich-styled version with state-based border coloring and validation.

Usage:
    python hello_app_rich.py

The app will launch a rich-styled vim input editor where you can:
- Type your name in a beautiful bordered box
- Use vim navigation (hjkl, i for insert mode, etc.)
- See border colors change based on validation state (blue→green/red)
- Press Enter to submit
- Press Ctrl-C to cancel
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import validated_rich_vim_input, length, VimReadlineTheme, DarkTheme, LightTheme


def main():
    """Simple Hello app using ValidatedRichVimReadline with rich styling."""
    print("Simple Hello App (Rich Style)")
    print("==============================")
    print("Enter your name in the rich-styled vim editor below")
    print("• Border colors: Blue=active, Green=valid, Red=invalid")
    print("• Vim mode shown in bottom-left corner (I=insert, V=visual, nothing=normal)")
    print("• Use vim navigation (i for insert, hjkl for movement)")
    print("• Press Enter to submit, Ctrl-C to exit")
    print()
    print("Theme Options:")
    print("1. Dark Theme (default) - Bright colors for dark terminals")
    print("2. Light Theme - Darker colors for light terminals")
    print("3. Custom Theme - Manual color specification")
    print()

    # Let user choose theme
    theme_choice = input("Choose theme (1, 2, 3) or press Enter for default: ").strip()

    if theme_choice == "2":
        hello_theme = LightTheme()
        print("Using Light Theme")
    elif theme_choice == "3":
        # Create a custom theme for demonstration
        hello_theme = VimReadlineTheme(**{
            'placeholder': 'cyan italic',
            'prompt': 'yellow bold',
            'border-active': '#4a9eff',      # Bright blue
            'border-valid': '#00ff88',       # Bright green
            'border-invalid': '#ff4444',     # Bright red
            'border-title-active': '#4a9eff bold',
            'border-title-valid': '#00ff88 bold',
            'border-title-invalid': '#ff4444 bold',
            'validation-message-valid': '#00ff88',
            'validation-message-invalid': '#ff4444'
        })
        print("Using Custom Theme")
    else:
        hello_theme = DarkTheme()
        print("Using Dark Theme (default)")

    print()

    try:
        # Ask for user's name with rich styling and validation
        name = validated_rich_vim_input(
            prompt="Name: ",
            placeholder_text="Enter your name here...",
            validator=length(min_length=1, max_length=50, allow_empty=False),
            panel_title="Hello App - Name Entry",
            panel_box_style="rounded",  # Beautiful rounded corners
            show_mode_in_border=True,   # Show vim mode in bottom border
            mode_style="initial",       # Use I/V/N style (nothing for normal)
            theme=hello_theme
        )

        if name:
            print()
            print("=" * 40)
            print(f"🎉 Hello, {name.strip()}! 🎉")
            print("=" * 40)
            print()
            print("Thanks for trying the Rich-styled vim input!")
        else:
            print()
            print("👋 Goodbye!")

    except KeyboardInterrupt:
        print()
        print("👋 Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("This app requires running in a real terminal.")
        print("Try running: python hello_app_rich.py")


if __name__ == "__main__":
    main()