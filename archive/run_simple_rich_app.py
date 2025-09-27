#!/usr/bin/env python3
"""
Wrapper to test the simple Rich app with proper error handling.
"""

import sys

def main():
    """Run the simple Rich app with error handling."""
    try:
        # Test imports first
        from vim_readline import rich_vim_input
        from rich.console import Console

        console = Console()
        console.print("[green]✅ All imports successful![/green]")
        console.print("[blue]Starting Simple Rich App...[/blue]")
        console.print()

        # Import and run the app
        from simple_rich_app import main as app_main
        app_main()

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure to install dependencies:")
        print("  pip install rich")
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()