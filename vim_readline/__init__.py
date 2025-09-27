"""
VimReadline - A vim-mode readline implementation for single-buffer text editing.

Based on prompt-toolkit, provides full vim navigation modes (normal/insert/visual)
without file I/O operations. Perfect for interactive applications that need
vim-style text input.
"""

from .core import VimReadline, vim_input

# Validated vim readline with input validation
from .validated import ValidatedVimReadline, validated_vim_input
from .validators import (
    Validator, ValidationResult,
    EmailValidator, DateValidator, IntegerValidator, FloatValidator,
    RegexValidator, LengthValidator, FunctionValidator, CompositeValidator,
    email, date, integer, float_num, regex, length, custom, combine
)

# Box-constrained version
from .constrained import BoxConstrainedVimReadline, box_constrained_vim_input

# Full box version (complete borders like screenshot)
from .full_box import FullBoxVimReadline, full_box_vim_input

# Rich-enhanced version (optional)
try:
    from .rich_enhanced import RichVimReadline, rich_vim_input
    _rich_available = True
except ImportError:
    RichVimReadline = None
    rich_vim_input = None
    _rich_available = False

# Rich-native box version (uses Rich's built-in box routines)
try:
    from .rich_box_native import RichBoxVimReadline, rich_box_vim_input
    _rich_box_available = True
except ImportError:
    RichBoxVimReadline = None
    rich_box_vim_input = None
    _rich_box_available = False

__version__ = "0.1.0"
__author__ = "Generated with Claude Code"
__email__ = "noreply@anthropic.com"

__all__ = [
    "VimReadline",
    "vim_input",
    "ValidatedVimReadline",
    "validated_vim_input",
    "Validator",
    "ValidationResult",
    "EmailValidator",
    "DateValidator",
    "IntegerValidator",
    "FloatValidator",
    "RegexValidator",
    "LengthValidator",
    "FunctionValidator",
    "CompositeValidator",
    "email",
    "date",
    "integer",
    "float_num",
    "regex",
    "length",
    "custom",
    "combine",
    "BoxConstrainedVimReadline",
    "box_constrained_vim_input",
    "FullBoxVimReadline",
    "full_box_vim_input",
    "__version__"
]

# Add Rich exports if available
if _rich_available:
    __all__.extend([
        "RichVimReadline",
        "rich_vim_input"
    ])

# Add Rich-native box exports if available
if _rich_box_available:
    __all__.extend([
        "RichBoxVimReadline",
        "rich_box_vim_input"
    ])

# Rich interactive app version (full Rich integration)
try:
    from .rich_prompt_integration import RichPromptIntegration, rich_vim_input, RichVimWorkspace
    _rich_interactive_available = True
except ImportError:
    RichPromptIntegration = None
    rich_vim_input = None
    RichVimWorkspace = None
    _rich_interactive_available = False

# Add Rich interactive exports if available
if _rich_interactive_available:
    __all__.extend([
        "RichPromptIntegration",
        "rich_vim_input",
        "RichVimWorkspace"
    ])