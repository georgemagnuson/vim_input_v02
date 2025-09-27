#!/usr/bin/env python3
"""
Interactive Theming Demo - Experience the ValidatedVimReadline theming system!

This demo showcases:
1. Pre-defined themes (Dark, Light, Minimal)
2. Custom theme creation
3. Instance-specific color overrides
4. Rich component theming
5. Real-world usage examples

Navigate through the demo to see how easy it is to customize colors!
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vim_readline import (
    validated_vim_input,
    VimReadlineTheme,
    DarkTheme,
    LightTheme,
    MinimalTheme,
    create_custom_theme,
    email,
    integer,
    custom
)

# Note: This demo focuses on the centralized theme system
# with ValidatedVimReadline as the primary component


def show_menu():
    """Display the demo menu."""
    print("\n" + "="*60)
    print("🎨 VALIDATEDVIMREADLINE INTERACTIVE THEMING DEMO 🎨")
    print("="*60)
    print("Choose a demo to experience the theming system:")
    print()
    print("1. 🌚 Dark Theme Demo (default)")
    print("2. ☀️  Light Theme Demo")
    print("3. 🎭 Minimal Theme Demo")
    print("4. 🌈 Custom Theme Creation")
    print("5. 🎯 Instance-Specific Overrides")
    print("6. 💎 Rich-Inspired Theming")
    print("7. 🏢 Real-World Example: User Registration")
    print("8. 🔄 Compare All Themes Side-by-Side")
    print("9. 📚 View Theme Documentation")
    print("0. 👋 Exit")
    print()


def demo_dark_theme():
    """Demo the default dark theme."""
    print("\n🌚 DARK THEME DEMO")
    print("=" * 40)
    print("This is the default theme, optimized for dark terminals.")
    print("Colors: Gray placeholder (#999999), bold prompt, red errors")
    print()

    # Simple input
    name = validated_vim_input(
        prompt="Name: ",
        placeholder_text="Enter your full name"
    )

    if name:
        # Email with validation
        email_addr = validated_vim_input(
            prompt="Email: ",
            placeholder_text="user@example.com",
            validator=email(allow_empty=False)
        )

        if email_addr:
            print(f"\n✅ Dark theme demo completed!")
            print(f"Name: {name}")
            print(f"Email: {email_addr}")
        else:
            print("Email input cancelled")
    else:
        print("Name input cancelled")


def demo_light_theme():
    """Demo the light theme."""
    print("\n☀️ LIGHT THEME DEMO")
    print("=" * 40)
    print("Optimized for light terminal backgrounds.")
    print("Colors: Darker grays, adjusted contrast")
    print()

    light_theme = LightTheme()

    name = validated_vim_input(
        prompt="Name: ",
        placeholder_text="Enter your full name",
        theme=light_theme
    )

    if name:
        age = validated_vim_input(
            prompt="Age: ",
            placeholder_text="Enter your age",
            validator=integer(min_value=1, max_value=150, allow_empty=False),
            theme=light_theme
        )

        if age:
            print(f"\n✅ Light theme demo completed!")
            print(f"Name: {name}")
            print(f"Age: {age}")
        else:
            print("Age input cancelled")
    else:
        print("Name input cancelled")


def demo_minimal_theme():
    """Demo the minimal theme."""
    print("\n🎭 MINIMAL THEME DEMO")
    print("=" * 40)
    print("Subtle colors for distraction-free editing.")
    print("Colors: Muted grays, minimal contrast")
    print()

    minimal_theme = MinimalTheme()

    username = validated_vim_input(
        prompt="Username: ",
        placeholder_text="Choose a username",
        theme=minimal_theme
    )

    if username:
        bio = validated_vim_input(
            prompt="Bio: ",
            placeholder_text="Tell us about yourself (optional)",
            theme=minimal_theme
        )

        print(f"\n✅ Minimal theme demo completed!")
        print(f"Username: {username}")
        print(f"Bio: {bio or '(none)'}")
    else:
        print("Username input cancelled")


def demo_custom_theme():
    """Demo creating custom themes."""
    print("\n🌈 CUSTOM THEME CREATION DEMO")
    print("=" * 40)
    print("See how easy it is to create custom color schemes!")
    print()

    # Cyberpunk theme
    print("🤖 First: Cyberpunk theme (cyan/magenta)")
    cyberpunk_theme = create_custom_theme(
        placeholder='cyan italic',
        prompt='magenta bold',
        validation_error='red bold',
        border_active='cyan',
        border_valid='green',
        border_invalid='red'
    )

    handle = validated_vim_input(
        prompt="Handle: ",
        placeholder_text="Enter your hacker handle",
        theme=cyberpunk_theme
    )

    if handle:
        # Nature theme
        print("\n🌿 Second: Nature theme (green/earth tones)")
        nature_theme = create_custom_theme(
            placeholder='#90EE90',  # Light green
            prompt='#8B4513 bold',  # Saddle brown
            validation_error='#FF6347 bold',  # Tomato red
        )

        location = validated_vim_input(
            prompt="Location: ",
            placeholder_text="Where are you in nature?",
            theme=nature_theme
        )

        if location:
            print(f"\n✅ Custom theme demo completed!")
            print(f"Cyberpunk Handle: {handle}")
            print(f"Nature Location: {location}")
        else:
            print("Location input cancelled")
    else:
        print("Handle input cancelled")


def demo_instance_overrides():
    """Demo instance-specific color overrides."""
    print("\n🎯 INSTANCE-SPECIFIC OVERRIDE DEMO")
    print("=" * 40)
    print("Use different colors for specific inputs while keeping")
    print("the same base theme for everything else.")
    print()

    # Normal dark theme for most inputs
    print("📝 Normal inputs use dark theme:")
    name = validated_vim_input(
        prompt="Name: ",
        placeholder_text="Your name"
    )

    if name:
        email_addr = validated_vim_input(
            prompt="Email: ",
            placeholder_text="your.email@example.com",
            validator=email(allow_empty=False)
        )

        if email_addr:
            # Special magenta prompt for the famous question
            print("\n🔥 Special input with magenta override:")
            daddy = validated_vim_input(
                prompt="Who is your daddy? ",
                placeholder_text="Type your answer...",
                theme=DarkTheme().override(
                    prompt='magenta bold',
                    placeholder='magenta italic'
                )
            )

            if daddy:
                # Back to normal theme
                print("\n📝 Back to normal theme:")
                comment = validated_vim_input(
                    prompt="Comment: ",
                    placeholder_text="Any additional comments?"
                )

                print(f"\n✅ Instance override demo completed!")
                print(f"Name: {name}")
                print(f"Email: {email_addr}")
                print(f"Daddy Answer: {daddy}")
                print(f"Comment: {comment or '(none)'}")
            else:
                print("Daddy question cancelled")
        else:
            print("Email input cancelled")
    else:
        print("Name input cancelled")


def demo_rich_theming():
    """Demo Rich component theming."""
    print("\n💎 RICH-INSPIRED THEMING DEMO")
    print("=" * 40)

    print("Rich components not available - showing themed ValidatedVimReadline instead!")
    print("This demonstrates how the centralized theme system works with basic components.")
    print()

    # Custom theme with Rich-inspired colors
    rich_inspired_theme = create_custom_theme(
        placeholder='cyan italic',
        prompt='blue bold',
        validation_error='red bold'
    )

    print("🎨 Rich-inspired themed input:")
    email_addr = validated_vim_input(
        prompt="Email: ",
        placeholder_text="Themed like Rich components would be!",
        validator=email(allow_empty=False),
        theme=rich_inspired_theme
    )

    if email_addr:
        # Password with different styling
        password_theme = create_custom_theme(
            placeholder='magenta',
            prompt='magenta bold',
            validation_error='red bold'
        )

        def strong_password(password):
            if len(password) < 8:
                return False, "Password must be at least 8 characters"
            if not any(c.isupper() for c in password):
                return False, "Must contain uppercase letter"
            if not any(c.islower() for c in password):
                return False, "Must contain lowercase letter"
            if not any(c.isdigit() for c in password):
                return False, "Must contain digit"
            return True, ""

        print("\n🔒 Themed password input (Rich-inspired):")
        password = validated_vim_input(
            prompt="Password: ",
            placeholder_text="Create a strong password",
            validator=custom(strong_password, allow_empty=False),
            hidden_input=True,
            mask_character='●',
            theme=password_theme
        )

        if password:
            print(f"\n✅ Rich theming demo completed!")
            print(f"Email: {email_addr}")
            print(f"Password: {'●' * len(password)} (hidden)")
        else:
            print("Password input cancelled")
    else:
        print("Email input cancelled")


def demo_real_world():
    """Demo a real-world user registration example."""
    print("\n🏢 REAL-WORLD EXAMPLE: USER REGISTRATION")
    print("=" * 40)
    print("See how different themes can be used together in a")
    print("real application to guide user attention and create")
    print("a polished experience.")
    print()

    print("🎬 Simulating a user registration flow with themed inputs:")
    print()

    # Step 1: Basic info (default theme)
    print("Step 1: Basic Information (Default Theme)")
    name = validated_vim_input(
        prompt="Full Name: ",
        placeholder_text="Enter your full name"
    )

    if not name:
        print("Registration cancelled")
        return

    # Step 2: Contact info (light theme for contrast)
    print("\nStep 2: Contact Information (Light Theme)")
    email_addr = validated_vim_input(
        prompt="Email: ",
        placeholder_text="your.email@example.com",
        validator=email(allow_empty=False),
        theme=LightTheme()
    )

    if not email_addr:
        print("Registration cancelled")
        return

    # Step 3: Security (special red theme for importance)
    print("\nStep 3: Security Setup (Important - Red Theme)")
    security_theme = DarkTheme().override(
        prompt='red bold',
        placeholder='red italic',
        validation_error='red bold'
    )

    def strong_password(password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        return True, ""

    password = validated_vim_input(
        prompt="Password: ",
        placeholder_text="Create a secure password",
        validator=custom(strong_password, allow_empty=False),
        theme=security_theme
    )

    if not password:
        print("Registration cancelled")
        return

    # Step 4: Optional info (minimal theme, less emphasis)
    print("\nStep 4: Optional Information (Minimal Theme)")
    bio = validated_vim_input(
        prompt="Bio: ",
        placeholder_text="Tell us about yourself (optional)",
        theme=MinimalTheme()
    )

    # Success with bright theme
    print("\n🎉 Registration Complete! (Success Theme)")
    success_theme = create_custom_theme(
        prompt='green bold',
        placeholder='green italic'
    )

    confirmation = validated_vim_input(
        prompt="Type 'CONFIRM' to finish: ",
        placeholder_text="CONFIRM",
        theme=success_theme
    )

    if confirmation and confirmation.upper() == 'CONFIRM':
        print(f"\n🎊 SUCCESS! Registration completed:")
        print(f"Name: {name}")
        print(f"Email: {email_addr}")
        print(f"Password: ●●●●●●●● (secure)")
        print(f"Bio: {bio or '(none provided)'}")
    else:
        print("Registration not confirmed")


def demo_side_by_side():
    """Compare all themes side by side."""
    print("\n🔄 SIDE-BY-SIDE THEME COMPARISON")
    print("=" * 40)
    print("Enter the same text with different themes to see the differences:")
    print()

    test_text = "sample@email.com"
    themes = [
        ("Dark Theme (Default)", DarkTheme()),
        ("Light Theme", LightTheme()),
        ("Minimal Theme", MinimalTheme()),
        ("Custom Cyan Theme", create_custom_theme(
            placeholder='cyan italic',
            prompt='cyan bold',
            validation_error='red bold'
        ))
    ]

    results = []
    for name, theme in themes:
        print(f"\n🎨 {name}:")
        result = validated_vim_input(
            prompt="Email: ",
            placeholder_text="Enter email to compare themes",
            validator=email(allow_empty=False),
            theme=theme
        )

        if result:
            results.append((name, result))
        else:
            print(f"{name} cancelled")
            break

    if len(results) == len(themes):
        print(f"\n✅ Theme comparison completed!")
        for name, result in results:
            print(f"{name}: {result}")
    else:
        print("Comparison incomplete")


def show_documentation():
    """Show key theming concepts."""
    print("\n📚 THEMING QUICK REFERENCE")
    print("=" * 40)
    print("""
