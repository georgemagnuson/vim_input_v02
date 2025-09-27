# ValidatedVimReadline Theming Guide

This guide explains how to use the centralized theme system to customize the appearance of ValidatedVimReadline components.

## Overview

The theming system centralizes all color definitions in one place (`vim_readline/themes.py`), making it easy to:
- Use consistent colors across all VimReadline components
- Create custom themes without hunting through files
- Override specific colors for individual instances
- Switch between pre-defined theme variants

## Quick Start

### Basic Usage with Default Theme

```python
from vim_readline import validated_vim_input, email

# Uses default dark theme automatically
result = validated_vim_input(
    prompt="Email: ",
    placeholder_text="Enter your email...",
    validator=email()
)
```

### Using Pre-defined Themes

```python
from vim_readline import validated_vim_input, LightTheme, MinimalTheme

# Light theme for light terminal backgrounds
result = validated_vim_input(
    prompt="Email: ",
    theme=LightTheme()
)

# Minimal theme with subtle colors
result = validated_vim_input(
    prompt="Email: ",
    theme=MinimalTheme()
)
```

## Pre-defined Themes

### DarkTheme (Default)
Optimized for dark terminal backgrounds with good contrast:
- Placeholder: `#999999` (readable gray)
- Line numbers: `#666666`
- Borders: `#666666`
- Validation error: `#ff0000 bold` (red)

### LightTheme
Optimized for light terminal backgrounds:
- Placeholder: `#666666` (darker gray)
- Line numbers: `#888888`
- Borders: `#888888`
- Status bar: `bold bg:#f0f0f0 fg:#333333`

### MinimalTheme
Subtle colors for distraction-free editing:
- Placeholder: `#777777`
- Borders: `#444444`
- Muted validation colors

## Creating Custom Themes

### Method 1: Quick Custom Theme

```python
from vim_readline import create_custom_theme, validated_vim_input

# Create theme with specific color overrides
custom_theme = create_custom_theme(
    placeholder='cyan italic',
    prompt='yellow bold',
    validation_error='magenta bold',
    border_active='cyan',
    border_valid='green',
    border_invalid='red'
)

result = validated_vim_input(
    prompt="Custom: ",
    theme=custom_theme
)
```

### Method 2: Theme Class Inheritance

```python
from vim_readline import DarkTheme, validated_vim_input

class MyTheme(DarkTheme):
    """Custom theme based on dark theme."""
    def __init__(self):
        super().__init__(
            placeholder='bright_cyan',
            prompt='green bold',
            validation_error='#ff4444 bold'
        )

# Use your custom theme
result = validated_vim_input(
    prompt="Custom: ",
    theme=MyTheme()
)
```

## Instance-Specific Color Overrides

### Override Specific Colors

```python
from vim_readline import validated_vim_input, DarkTheme

# Most inputs use dark theme
normal_result = validated_vim_input("Email: ", theme=DarkTheme())

# One input with special magenta prompt
special_result = validated_vim_input(
    "Who is your daddy? ",
    theme=DarkTheme().override(prompt='magenta bold')
)

# Back to normal
another_result = validated_vim_input("Password: ", theme=DarkTheme())
```

### Multiple Overrides

```python
special_theme = DarkTheme().override(
    prompt='magenta bold',
    placeholder='magenta italic',
    validation_error='#ff4444 bold'
)

result = validated_vim_input(
    "Special question: ",
    theme=special_theme
)
```

## Available Color Keys

The theme system supports these color keys:

### Basic Interface
- `prompt`: Prompt text styling
- `placeholder`: Placeholder text color
- `status`: Status bar styling
- `line-number`: Line number color
- `line-number-separator`: Line separator color

### Validation
- `validation-error`: Error message color
- `validation-valid`: Valid state color
- `validation-warning`: Warning color

### Rich Components (ValidatedRichVimReadline)
- `border-active`: Active border color
- `border-valid`: Valid state border
- `border-invalid`: Invalid state border
- `border-title-active`: Active title color
- `border-title-valid`: Valid title color
- `border-title-invalid`: Invalid title color
- `validation-message-valid`: Valid message color
- `validation-message-invalid`: Invalid message color

### Advanced Styling
- `border-default`: Default border color
- `border-light`: Light border variant
- `border-dark`: Dark border variant
- `rich-border`: Rich component borders
- `rich-status`: Rich status bar styling
- `box-border`: Box component borders

## Color Format Examples

Colors can be specified in various formats:

```python
# Named colors
'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white'

# Hex colors
'#ff0000', '#00ff00', '#0066ff', '#999999'

# With styling
'red bold', 'cyan italic', 'yellow bold italic'

# Background colors
'bg:#2d3748 fg:#e2e8f0'

# Bright variants
'#ff4444', '#44ff44', '#4444ff'
```

## Complete Example: Multi-Theme Application

