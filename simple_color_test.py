#!/usr/bin/env python3
"""
Simple color display test using prompt-toolkit's print_formatted_text.
This shows what different colors look like in the terminal.
"""

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style

def test_colors():
    """Test different color formats to see what works in the terminal."""

    print("=== Basic Color Test ===")
    print("Testing different color formats that ValidatedVimReadline could use:")
    print()

    # Test 1: Basic named colors
    print("1. Named colors:")
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    for color in colors:
        style = Style.from_dict({
            'testcolor': f'{color} italic'
        })
        print_formatted_text(
            HTML(f'<testcolor>This is {color} italic placeholder text</testcolor>'),
            style=style
        )

    print()

    # Test 2: Hex colors (what we're currently using)
    print("2. Hex colors:")
    hex_colors = [
        ('#ff0000', 'Red'),
        ('#00ff00', 'Green'),
        ('#0000ff', 'Blue'),
        ('#0066ff', 'Blue (current placeholder)'),
        ('#999999', 'Gray (old placeholder)'),
        ('#666666', 'Dark gray')
    ]

    for hex_color, name in hex_colors:
        style = Style.from_dict({
            'testhex': f'{hex_color} italic'
        })
        print_formatted_text(
            HTML(f'<testhex>This is {name} ({hex_color}) italic text</testhex>'),
            style=style
        )

    print()

    # Test 3: Different intensities
    print("3. Different intensities:")
    intensities = [
        ('blue', 'Normal blue'),
        ('#4444ff', 'Light blue hex'),
        ('#0066ff', 'Current blue hex'),
        ('#0033cc', 'Dark blue hex'),
        ('#0080ff', 'Brighter blue hex'),
        ('#002080', 'Darker blue hex')
    ]

    for color, name in intensities:
        style = Style.from_dict({
            'testintensity': f'{color} italic'
        })
        print_formatted_text(
            HTML(f'<testintensity>This is {name} ({color}) placeholder text</testintensity>'),
            style=style
        )

    print()

    # Test 4: What ValidatedVimReadline currently shows
    print("4. Current ValidatedVimReadline style simulation:")
    current_style = Style.from_dict({
        'prompt': 'bold',
        'placeholder': '#0066ff italic',
        'error': '#ff0000 bold'
    })

    print_formatted_text(
        HTML('<prompt>Email: </prompt><placeholder>Enter email address...</placeholder>'),
        style=current_style
    )
    print_formatted_text(
        HTML('<error>Error: Invalid email format</error>'),
        style=current_style
    )

if __name__ == "__main__":
    test_colors()