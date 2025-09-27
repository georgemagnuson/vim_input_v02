#!/usr/bin/env python3
"""
Interactive Rich Demo App - Use the true interactive Rich box editor.

This app lets you actually type and edit text inside Rich boxes!
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main interactive demo app."""
    print("🎯 INTERACTIVE RICH BOX EDITOR")
    print("=" * 50)
    print()
    print("This app lets you type and edit text INSIDE Rich boxes!")
    print("The cursor and all editing happens within Rich box boundaries.")
    print()

    try:
        from vim_readline.true_rich_interactive import TrueRichInteractiveBox

        print("📋 CONTROLS:")
        print("  • Type to add text")
        print("  • Arrow keys: Navigate cursor")
        print("  • Enter: Create new line")
        print("  • Backspace: Delete characters")
        print("  • Ctrl+M (Return): Submit your text")
        print("  • Ctrl+C: Cancel and exit")
        print()
        print("🎨 RICH BOX STYLES AVAILABLE:")
        print("  • ROUNDED (default) - Rich's signature rounded corners")
        print("  • SQUARE - Clean square corners")
        print("  • DOUBLE - Double lines")
        print("  • HEAVY - Bold thick lines")
        print("  • ASCII - ASCII-only compatibility")
        print()

        # Get user preferences
        print("Choose your Rich box style:")
        print("1. ROUNDED (default)")
        print("2. SQUARE")
        print("3. DOUBLE")
        print("4. HEAVY")
        print("5. ASCII")
        print()

        try:
            choice = input("Enter choice (1-5, or press Enter for ROUNDED): ").strip()
            style_map = {
                "1": "ROUNDED",
                "2": "SQUARE",
                "3": "DOUBLE",
                "4": "HEAVY",
                "5": "ASCII",
                "": "ROUNDED"
            }
            rich_style = style_map.get(choice, "ROUNDED")
        except (EOFError, KeyboardInterrupt):
            rich_style = "ROUNDED"
            print()

        print(f"✅ Using {rich_style} box style")
        print()

        # Create the interactive Rich box
        app = TrueRichInteractiveBox(
            box_title=f'Interactive Rich Editor - {rich_style} Style',
            box_width=70,
            box_height=15,
            rich_box_style=rich_style,
            initial_text=f'Welcome to the Interactive Rich Box Editor!\n\nThis is a {rich_style} style box where you can:\n• Type and edit text\n• Navigate with arrow keys\n• Create new lines with Enter\n• See your cursor (│) position\n\nTry editing this text!'
        )

        print("🚀 Starting interactive Rich box editor...")
        print("(Look for the Rich box with a cursor where you can type)")
        print()

        # Run the interactive editor
        result = app.run_with_keyboard_input()

        # Show results
        print("\n" + "=" * 70)
        if result is not None:
            print("✅ SUCCESS! Here's what you entered:")
            print("-" * 50)
            print(result)
            print("-" * 50)
            print(f"📊 Statistics:")
            print(f"  • Characters: {len(result)}")
            print(f"  • Lines: {len(result.splitlines())}")
            print(f"  • Words: {len(result.split())}")
        else:
            print("❌ Cancelled or no input received")

        print("\n🎉 Interactive Rich Box Demo Complete!")

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nMake sure you have the required dependencies:")
        print("  pip install rich keyboard")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  • Make sure you have 'keyboard' library: pip install keyboard")
        print("  • On macOS, you may need to grant accessibility permissions")
        print("  • Try running with sudo if needed: sudo python interactive_rich_demo.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")