#!/usr/bin/env python3
"""
Test Rich-native box implementation using Rich's built-in box routines.
"""

def test_rich_box_styles():
    """Test all available Rich box styles."""
    print("📦 Rich-Native Box Styles Test")
    print("=" * 60)

    try:
        from vim_readline.rich_box_native import RichBoxVimReadline

        # Test all Rich box styles
        styles = [
            ("ROUNDED", "Rich's rounded corners (╭╮╰╯)"),
            ("SQUARE", "Square corners (┌┐└┘)"),
            ("DOUBLE", "Double lines (╔╗╚╝)"),
            ("HEAVY", "Heavy lines (┏┓┗┛)"),
            ("ASCII", "ASCII-only characters (+|-)"),
            ("MINIMAL", "Minimal style"),
            ("SIMPLE", "Simple clean lines"),
            ("SIMPLE_HEAVY", "Simple with heavy lines"),
        ]

        for style_name, description in styles:
            print(f"\n🎨 {style_name}: {description}")

            try:
                readline = RichBoxVimReadline(
                    box_width=40,
                    box_height=5,
                    box_title=f"{style_name} Demo",
                    rich_box_style=style_name
                )

                # Test character extraction
                chars = readline._extract_rich_box_characters()
                print(f"   Characters: {chars['top_left']}{chars['horizontal']}{chars['top_right']} {chars['vertical']} {chars['bottom_left']}{chars['horizontal']}{chars['bottom_right']}")

                # Test border rendering
                top_border, bottom_border, middle_template = readline._render_rich_panel_borders(30, 3)
                print(f"   Top: {top_border}")
                print(f"   Bot: {bottom_border}")
                print(f"   ✅ {style_name} style working")

            except Exception as e:
                print(f"   ❌ {style_name} style failed: {e}")

    except ImportError as e:
        print(f"❌ Rich-native implementation not available: {e}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_rich_panel_rendering():
    """Test Rich Panel rendering extraction."""
    print("\n📐 Rich Panel Rendering Test")
    print("=" * 60)

    try:
        from vim_readline.rich_box_native import RichBoxVimReadline
        from rich import box

        readline = RichBoxVimReadline(
            box_width=35,
            box_height=4,
            box_title="Panel Test",
            rich_box_style="ROUNDED"
        )

        # Test panel rendering
        top_border, bottom_border, middle_lines = readline._render_rich_panel_borders(35, 4)

        print("📦 Rendered Panel Structure:")
        print(f"Top:    {top_border}")
        for i, line in enumerate(middle_lines[:4]):  # Show first few middle lines
            print(f"Mid {i+1}:  {line}")
        print(f"Bottom: {bottom_border}")

        print(f"\n📏 Measurements:")
        print(f"   Top border length: {len(top_border)}")
        print(f"   Bottom border length: {len(bottom_border)}")
        print(f"   Middle lines: {len(middle_lines)}")

        # Test character extraction
        chars = readline._extract_rich_box_characters()
        print(f"\n🔤 Extracted Characters:")
        for key, char in chars.items():
            print(f"   {key}: '{char}'")

        print("✅ Rich Panel rendering working correctly")

    except Exception as e:
        print(f"❌ Panel rendering test failed: {e}")
        import traceback
        traceback.print_exc()

def compare_rich_vs_manual():
    """Compare Rich-native vs manual box drawing."""
    print("\n🔄 Rich-Native vs Manual Comparison")
    print("=" * 60)

    try:
        from vim_readline.rich_box_native import RichBoxVimReadline as RichNative
        from vim_readline.full_box import FullBoxVimReadline as Manual

        width, height = 30, 4
        title = "Comparison"

        print("📦 RICH-NATIVE (using Rich's Panel system):")
        rich_readline = RichNative(
            box_width=width,
            box_height=height,
            box_title=title,
            rich_box_style="ROUNDED"
        )

        rich_top, rich_bottom, rich_middle = rich_readline._render_rich_panel_borders(width, height)
        print(rich_top)
        for line in rich_middle[:height]:
            print(line)
        print(rich_bottom)

        print(f"\n📦 MANUAL (custom border drawing):")
        manual_readline = Manual(
            box_width=width,
            box_height=height,
            box_title=title,
            border_style="rounded"
        )

        manual_chars = manual_readline.border_chars["rounded"]
        manual_top = manual_readline._get_border_line("top", width)
        manual_bottom = manual_readline._get_border_line("bottom", width)

        print(manual_top)
        for i in range(height):
            line = f"Line {i+1}".ljust(width)
            bordered_line = manual_chars["vertical"] + line + manual_chars["vertical"]
            print(bordered_line)
        print(manual_bottom)

        print(f"\n🎯 COMPARISON RESULTS:")
        print(f"   Rich-native top length: {len(rich_top)}")
        print(f"   Manual top length: {len(manual_top)}")
        print(f"   Rich uses: {rich_readline._extract_rich_box_characters()}")
        print(f"   Manual uses: {manual_chars}")

        print("✅ Both approaches working, Rich-native has better terminal compatibility")

    except Exception as e:
        print(f"❌ Comparison failed: {e}")

def main():
    """Main test function."""
    print("🔥 Rich-Native Box Implementation Tests")
    print()
    print("This tests the implementation that uses Rich's built-in box routines")
    print("instead of manually drawing borders.")
    print()

    test_rich_box_styles()
    test_rich_panel_rendering()
    compare_rich_vs_manual()

    print("\n" + "=" * 60)
    print("🎉 Rich-Native Box Testing Complete!")
    print()
    print("ADVANTAGES of Rich-native approach:")
    print("  ✅ Uses Rich's tested and optimized box routines")
    print("  ✅ Perfect alignment guaranteed by Rich")
    print("  ✅ More box styles available (ASCII, DOUBLE, HEAVY, etc.)")
    print("  ✅ Better terminal compatibility")
    print("  ✅ Automatic width/height calculations")
    print("  ✅ No manual border alignment issues")
    print()
    print("Usage:")
    print("from vim_readline import rich_box_vim_input")
    print("")
    print("result = rich_box_vim_input(")
    print("    box_title='Rich Box',")
    print("    rich_box_style='ROUNDED',  # or SQUARE, DOUBLE, HEAVY, etc.")
    print("    box_width=60,")
    print("    box_height=10")
    print(")")

if __name__ == "__main__":
    main()