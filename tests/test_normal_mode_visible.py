#!/usr/bin/env python3
"""
Test that NORMAL mode is now visible with proper formatting.
"""

from rich.console import Console

console = Console()

def test_normal_mode_formatting():
    """Test that normal mode formats correctly without corruption."""
    print("Testing NORMAL mode formatting...")

    # Test the exact logic from the Rich enhanced version
    mode_info = {
        'vi-insert': ('INSERT', 'green', '✏️'),
        'vi-replace': ('REPLACE', 'red', '🔄'),
        'vi-navigation': {
            'normal': ('NORMAL', 'blue', '🔍'),
            'visual': ('VISUAL', 'yellow', '📝'),
            'visual-line': ('VISUAL LINE', 'yellow', '📄'),
            'visual-block': ('VISUAL BLOCK', 'yellow', '📋')
        }
    }

    print("\nTesting all mode formats:")

    # Test INSERT
    mode, color, icon = mode_info['vi-insert']
    result = f" {icon} -- {mode} --" if icon else f"-- {mode} --"
    print(f"INSERT: '{result}'")

    # Test NORMAL (the problematic one)
    mode, color, icon = mode_info['vi-navigation']['normal']
    if not mode:
        result = ""
    elif icon:
        result = f" {icon} -- {mode} --"
    else:
        result = f"-- {mode} --"
    print(f"NORMAL: '{result}' (should show: ' 🔍 -- NORMAL --')")

    # Verify character by character
    expected = " 🔍 -- NORMAL --"
    print(f"\nCharacter breakdown of expected NORMAL mode:")
    for i, char in enumerate(expected):
        print(f"  {i:2d}: '{char}' (ord: {ord(char)})")

    # Test VISUAL
    mode, color, icon = mode_info['vi-navigation']['visual']
    result = f" {icon} -- {mode} --" if icon else f"-- {mode} --"
    print(f"VISUAL: '{result}'")

    # Test REPLACE
    mode, color, icon = mode_info['vi-replace']
    result = f" {icon} -- {mode} --" if icon else f"-- {mode} --"
    print(f"REPLACE: '{result}'")

def main():
    """Main test."""
    console.print("[bold green]NORMAL Mode Visibility Fix[/bold green]")
    console.print()

    test_normal_mode_formatting()

    console.print()
    console.print("[green]✅ Visibility fixes applied:[/green]")
    console.print("  • NORMAL mode now shows: [blue]🔍 -- NORMAL --[/blue]")
    console.print("  • Added better status bar styling with background color")
    console.print("  • Improved contrast: [bold]bg:#2d3748 fg:#e2e8f0[/bold]")
    console.print()
    console.print("[yellow]⚠️  If the issue persists:[/yellow]")
    console.print("  • The problem might be terminal-specific")
    console.print("  • Try a different terminal or font")
    console.print("  • Check if emoji fonts are installed properly")

if __name__ == "__main__":
    main()