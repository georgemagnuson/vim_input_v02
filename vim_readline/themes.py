"""
Centralized theme system for VimReadline components.

This module provides a unified color theme system that allows programmers to:
1. Use sensible defaults for all VimReadline components
2. Override specific colors as needed
3. Create custom themes easily
4. Maintain consistency across all vim readline variants
"""

from typing import Dict, Optional, Any
from prompt_toolkit.styles import Style


class VimReadlineTheme:
    """
    Centralized theme configuration for all VimReadline components.

    This class defines all colors used across the vim readline ecosystem in one place,
    making it easy for programmers to customize appearance without hunting through files.
    """

    def __init__(self, **overrides):
        """
        Initialize theme with default colors and optional overrides.

        Args:
            **overrides: Any color definitions to override defaults
                        (e.g., placeholder='cyan', prompt='yellow bold')
        """
        # Core text and interface colors
        self.colors = {
            # Basic interface elements
            'prompt': 'bold',
            'placeholder': '#999999',  # Readable gray for placeholder text
            'status': 'reverse',

            # Line numbers and separators
            'line-number': '#666666',
            'line-number-separator': '#666666',

            # Validation states
            'validation-error': '#ff0000 bold',  # Red error messages
            'validation-valid': '#00ff00',       # Green for valid state
            'validation-warning': '#ffaa00',     # Orange for warnings

            # Rich component borders (various styles) - bright colors for visibility
            'border-default': '#666666',
            'border-active': '#4a9eff',      # Bright blue
            'border-valid': '#00ff88',       # Bright green
            'border-invalid': '#ff4444',     # Bright red
            'border-light': '#888888',
            'border-dark': '#444444',

            # Rich component titles and messages - bright colors
            'border-title-active': '#4a9eff bold',
            'border-title-valid': '#00ff88 bold',
            'border-title-invalid': '#ff4444 bold',
            'validation-message-valid': '#00ff88',
            'validation-message-invalid': '#ff4444',

            # Rich enhanced styling
            'rich-border': '#666666',
            'rich-status': 'bold bg:#2d3748 fg:#e2e8f0',
            'rich-box-border': '#888888',

            # Box component styling
            'box-border': '#666666',
        }

        # Apply any overrides
        self.colors.update(overrides)

    def get_style_dict(self) -> Dict[str, str]:
        """
        Get the complete style dictionary for prompt-toolkit.

        Returns:
            Dict mapping style class names to style definitions
        """
        return self.colors.copy()

    def get_prompt_toolkit_style(self) -> Style:
        """
        Get a prompt-toolkit Style object with all theme colors.

        Returns:
            Style object ready to use with prompt-toolkit applications
        """
        return Style.from_dict(self.get_style_dict())

    def override(self, **new_colors) -> 'VimReadlineTheme':
        """
        Create a new theme with some colors overridden.

        Args:
            **new_colors: Color definitions to override

        Returns:
            New VimReadlineTheme instance with overrides applied
        """
        return VimReadlineTheme(**{**self.colors, **new_colors})

    def get_color(self, key: str, default: str = '') -> str:
        """
        Get a specific color from the theme.

        Args:
            key: Color key (e.g., 'placeholder', 'prompt')
            default: Default value if key not found

        Returns:
            Color definition string
        """
        return self.colors.get(key, default)


# Pre-defined theme variants
class DarkTheme(VimReadlineTheme):
    """Dark theme optimized for dark terminal backgrounds."""

    def __init__(self, **overrides):
        dark_colors = {
            # Basic interface
            'placeholder': '#999999',  # Light gray for dark backgrounds
            'line-number': '#666666',
            'border-default': '#666666',
            'rich-status': 'bold bg:#2d3748 fg:#e2e8f0',

            # Rich component borders - bright colors for dark backgrounds
            'border-active': '#5aa3f0',      # Softer blue for dark theme
            'border-valid': '#4ade80',       # Bright green for dark theme
            'border-invalid': '#f87171',     # Bright red for dark theme

            # Rich component titles - matching border colors
            'border-title-active': '#5aa3f0 bold',
            'border-title-valid': '#4ade80 bold',
            'border-title-invalid': '#f87171 bold',

            # Rich validation messages
            'validation-message-valid': '#4ade80',
            'validation-message-invalid': '#f87171',
        }
        super().__init__(**{**dark_colors, **overrides})


