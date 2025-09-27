#!/usr/bin/env python3
"""
Simple interactive Hello app using ValidatedVimReadline.

Asks for user's name and displays "Hello, <name>!" message.

Usage:
    python hello_app.py

The app will launch a vim-style input editor where you can:
- Type your name
- Use vim navigation (hjkl, i for insert mode, etc.)
- Press Enter to submit
- Press Ctrl-C to cancel
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import validated_vim_input, length


def main():
    """Simple Hello app using ValidatedVimReadline."""
    print("Simple Hello App")
    print("================")
    print("Enter your name using vim-style editing")
    print("(Press 'i' for insert mode, hjkl for navigation, Enter to submit, Ctrl-C to exit)")
    print()

    try:
        # Ask for user's name with basic validation (must not be empty)
        name = validated_vim_input(
            prompt="Name: ",
            placeholder_text="Enter your name...",
            validator=length(min_length=1, allow_empty=False),
            show_status=True
        )

        if name:
            print()
            print(f"Hello, {name.strip()}!")
        else:
            print()
            print("Goodbye!")

    except KeyboardInterrupt:
        print()
        print("Goodbye!")
    except Exception as e:
        print(f"Error: {e}")
        print("This app requires running in a real terminal.")
        print("Try running: python hello_app.py")


if __name__ == "__main__":
    main()