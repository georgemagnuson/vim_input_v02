#!/usr/bin/env python3
"""
Example usage of VimReadline.

Demonstrates various features:
- Basic usage with placeholder text
- Pre-populated content
- Line numbers and status indicators
- Different configuration options
"""

from . import VimReadline, vim_input


def example_basic():
    """Basic usage with placeholder text."""
    print("=== Basic Usage (with placeholder) ===")
    print("Try typing some text. Use Return to submit, Ctrl-J (or Shift-Return) for newline.")
    print("ESC switches to normal mode, i/a/o enter insert mode.")
    print()

    result = vim_input(
        prompt=">>> ",
        placeholder_text="Type your message here...",
        show_line_numbers=False,
        show_status=True
    )

    if result is not None:
        print(f"You entered:\n{repr(result)}")
    else:
        print("Cancelled!")
    print()


def example_prepopulated():
    """Example with pre-populated content."""
    print("=== Pre-populated Content ===")
    print("Edit the Python function below:")
    print()

    initial_code = """def hello_world():
    print("Hello, World!")
    return "success" """

    result = vim_input(
        initial_text=initial_code,
        show_line_numbers=True,
        show_status=True,
        wrap_lines=True
    )

    if result is not None:
        print("Final code:")
        print(result)
    else:
        print("Cancelled!")
    print()


def example_advanced():
    """Advanced usage with custom configuration."""
    print("=== Advanced Configuration ===")
    print("Custom key bindings and styling:")
    print()

    readline = VimReadline(
        initial_text="Edit this text...\nLine 2\nLine 3",
        placeholder_text="This won't show since we have initial text",
        show_line_numbers=True,
        show_status=True,
        wrap_lines=False,
        submit_key='c-m',      # Return
        newline_key='c-j',     # Ctrl-J (newline)
        cancel_keys=['c-c']    # Only Ctrl-C cancels
    )

    result = readline.run()

    if result is not None:
        print("Result:")
        print(result)
    else:
        print("Cancelled!")
    print()


def example_empty():
    """Example with empty buffer."""
    print("=== Empty Buffer ===")
    print("Start with completely empty buffer:")
    print()

    result = vim_input(
        initial_text="",
        placeholder_text="Start typing...",
        show_line_numbers=False,
        show_status=True
    )

    if result is not None:
        print(f"You entered: {repr(result)}")
    else:
        print("Cancelled!")
    print()


def demo_vim_features():
    """Demonstrate vim features."""
    print("=== Vim Features Demo ===")
    print("Try these vim commands:")
    print("- hjkl for movement")
    print("- w/b for word movement")
    print("- 0/$ for line start/end")
    print("- dd to delete line")
    print("- yy to yank line, p to paste")
    print("- u for undo, Ctrl-R for redo")
    print("- v for visual mode, V for visual line")
    print("- /text to search")
    print("- :s/old/new/g for substitute")
    print()

    sample_text = """Line 1: The quick brown fox
Line 2: jumps over the lazy dog
Line 3: This is a sample text
Line 4: for testing vim features"""

    result = vim_input(
        initial_text=sample_text,
        show_line_numbers=True,
        show_status=True
    )

    if result is not None:
        print("Edited text:")
        print(result)
    else:
        print("Cancelled!")


def main():
    """Main entry point for console script."""
    print("VimReadline Examples")
    print("===================")
    print()

    examples = [
        ("1", "Basic usage (with prompt)", example_basic),
        ("2", "Pre-populated content", example_prepopulated),
        ("3", "Advanced configuration", example_advanced),
        ("4", "Empty buffer", example_empty),
        ("5", "Vim features demo", demo_vim_features),
    ]

    while True:
        print("Choose an example:")
        for key, desc, _ in examples:
            print(f"  {key}. {desc}")
        print("  q. Quit")
        print()

        choice = input("Enter choice (1-5, q): ").strip().lower()

        if choice == 'q':
            print("Goodbye!")
            break

        for key, desc, func in examples:
            if choice == key:
                print()
                func()
                input("Press Enter to continue...")
                print("\n" + "="*50 + "\n")
                break
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()