class LightTheme(VimReadlineTheme):
    """Light theme optimized for light terminal backgrounds."""

    def __init__(self, **overrides):
        light_colors = {
            # Basic interface
            'placeholder': '#666666',  # Darker gray for light backgrounds
            'line-number': '#888888',
            'border-default': '#888888',
            'rich-status': 'bold bg:#f0f0f0 fg:#333333',

            # Rich component borders - darker colors for light backgrounds
            'border-active': '#2563eb',      # Darker blue for light theme
            'border-valid': '#16a34a',       # Darker green for light theme
            'border-invalid': '#dc2626',     # Darker red for light theme

            # Rich component titles - matching border colors
            'border-title-active': '#2563eb bold',
            'border-title-valid': '#16a34a bold',
            'border-title-invalid': '#dc2626 bold',

            # Rich validation messages
            'validation-message-valid': '#16a34a',
            'validation-message-invalid': '#dc2626',
        }
        super().__init__(**{**light_colors, **overrides})


class MinimalTheme(VimReadlineTheme):
    """Minimal theme with subtle colors."""

    def __init__(self, **overrides):
        minimal_colors = {
            # Basic interface - subtle grays
            'placeholder': '#777777',
            'line-number': '#555555',
            'border-default': '#444444',

            # Rich component borders - subtle, muted colors
            'border-active': '#6b7280',      # Muted gray-blue
            'border-valid': '#6b7280',       # Same muted tone for valid
            'border-invalid': '#9ca3af',     # Slightly lighter for invalid

            # Rich component titles - consistent muted styling
            'border-title-active': '#6b7280',
            'border-title-valid': '#6b7280',
            'border-title-invalid': '#9ca3af',

            # Rich validation messages - very subtle
            'validation-message-valid': '#6b7280',
            'validation-message-invalid': '#9ca3af',
        }
        super().__init__(**{**minimal_colors, **overrides})


class HighContrastTheme(VimReadlineTheme):
    """High contrast theme for accessibility."""

    def __init__(self, **overrides):
        high_contrast_colors = {
            # Basic interface - high contrast
            'placeholder': '#cccccc',
            'line-number': '#ffffff',
            'border-default': '#ffffff',

            # Rich component borders - maximum contrast colors
            'border-active': '#00ffff',      # Cyan for active
            'border-valid': '#00ff00',       # Pure green for valid
            'border-invalid': '#ff0000',     # Pure red for invalid

            # Rich component titles - high contrast
            'border-title-active': '#00ffff bold',
            'border-title-valid': '#00ff00 bold',
            'border-title-invalid': '#ff0000 bold',

            # Rich validation messages - high contrast
            'validation-message-valid': '#00ff00 bold',
            'validation-message-invalid': '#ff0000 bold',
        }
        super().__init__(**{**high_contrast_colors, **overrides})


class NeonTheme(VimReadlineTheme):
    """Neon theme with vibrant colors."""

    def __init__(self, **overrides):
        neon_colors = {
            # Basic interface - neon styling
            'placeholder': '#ff00ff italic',  # Magenta placeholder
            'line-number': '#00ffff',
            'border-default': '#ff00ff',

            # Rich component borders - neon colors
            'border-active': '#00ffff',      # Neon cyan
            'border-valid': '#39ff14',       # Neon green
            'border-invalid': '#ff073a',     # Neon red

            # Rich component titles - neon bold
            'border-title-active': '#00ffff bold',
            'border-title-valid': '#39ff14 bold',
            'border-title-invalid': '#ff073a bold',

            # Rich validation messages - neon
            'validation-message-valid': '#39ff14 bold',
            'validation-message-invalid': '#ff073a bold',
        }
        super().__init__(**{**neon_colors, **overrides})


# Default theme instance
DEFAULT_THEME = DarkTheme()


def get_default_theme() -> VimReadlineTheme:
    """Get the default theme for vim readline components."""
    return DEFAULT_THEME


def create_custom_theme(**colors) -> VimReadlineTheme:
    """
    Create a custom theme with specific color overrides.

    Args:
        **colors: Color definitions (e.g., placeholder='cyan', prompt='yellow bold')

    Returns:
        VimReadlineTheme instance with custom colors

    Example:
        theme = create_custom_theme(
            placeholder='cyan italic',
            prompt='yellow bold',
            validation_error='magenta bold'
        )
    """
    return VimReadlineTheme(**colors)