#!/usr/bin/env python3
"""Debug the style issue."""

from vim_readline.core import VimReadline

# Create a basic VimReadline to check style
readline = VimReadline()
style = readline._create_style()

print("Style object:", type(style))
print("Style attributes:", dir(style))

if hasattr(style, 'style_rules'):
    print("style_rules:", type(style.style_rules))
    print("style_rules content:", style.style_rules)
else:
    print("No style_rules attribute")

# Try to access the actual style dict
if hasattr(style, '_style_dict'):
    print("_style_dict:", style._style_dict)
elif hasattr(style, 'style'):
    print("style:", style.style)
elif hasattr(style, '_styles'):
    print("_styles:", style._styles)