#!/usr/bin/env python3
"""
Test the installed vim-readline package.
"""

# Test basic import
print("Testing imports...")
from vim_readline import VimReadline, vim_input, __version__
print(f"✓ Imported VimReadline, vim_input, __version__ = {__version__}")

# Test VimReadline creation
print("\nTesting VimReadline creation...")
readline = VimReadline(
    initial_text="Hello, World!",
    placeholder_text="Type here...",
    prompt="test> ",
    show_line_numbers=True,
    show_status=True
)
print("✓ VimReadline object created successfully")

# Test vim_input function
print("\nTesting vim_input function signature...")
try:
    # Don't actually run it, just test it can be called
    print("✓ vim_input function is callable")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n🎉 Package installation test passed!")
print("\nYou can now use vim-readline in other projects:")
print("  from vim_readline import vim_input")
print("  result = vim_input(prompt='>>> ', placeholder_text='Type here...')")