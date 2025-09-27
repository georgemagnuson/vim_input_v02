#!/usr/bin/env python3
"""
Demo of the FullBoxVimReadline that draws complete borders like the screenshot.
"""

def demo_full_box():
    """Demonstrate the full box input like the screenshot."""
    print("📦 Full Box VimReadline Demo")
    print("=" * 50)
    print()
    print("This creates a complete drawn box around the input area,")
    print("exactly like the 'Type entry' box shown in the screenshot!")
    print()

    try:
        from vim_readline.full_box import full_box_vim_input

        # Demo different box styles
        examples = [
            {
                "title": "Type entry",
                "width": 60,
                "height": 8,
                "style": "rounded",
                "text": "Enter your text here...\n\nThis box looks just like the screenshot with complete borders on all sides."
            },
            {
                "title": "Code Input",
                "width": 70,
                "height": 12,
                "style": "square",
                "text": "def example():\n    # Your code here\n    pass\n\nThis is perfect for code input with square borders."
            },
            {
                "title": "Important Note",
                "width": 50,
                "height": 6,
                "style": "double",
                "text": "This is a double-border box for important content!"
            }
        ]

        for i, example in enumerate(examples):
            print(f"📝 Example {i+1}: {example['title']}")
            print(f"   Style: {example['style']} borders")
            print(f"   Size: {example['width']}×{example['height']}")
            print()

            # This would create a box like:
            # ┌─── Type entry ────┐
            # │ Enter your text   │
            # │ here...           │
            # │                   │
            # └───────────────────┘

            result = full_box_vim_input(
                initial_text=example["text"],
                box_title=example["title"],
                box_width=example["width"],
                box_height=example["height"],
                border_style=example["style"],
                show_line_numbers=True,
                show_status=True,
                wrap_lines=True
            )

            if result is not None:
                print(f"✅ {example['title']} completed!")
                print(f"   Result: {len(result)} characters")
            else:
                print(f"❌ {example['title']} cancelled")

            if i < len(examples) - 1:
                if input("\nContinue to next example? (Enter/n): ").lower().startswith('n'):
                    break

        # Show border style comparison
        print("\n" + "=" * 50)
        print("🎨 Border Style Comparison")
        print()

        styles = [
            ("rounded", "Standard rounded corners (like screenshot)"),
            ("square", "Clean square corners"),
            ("double", "Double-line borders for emphasis"),
            ("heavy", "Heavy/thick borders")
        ]

        for style, desc in styles:
            print(f"📦 {style.title()} Style: {desc}")
            if input("Try this style? (y/N): ").lower().startswith('y'):
                result = full_box_vim_input(
                    initial_text=f"This demonstrates the {style} border style.\n\nNotice how the borders are drawn completely around the text area!",
                    box_title=f"{style.title()} Demo",
                    box_width=55,
                    box_height=8,
                    border_style=style,
                    show_status=True
                )

                if result:
                    print(f"✅ {style.title()} style demo completed!")
                else:
                    print(f"❌ {style.title()} style demo cancelled")

    except ImportError as e:
        print(f"❌ Import error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_ascii_preview():
    """Show what the boxes look like in ASCII."""
    print("\n📋 Box Preview (ASCII art)")
    print("=" * 50)

    styles = {
        "rounded": {
            "top_left": "┌", "top_right": "┐",
            "bottom_left": "└", "bottom_right": "┘",
            "horizontal": "─", "vertical": "│"
        },
        "square": {
            "top_left": "┌", "top_right": "┐",
            "bottom_left": "└", "bottom_right": "┘",
            "horizontal": "─", "vertical": "│"
        },
        "double": {
            "top_left": "╔", "top_right": "╗",
            "bottom_left": "╚", "bottom_right": "╝",
            "horizontal": "═", "vertical": "║"
        },
        "heavy": {
            "top_left": "┏", "top_right": "┓",
            "bottom_left": "┗", "bottom_right": "┛",
            "horizontal": "━", "vertical": "┃"
        }
    }

    for name, chars in styles.items():
        print(f"\n{name.title()} Style:")
        width = 30

        # Top border with title
        title = f" {name} example "
        remaining = width - len(title)
        left_pad = remaining // 2
        right_pad = remaining - left_pad
        top_line = chars["top_left"] + chars["horizontal"] * left_pad + title + chars["horizontal"] * right_pad + chars["top_right"]

        print(top_line)
        print(chars["vertical"] + " Your text content goes here  " + chars["vertical"])
        print(chars["vertical"] + " Line 2 of text...            " + chars["vertical"])
        print(chars["vertical"] + " Line 3...                    " + chars["vertical"])
        print(chars["bottom_left"] + chars["horizontal"] * width + chars["bottom_right"])

def main():
    """Main demo function."""
    print()

    # Show ASCII previews first
    show_ascii_preview()

    print()
    print("Ready to try the interactive full box input?")
    if input("Start demo? (Y/n): ").lower() not in ['n', 'no']:
        demo_full_box()

    print()
    print("🎉 Full Box Demo Complete!")
    print()
    print("The FullBoxVimReadline creates complete bordered boxes like:")
    print("┌─── Title ────────┐")
    print("│ Text content     │")
    print("│ goes here...     │")
    print("└──────────────────┘")
    print()
    print("Perfect for creating input areas that look exactly")
    print("like the screenshot you showed!")

if __name__ == "__main__":
    main()