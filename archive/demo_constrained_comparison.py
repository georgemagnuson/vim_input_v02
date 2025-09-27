#!/usr/bin/env python3
"""
Demo comparing constrained vs unconstrained VimReadline behavior.
"""

def demo_comparison():
    """Demonstrate the difference between constrained and unconstrained input."""
    print("🔄 VimReadline: Constrained vs Unconstrained Comparison")
    print("=" * 60)
    print()

    test_text = """This is a demonstration of text boundary constraints.

Try typing very long lines that would normally extend across the full terminal width. Notice how the constrained version keeps everything within defined boundaries.

You can use all vim commands:
- ESC: normal mode
- i: insert mode
- a: append
- o: new line below
- A: append at end of line
- And many more...

The key difference is in HOW the text is constrained within the editing area."""

    print("This demo will show you both versions side by side (conceptually).")
    print("First you'll try the UNCONSTRAINED version, then the CONSTRAINED version.")
    print()

    try:
        from vim_readline.core import vim_input
        from vim_readline.constrained import box_constrained_vim_input

        # First: Unconstrained
        print("📝 STEP 1: UNCONSTRAINED VimReadline")
        print("This is the normal VimReadline - text can extend to full terminal width")
        print("Press Enter to continue...")
        input()

        result1 = vim_input(
            initial_text=test_text,
            show_line_numbers=True,
            show_status=True
        )

        print("\n" + "─" * 60)
        print("📦 STEP 2: BOX-CONSTRAINED VimReadline")
        print("This version constrains text within a 70×15 box with borders")
        print("Notice how long lines wrap within the box boundaries!")
        print("Press Enter to continue...")
        input()

        result2 = box_constrained_vim_input(
            initial_text=test_text,
            box_width=70,
            box_height=15,
            show_box_border=True,
            show_line_numbers=True,
            show_status=True,
            wrap_lines=True
        )

        # Show results
        print("\n" + "=" * 60)
        print("📊 COMPARISON RESULTS")
        print("=" * 60)

        if result1 is not None:
            print(f"✅ Unconstrained result: {len(result1)} characters")
        else:
            print("❌ Unconstrained: cancelled")

        if result2 is not None:
            print(f"✅ Box-constrained result: {len(result2)} characters")
        else:
            print("❌ Box-constrained: cancelled")

        print("\n🎯 KEY DIFFERENCES DEMONSTRATED:")
        print("  • Unconstrained: Text flows to full terminal width")
        print("  • Constrained: Text wraps within fixed box dimensions")
        print("  • Constrained: Visual borders show the boundaries")
        print("  • Constrained: Uses pyvim-style window management")
        print("  • Both: Full vim editing capabilities maintained")

        if result1 and result2:
            print(f"\n📏 Length difference: {abs(len(result1) - len(result2))} characters")

    except ImportError as e:
        print(f"❌ Import error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def demo_different_box_sizes():
    """Demo different box constraint sizes."""
    print("\n" + "=" * 60)
    print("📐 Different Box Size Demo")
    print("=" * 60)

    try:
        from vim_readline.constrained import box_constrained_vim_input

        sizes = [
            ("Small", 40, 6, "Tight constraints for focused editing"),
            ("Medium", 60, 10, "Balanced size for general use"),
            ("Large", 80, 15, "Spacious for complex content")
        ]

        for name, width, height, desc in sizes:
            print(f"\n📦 {name} Box: {width}×{height}")
            print(f"   {desc}")

            if input("Try this size? (y/N): ").lower().startswith('y'):
                result = box_constrained_vim_input(
                    initial_text=f"{name} box ({width}×{height}) test.\n\nThis demonstrates how different box sizes affect the editing experience.\n\nTry typing long lines to see the wrapping behavior.",
                    box_width=width,
                    box_height=height,
                    show_box_border=True,
                    show_line_numbers=True,
                    show_status=True
                )

                if result:
                    print(f"✅ {name} box test completed!")
                else:
                    print(f"❌ {name} box test cancelled")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo function."""
    print("🚀 Box-Constrained VimReadline Demo")
    print()

    demo_comparison()

    if input("\nTry different box sizes demo? (y/N): ").lower().startswith('y'):
        demo_different_box_sizes()

    print("\n🎉 Demo complete!")
    print("\nThe box-constrained VimReadline successfully demonstrates:")
    print("  ✅ Proper text boundary constraints")
    print("  ✅ pyvim-style window management")
    print("  ✅ Visual box borders")
    print("  ✅ Configurable dimensions")
    print("  ✅ Full vim editing capabilities")

if __name__ == "__main__":
    main()