```python
from vim_readline import (
    validated_vim_input, validated_rich_vim_input,
    DarkTheme, LightTheme, create_custom_theme,
    email, integer
)

def themed_user_registration():
    """Example showing different themes for different inputs."""

    # Default dark theme for most inputs
    name = validated_vim_input(
        prompt="Name: ",
        placeholder_text="Enter your full name"
    )

    # Light theme for email (maybe user preference)
    email_addr = validated_vim_input(
        prompt="Email: ",
        placeholder_text="user@example.com",
        validator=email(),
        theme=LightTheme()
    )

    # Special bright theme for age input
    age_theme = create_custom_theme(
        prompt='bright_yellow bold',
        placeholder='yellow',
        validation_error='#ff4444 bold'
    )

    age = validated_vim_input(
        prompt="Age: ",
        placeholder_text="Enter your age",
        validator=integer(min_value=1, max_value=150),
        theme=age_theme
    )

    # Rich component with custom theme for password
    password_theme = DarkTheme().override(
        border_active='red',
        border_valid='green',
        border_invalid='#ff4444',
        validation_message_invalid='#ff4444 bold'
    )

    password = validated_rich_vim_input(
        prompt="Password: ",
        placeholder_text="Enter secure password",
        hidden_input=True,
        panel_title="Security",
        theme=password_theme
    )

    return {
        'name': name,
        'email': email_addr,
        'age': age,
        'password': password
    }
```

## Best Practices

### 1. Use Default Theme for Consistency
Start with the default theme and only override when needed:

```python
# Good: Consistent experience
result = validated_vim_input("Email: ")

# Also good: Intentional customization
result = validated_vim_input("Email: ", theme=custom_theme)
```

### 2. Create Named Themes for Reuse
If you use the same custom colors multiple times:

```python
# Good: Reusable theme
ERROR_THEME = DarkTheme().override(
    prompt='red bold',
    validation_error='#ff4444 bold'
)

# Use wherever you need error styling
error_input = validated_vim_input("Fix this: ", theme=ERROR_THEME)
```

### 3. Override Minimal Colors
Only override the colors you need to change:

```python
# Good: Minimal override
theme = DarkTheme().override(prompt='magenta bold')

# Avoid: Recreating entire theme for one color
# theme = create_custom_theme(prompt='magenta bold', ...)
```

### 4. Test with Different Terminal Backgrounds
Ensure your custom colors work with both dark and light terminals:

```python
# Consider providing both variants
DARK_SPECIAL = DarkTheme().override(placeholder='cyan')
LIGHT_SPECIAL = LightTheme().override(placeholder='blue')
```

## Integration with ValidatedRichVimReadline

The theme system works seamlessly with Rich components:

```python
from vim_readline import validated_rich_vim_input, create_custom_theme

# Rich theme with state-based border coloring
rich_theme = create_custom_theme(
    border_active='blue',
    border_valid='green',
    border_invalid='red',
    validation_message_valid='green',
    validation_message_invalid='red bold'
)

result = validated_rich_vim_input(
    prompt="Email: ",
    validator=email(),
    panel_title="User Registration",
    panel_box_style="rounded",
    theme=rich_theme
)
```

## Migration from Old System

If you were previously overriding `_create_style()` methods:

```python
# Old way (no longer needed)
class CustomValidatedVimReadline(ValidatedVimReadline):
    def _create_style(self):
        return Style.from_dict({
            'placeholder': 'cyan',
            'prompt': 'yellow bold'
            # ... other colors
        })

# New way (much simpler)
custom_theme = create_custom_theme(
    placeholder='cyan',
    prompt='yellow bold'
)

result = validated_vim_input(
    prompt="Input: ",
    theme=custom_theme
)
```

## Troubleshooting

### Theme Not Applied
Make sure you're passing the theme to the correct parameter:

```python
# Correct
validated_vim_input("Prompt: ", theme=my_theme)

# Wrong parameter name
validated_vim_input("Prompt: ", style=my_theme)  # Won't work
```

### Colors Not Visible
Test your colors in your terminal:

```python
from vim_readline import create_custom_theme

# Test theme with high contrast
test_theme = create_custom_theme(
    placeholder='bright_cyan',
    prompt='bright_yellow bold'
)
```

### Inheritance Issues
When creating theme classes, call parent constructor:

```python
class MyTheme(DarkTheme):
    def __init__(self):
        # Don't forget super().__init__()
        super().__init__(
            placeholder='custom_color'
        )
```

## API Reference

### VimReadlineTheme
- `__init__(**overrides)`: Create theme with color overrides
- `get_color(key, default='')`: Get specific color value
- `override(**colors)`: Create new theme with overrides
- `get_style_dict()`: Get dictionary for prompt-toolkit
- `get_prompt_toolkit_style()`: Get Style object

### Theme Functions
- `get_default_theme()`: Get default theme instance
- `create_custom_theme(**colors)`: Create custom theme quickly

### Pre-defined Theme Classes
- `DarkTheme()`: Dark terminal optimized
- `LightTheme()`: Light terminal optimized
- `MinimalTheme()`: Subtle, minimal colors