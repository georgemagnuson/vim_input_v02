#!/usr/bin/env python3
"""Quick test of the simple rich app function parameters."""

from vim_readline import rich_vim_input

# Test that all parameters are accepted
def test_parameters():
    """Test that rich_vim_input accepts all the parameters used in simple_rich_app."""
    try:
        # This should not raise a TypeError about unexpected keyword arguments
        print("Testing parameter acceptance...")

        # Test the parameters used in the app (don't actually run)
        params = {
            'initial_text': 'test',
            'panel_title': '🐍 Python Code Editor',
            'panel_box_style': 'rounded',
            'show_rules': True,
            'rule_style': 'green',
            'show_line_numbers': True,
            'show_status': True
        }

        # Check if function signature accepts these parameters
        import inspect
        sig = inspect.signature(rich_vim_input)

        print(f"Function signature: {sig}")

        for param_name in params:
            if param_name in sig.parameters:
                print(f"✓ {param_name} - supported")
            else:
                print(f"✗ {param_name} - NOT supported")

        print("\nAll parameter tests completed!")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    test_parameters()