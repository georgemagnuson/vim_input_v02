#!/usr/bin/env python3
"""
Debug script to see what key codes are sent by different key combinations.
Press keys to see their codes, 'q' to quit.

This is a utility script for vim_readline development.
"""

from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window


def main():
    pressed_keys = []

    def update_display():
        if not pressed_keys:
            return "Press keys to see their codes. Press 'q' to quit.\n\n"

        lines = ["Recent key presses:", ""]
        for i, (key_name, key_data) in enumerate(pressed_keys[-10:]):  # Show last 10
            lines.append(f"{i+1:2}. Key: '{key_name}' Data: {repr(key_data)}")

        lines.extend(["", "Try pressing Shift-Return to see what code it sends!"])
        return "\n".join(lines)

    kb = KeyBindings()

    # Catch all possible keys and log them
    @kb.add('<any>')
    def _(event):
        key_name = event.key_sequence[0].key if event.key_sequence else 'unknown'
        key_data = event.data if hasattr(event, 'data') else 'no data'
        pressed_keys.append((key_name, key_data))

        # Quit on 'q'
        if key_name == 'q':
            event.app.exit()

    # Also try to catch some specific combinations that might be shift-return
    shift_return_candidates = [
        'c-j', 'c-m', 'enter', 'return',
        's-c-j', 's-c-m', 's-enter', 's-return',
        'escape', 'tab'
    ]

    for candidate in shift_return_candidates:
        try:
            @kb.add(candidate)
            def make_handler(key_name):
                def handler(event):
                    pressed_keys.append((f"SPECIAL: {key_name}", event.data if hasattr(event, 'data') else 'no data'))
                    if key_name == 'q':
                        event.app.exit()
                return handler

            kb.add(candidate)(make_handler(candidate))
        except ValueError:
            # Skip invalid keys
            pass

    layout = Layout(
        HSplit([
            Window(
                content=FormattedTextControl(update_display),
                height=None
            )
        ])
    )

    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True
    )

    print("Starting key debug mode...")
    print("Press Shift-Return to see what your terminal sends!")
    print("Press 'q' to quit.")

    app.run()


if __name__ == "__main__":
    main()