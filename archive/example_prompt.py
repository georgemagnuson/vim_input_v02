#!/usr/bin/env python3
"""
Example showing different prompt styles with VimReadline.
"""

from vim_readline import vim_input


def demo_prompts():
    """Demonstrate different prompt styles."""

    print("=== Prompt Style Examples ===")
    print()

    # Python REPL style
    print("1. Python REPL style:")
    result = vim_input(
        prompt=">>> ",
        placeholder_text="print('Hello, World!')",
        show_status=True
    )
    print(f"Result: {repr(result)}")
    print()

    # Shell style
    print("2. Shell style:")
    result = vim_input(
        prompt="$ ",
        placeholder_text="ls -la",
        show_status=True
    )
    print(f"Result: {repr(result)}")
    print()

    # No prompt
    print("3. No prompt (clean):")
    result = vim_input(
        prompt="",
        placeholder_text="Type anything...",
        show_line_numbers=True,
        show_status=True
    )
    print(f"Result: {repr(result)}")
    print()

    # Custom prompt
    print("4. Custom prompt:")
    result = vim_input(
        prompt="[vim] ",
        placeholder_text="Enter vim commands or text...",
        show_status=True
    )
    print(f"Result: {repr(result)}")
    print()

    # SQL style
    print("5. SQL style:")
    result = vim_input(
        prompt="sql> ",
        placeholder_text="SELECT * FROM users;",
        show_status=False  # Hide status for cleaner look
    )
    print(f"Result: {repr(result)}")


if __name__ == "__main__":
    demo_prompts()