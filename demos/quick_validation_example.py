#!/usr/bin/env python3
"""
Quick example showing ValidatedVimReadline usage.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vim_readline import validated_vim_input, email, integer


def main():
    print("Quick ValidatedVimReadline Example")
    print("=================================")

    # Email validation
    email_result = validated_vim_input(
        prompt="Email: ",
        placeholder_text="Enter your email...",
        validator=email(allow_empty=False)
    )

    if email_result:
        print(f"You entered: {email_result}")
    else:
        print("Email input cancelled")

    # Age validation
    age_result = validated_vim_input(
        prompt="Age: ",
        placeholder_text="Enter your age...",
        validator=integer(min_value=1, max_value=150, allow_empty=False)
    )

    if age_result:
        print(f"You entered: {age_result}")
    else:
        print("Age input cancelled")


if __name__ == "__main__":
    main()