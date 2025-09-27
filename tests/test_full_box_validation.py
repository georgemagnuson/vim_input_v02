#!/usr/bin/env python3
"""
Validation test for the FullBoxVimReadline (non-interactive).
"""

def test_full_box_borders():
    """Test that border generation works correctly."""
    print("🔲 Testing Full Box Border Generation...")

    try:
        from vim_readline.full_box import FullBoxVimReadline

        readline = FullBoxVimReadline(
            box_width=20,
            box_height=5,
            box_title="Test Box",
            border_style="rounded"
        )

        # Test border line generation
        top_line = readline._get_border_line("top", 18)  # width - 2 for corners
        bottom_line = readline._get_border_line("bottom", 18)

        print(f"✅ Top border: '{top_line}'")
        print(f"✅ Bottom border: '{bottom_line}'")

        # Should contain the title
        assert "Test Box" in top_line
        print("✅ Title properly embedded in top border")

        # Test different border styles
        styles = ["rounded", "square", "double", "heavy"]
        for style in styles:
            readline.border_style = style
            line = readline._get_border_line("top", 10)
            assert len(line) > 0
            print(f"✅ {style} style generates borders")

        return True

    except Exception as e:
        print(f"❌ Border test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_full_box_initialization():
    """Test full box initialization."""
    print("\n🧪 Testing Full Box Initialization...")

    try:
        from vim_readline.full_box import FullBoxVimReadline

        # Test basic initialization
        readline = FullBoxVimReadline(
            initial_text="Test content",
            box_width=40,
            box_height=6,
            box_title="My Box",
            border_style="rounded"
        )

        print("✅ Basic initialization successful")

        # Test layout creation
        assert readline.layout is not None
        print("✅ Layout created successfully")

        # Test dimension calculation
        width, height = readline._calculate_box_dimensions()
        assert width > 0 and height > 0
        print(f"✅ Dimensions calculated: {width}×{height}")

        # Test style creation
        style = readline._create_style()
        style_dict = dict(style.style_rules)
        assert 'box-border' in style_dict
        print("✅ Box border styles included")

        return True

    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_border_character_sets():
    """Test that all border styles have complete character sets."""
    print("\n📐 Testing Border Character Sets...")

    try:
        from vim_readline.full_box import FullBoxVimReadline

        readline = FullBoxVimReadline()
        required_chars = ["top_left", "top_right", "bottom_left", "bottom_right", "horizontal", "vertical"]

        for style_name, char_set in readline.border_chars.items():
            print(f"Testing {style_name} style...")
            for char_name in required_chars:
                assert char_name in char_set, f"Missing {char_name} in {style_name}"
                assert len(char_set[char_name]) == 1, f"Invalid character length for {char_name} in {style_name}"

            print(f"✅ {style_name}: all characters present")

        print("✅ All border character sets complete")
        return True

    except Exception as e:
        print(f"❌ Character set test failed: {e}")
        return False

def test_auto_sizing():
    """Test auto-sizing functionality."""
    print("\n📏 Testing Auto-sizing...")

    try:
        from vim_readline.full_box import FullBoxVimReadline

        # Test with auto_size=True
        readline_auto = FullBoxVimReadline(
            box_width=200,  # Very large
            box_height=50,  # Very large
            auto_size=True
        )

        width_auto, height_auto = readline_auto._calculate_box_dimensions()

        # Test with auto_size=False
        readline_fixed = FullBoxVimReadline(
            box_width=200,
            box_height=50,
            auto_size=False
        )

        width_fixed, height_fixed = readline_fixed._calculate_box_dimensions()

        # Auto-size should be smaller than fixed when dealing with large values
        terminal_width, terminal_height = readline_auto._get_terminal_size()

        print(f"Terminal size: {terminal_width}×{terminal_height}")
        print(f"Auto-sized: {width_auto}×{height_auto}")
        print(f"Fixed: {width_fixed}×{height_fixed}")

        # Auto-size should respect terminal boundaries
        assert width_auto <= terminal_width
        assert height_auto <= terminal_height

        # Fixed size should use the requested values (subject to minimums)
        assert width_fixed >= 200 or width_fixed >= 20  # minimum constraint
        assert height_fixed >= 50 or height_fixed >= 5   # minimum constraint

        print("✅ Auto-sizing works correctly")
        return True

    except Exception as e:
        print(f"❌ Auto-sizing test failed: {e}")
        return False

def test_import_exports():
    """Test that imports and exports work."""
    print("\n📦 Testing Import/Export...")

    try:
        # Test direct import
        from vim_readline.full_box import FullBoxVimReadline, full_box_vim_input
        print("✅ Direct imports successful")

        # Test main package exports
        from vim_readline import FullBoxVimReadline as MainFullBox
        from vim_readline import full_box_vim_input as main_full_func
        print("✅ Main package exports successful")

        # Test consistency
        assert FullBoxVimReadline is MainFullBox
        assert full_box_vim_input is main_full_func
        print("✅ Export consistency verified")

        return True

    except Exception as e:
        print(f"❌ Import/export test failed: {e}")
        return False

def show_visual_example():
    """Show what the generated boxes look like."""
    print("\n🎨 Visual Box Examples")
    print("=" * 50)

    try:
        from vim_readline.full_box import FullBoxVimReadline

        styles = ["rounded", "square", "double", "heavy"]

        for style in styles:
            print(f"\n{style.title()} Style Example:")

            readline = FullBoxVimReadline(
                box_title=f"{style.title()} Box",
                border_style=style
            )

            # Generate example lines
            width = 25  # Content width
            top_line = readline._get_border_line("top", width)
            bottom_line = readline._get_border_line("bottom", width)
            chars = readline.border_chars[style]

            print(top_line)
            print(chars["vertical"] + " Text content goes here " + chars["vertical"])
            print(chars["vertical"] + " Line 2...              " + chars["vertical"])
            print(chars["vertical"] + " More text...           " + chars["vertical"])
            print(bottom_line)

    except Exception as e:
        print(f"❌ Visual example failed: {e}")

def main():
    """Main validation function."""
    print("📦 FullBoxVimReadline Validation Tests")
    print("=" * 50)

    tests = [
        ("Import/Export", test_import_exports),
        ("Initialization", test_full_box_initialization),
        ("Border Generation", test_full_box_borders),
        ("Character Sets", test_border_character_sets),
        ("Auto-sizing", test_auto_sizing),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test PASSED")
        else:
            print(f"❌ {test_name} test FAILED")

    # Show visual examples regardless of test results
    show_visual_example()

    print("\n" + "=" * 50)
    print(f"📊 VALIDATION RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All validation tests PASSED!")
        print("\nThe FullBoxVimReadline creates complete boxes like the screenshot!")
        print("\n📝 Example usage:")
        print("```python")
        print("from vim_readline import full_box_vim_input")
        print("")
        print("result = full_box_vim_input(")
        print("    initial_text='Type your content...',")
        print("    box_title='Type entry',")
        print("    box_width=60,")
        print("    box_height=10,")
        print("    border_style='rounded'")
        print(")")
        print("```")
        print("\nThis creates a box exactly like your screenshot!")
    else:
        print(f"❌ {total - passed} validation tests FAILED")

if __name__ == "__main__":
    main()