🎨 BASIC USAGE:
   validated_vim_input("Prompt: ", theme=DarkTheme())

🌈 CUSTOM THEMES:
   theme = create_custom_theme(
       placeholder='cyan italic',
       prompt='yellow bold',
       validation_error='red bold'
   )

🎯 INSTANCE OVERRIDES:
   theme = DarkTheme().override(prompt='magenta bold')

🔧 AVAILABLE COLORS:
   • placeholder, prompt, status
   • validation-error, validation-valid
   • border-active, border-valid, border-invalid
   • line-number, line-number-separator

💡 COLOR FORMATS:
   • Named: 'red', 'green', 'cyan'
   • Hex: '#ff0000', '#999999'
   • Styled: 'red bold', 'cyan italic'
   • Bright: 'red', 'green'

📖 Full documentation: See THEMING.md
""")


def main():
    """Main demo loop."""
    print("Welcome to the ValidatedVimReadline Theming Demo!")
    print("This interactive demo showcases the powerful theming system.")
    print()
    print("💡 TIP: In each demo, try typing invalid input first to see")
    print("   validation error colors, then enter valid input to continue.")

    while True:
        show_menu()
        try:
            choice = input("Enter your choice (0-9): ").strip()

            if choice == '0':
                print("\n👋 Thanks for exploring the theming system!")
                print("Check out THEMING.md for complete documentation.")
                break
            elif choice == '1':
                demo_dark_theme()
            elif choice == '2':
                demo_light_theme()
            elif choice == '3':
                demo_minimal_theme()
            elif choice == '4':
                demo_custom_theme()
            elif choice == '5':
                demo_instance_overrides()
            elif choice == '6':
                demo_rich_theming()
            elif choice == '7':
                demo_real_world()
            elif choice == '8':
                demo_side_by_side()
            elif choice == '9':
                show_documentation()
            else:
                print("❌ Invalid choice. Please enter 0-9.")

            if choice != '0' and choice != '9':
                input("\nPress Enter to return to menu...")

        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("This demo requires running in a real terminal.")
            break


if __name__ == "__main__":
    main()