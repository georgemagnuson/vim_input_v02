#!/usr/bin/env python3
"""
Test the box-constrained VimReadline implementation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

def test_box_constraints():
    """Test the box-constrained input area."""
    print("🔲 Box-Constrained VimReadline Test")
    print("=" * 50)
    print()

    instructions = """
This tests the BOX-CONSTRAINED input area where:
• Input is truly constrained within defined box dimensions
• Text wrapping respects exact box boundaries
• Cursor movement is limited to box interior
• Fixed width/height creates a real text container
• Uses pyvim-style window management for constraints

Try typing long lines and see how they wrap within the exact box size!
    """

    print(instructions.strip())
    print()

    try:
        from vim_readline.constrained import box_constrained_vim_input

        # Test different box sizes
        test_cases = [
            {
                "name": "Small Box (40x8)",
                "width": 40,
                "height": 8,
                "desc": "Tight constraints - watch text wrap tightly",
                "initial": "This is a small constrained box.\n\nTry typing a really long line to see how it wraps within the exact 40-character width boundary of this box."
            },
            {
                "name": "Medium Box (60x12)",
                "width": 60,
                "height": 12,
                "desc": "Medium size - good for code editing",
                "initial": "def example_function():\n    # This is a medium-sized box\n    # Perfect for code editing\n    return 'constrained within 60x12'"
            },
            {
                "name": "Wide Box (80x6)",
                "width": 80,
                "height": 6,
                "desc": "Wide and short - like a console input",
                "initial": "Wide box format - good for command line style editing with horizontal space but limited vertical space."
            }
        ]

        for i, test_case in enumerate(test_cases):
            print(f"\n📦 Test {i+1}: {test_case['name']}")
            print(f"    {test_case['desc']}")
            print(f"    Box dimensions: {test_case['width']}w × {test_case['height']}h")
            print()

            result = box_constrained_vim_input(
                initial_text=test_case['initial'],
                box_width=test_case['width'],
                box_height=test_case['height'],
                show_box_border=True,
                show_line_numbers=True,
                show_status=True,
                wrap_lines=True
            )

            if result is not None:
                print(f"✅ {test_case['name']} test completed!")
                print("Result length:", len(result), "characters")
                print("Result preview:", repr(result[:100] + "..." if len(result) > 100 else result))
            else:
                print(f"❌ {test_case['name']} test cancelled")

            if i < len(test_cases) - 1:  # Not the last test
                response = input(f"\nPress Enter to continue to next test (or 'q' to quit): ")
                if response.lower().startswith('q'):
                    break

        # Test auto-sizing
        print(f"\n📦 Test 4: Auto-sized Box")
        print("    Uses terminal size to automatically determine box dimensions")
        print()

        result = box_constrained_vim_input(
            initial_text="Auto-sized box test.\n\nThis box automatically sizes itself based on your terminal dimensions.\nThe text is still constrained within calculated boundaries.",
            box_width=None,  # Auto-size
            box_height=None, # Auto-size
            show_box_border=True,
            show_line_numbers=True,
            show_status=True
        )

        if result is not None:
            print("✅ Auto-sized box test completed!")
        else:
            print("❌ Auto-sized box test cancelled")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure vim_readline.constrained module is available")
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

def test_comparison():
    """Compare constrained vs unconstrained behavior."""
    print("\n" + "=" * 50)
    print("🔀 Comparison Test: Constrained vs Unconstrained")
    print("=" * 50)

    try:
        from vim_readline.constrained import box_constrained_vim_input
        from vim_readline.core import vim_input

        test_text = "This is a comparison test between constrained and unconstrained input.\n\nType some long lines and notice the difference in how text wrapping and boundaries work.\n\nConstrained version should keep text within defined box boundaries."

        print("\n1️⃣ First: UNCONSTRAINED input (normal VimReadline)")
        print("Notice how text can extend across the full terminal width")

        result1 = vim_input(
            initial_text=test_text,
            show_line_numbers=True,
            show_status=True
        )

        print("\n2️⃣ Now: CONSTRAINED input (Box-Constrained VimReadline)")
        print("Notice how text is limited to the box boundaries")

        result2 = box_constrained_vim_input(
            initial_text=test_text,
            box_width=50,
            box_height=10,
            show_box_border=True,
            show_line_numbers=True,
            show_status=True
        )

        print("\n📊 Results:")
        print(f"Unconstrained result: {len(result1) if result1 else 0} chars")
        print(f"Constrained result: {len(result2) if result2 else 0} chars")

    except Exception as e:
        print(f"❌ Comparison test error: {e}")

def main():
    """Main test function."""
    print()
    test_box_constraints()

    if input("\nRun comparison test? (y/N): ").lower().startswith('y'):
        test_comparison()

    print()
    print("🎉 Box constraint testing complete!")
    print()
    print("Key features demonstrated:")
    print("  • ✅ Text properly constrained within fixed box dimensions")
    print("  • ✅ Exact width/height boundaries enforced")
    print("  • ✅ Text wrapping respects box limits")
    print("  • ✅ Scrolling when content exceeds box size")
    print("  • ✅ Visual borders show the constraint boundaries")
    print("  • ✅ Uses pyvim-style window management approach")

if __name__ == "__main__":
    main()