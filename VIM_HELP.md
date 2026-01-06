# VimReadline Help - Vim Mode Keybindings

VimReadline provides a vim-inspired text editing experience for single-buffer text input. This guide covers all available modes and keybindings.

## Quick Start

- **Enter Insert Mode**: Press `i`, `a`, `o`, `I`, `A`, or `O`
- **Exit to Normal Mode**: Press `Esc` or `Ctrl+[`
- **Submit/Accept Input**: Press `Enter` (Return)
- **Add New Line**: Press `Ctrl+J` or `Shift+Enter`
- **Cancel/Exit**: Press `Ctrl+C` or `Ctrl+D`

## Vim Modes

VimReadline supports the standard vim editing modes with appropriate cursor shapes:

### Normal Mode (Default)
- **Cursor**: Block cursor
- **Purpose**: Navigation and text manipulation
- **Status**: No status indicator (or "NORMAL" if using full mode display)

### Insert Mode
- **Cursor**: Beam cursor (|)
- **Purpose**: Text insertion
- **Status**: "-- INSERT --" or "I"
- **Entry**: `i`, `a`, `o`, `I`, `A`, `O`, `s`, `S`, `c` commands

### Visual Mode
- **Cursor**: Block cursor
- **Purpose**: Text selection
- **Status**: "-- VISUAL --", "-- VISUAL LINE --", or "-- VISUAL BLOCK --" (or "V")
- **Entry**: `v`, `V`, `Ctrl+V`

### Replace Mode
- **Cursor**: Underline cursor (_)
- **Purpose**: Character replacement
- **Status**: "-- REPLACE --" or "R"
- **Entry**: `R`

## Navigation Keybindings

### Basic Movement (Normal Mode)
| Key | Action |
|-----|--------|
| `h` | Move cursor left |
| `j` | Move cursor down |
| `k` | Move cursor up |
| `l` | Move cursor right |
| `←` `↓` `↑` `→` | Arrow keys (same as hjkl) |

### Word Movement
| Key | Action |
|-----|--------|
| `w` | Move to beginning of next word |
| `b` | Move to beginning of previous word |
| `e` | Move to end of current/next word |
| `W` | Move to next WORD (whitespace-separated) |
| `B` | Move to previous WORD |
| `E` | Move to end of current/next WORD |

### Line Movement
| Key | Action |
|-----|--------|
| `0` | Move to beginning of line |
| `^` | Move to first non-whitespace character |
| `$` | Move to end of line |
| `gg` | Move to first line |
| `G` | Move to last line |
| `{number}G` | Move to line number |

### Page Movement
| Key | Action |
|-----|--------|
| `Ctrl+F` | Page down |
| `Ctrl+B` | Page up |
| `Ctrl+D` | Half page down |
| `Ctrl+U` | Half page up |

## Editing Keybindings

### Insert Mode Entry
| Key | Action |
|-----|--------|
| `i` | Insert before cursor |
| `a` | Insert after cursor |
| `I` | Insert at beginning of line |
| `A` | Insert at end of line |
| `o` | Open new line below and insert |
| `O` | Open new line above and insert |
| `s` | Delete character and insert |
| `S` | Delete line and insert |

### Text Deletion
| Key | Action |
|-----|--------|
| `x` | Delete character under cursor |
| `X` | Delete character before cursor |
| `dd` | Delete entire line |
| `dw` | Delete word |
| `db` | Delete word backward |
| `d$` or `D` | Delete to end of line |
| `d0` | Delete to beginning of line |
| `dgg` | Delete to beginning of file |
| `dG` | Delete to end of file |

### Change (Delete and Insert)
| Key | Action |
|-----|--------|
| `cw` | Change word |
| `cb` | Change word backward |
| `cc` or `S` | Change entire line |
| `c$` or `C` | Change to end of line |
| `c0` | Change to beginning of line |

### Copy (Yank)
| Key | Action |
|-----|--------|
| `yy` | Yank (copy) entire line |
| `yw` | Yank word |
| `y$` | Yank to end of line |
| `y0` | Yank to beginning of line |
| `ygg` | Yank to beginning of file |
| `yG` | Yank to end of file |

### Paste
| Key | Action |
|-----|--------|
| `p` | Paste after cursor |
| `P` | Paste before cursor |

### Undo/Redo
| Key | Action |
|-----|--------|
| `u` | Undo |
| `Ctrl+R` | Redo |

## Visual Mode Keybindings

### Visual Selection
| Key | Action |
|-----|--------|
| `v` | Enter character-wise visual mode |
| `V` | Enter line-wise visual mode |
| `Ctrl+V` | Enter block-wise visual mode |
| `Esc` | Exit visual mode |

### Visual Mode Operations
| Key | Action |
|-----|--------|
| `d` | Delete selection |
| `c` | Change selection (delete and enter insert mode) |
| `y` | Yank (copy) selection |
| `>` | Indent selection |
| `<` | Unindent selection |

## Replace Mode

| Key | Action |
|-----|--------|
| `R` | Enter replace mode |
| `Esc` | Exit replace mode |
| Any character | Replace character under cursor |

## Search and Replace

| Key | Action |
|-----|--------|
| `/pattern` | Search forward for pattern |
| `?pattern` | Search backward for pattern |
| `n` | Next search match |
| `N` | Previous search match |
| `*` | Search for word under cursor (forward) |
| `#` | Search for word under cursor (backward) |

## Special Keys

### Application Control
| Key | Action |
|-----|--------|
| `Enter` | Submit/accept input and exit |
| `Ctrl+J` | Insert newline character |
| `Shift+Enter` | Insert newline character (alternative) |
| `Ctrl+C` | Cancel and exit |
| `Ctrl+D` | Cancel and exit |

### Insert Mode Special Keys
| Key | Action |
|-----|--------|
| `Esc` | Exit to normal mode |
| `Ctrl+[` | Exit to normal mode (alternative) |
| `Backspace` | Delete character before cursor |
| `Delete` | Delete character under cursor |
| `Ctrl+H` | Delete character before cursor |
| `Ctrl+W` | Delete word before cursor |

## Text Objects

Text objects can be used with `d`, `c`, `y` commands:

| Key | Action |
|-----|--------|
| `iw` | Inner word |
| `aw` | A word (including surrounding space) |
| `is` | Inner sentence |
| `as` | A sentence |
| `ip` | Inner paragraph |
| `ap` | A paragraph |
| `i"` | Inside double quotes |
| `a"` | Around double quotes |
| `i'` | Inside single quotes |
| `a'` | Around single quotes |
| `i(` or `i)` | Inside parentheses |
| `a(` or `a)` | Around parentheses |
| `i[` or `i]` | Inside brackets |
| `a[` or `a]` | Around brackets |
| `i{` or `i}` | Inside braces |
| `a{` or `a}` | Around braces |

## Repeat Commands

| Key | Action |
|-----|--------|
| `.` | Repeat last change |
| `{number}` | Repeat next command number times |

Examples:
- `3dd` - Delete 3 lines
- `5w` - Move 5 words forward
- `10x` - Delete 10 characters

## Marks and Jumps

| Key | Action |
|-----|--------|
| `m{a-z}` | Set mark |
| `'{a-z}` | Jump to mark (line) |
| `` `{a-z} `` | Jump to mark (exact position) |
| `''` | Jump to previous position (line) |
| ``` `` ``` | Jump to previous position (exact) |

## Configuration Options

VimReadline supports several configuration options:

- **Line Numbers**: Enable with `show_line_numbers=True`
- **Status Bar**: Show mode indicator with `show_status=True`
- **Line Wrapping**: Control with `wrap_lines=True/False`
- **Custom Submit Key**: Change with `submit_key` parameter
- **Custom Newline Key**: Change with `newline_key` parameter
- **Custom Cancel Keys**: Change with `cancel_keys` parameter

## Validation Features (ValidatedVimReadline)

When using validation, additional behavior applies:

- **Border Colors**: Blue (active), Green (valid), Red (invalid)
- **Validation Messages**: Displayed in bottom border
- **Submit Validation**: Invalid input prevents submission
- **Hidden Input**: Password masking with configurable characters

## Tips for New Users

1. **Start Simple**: Begin with `i` to insert, `Esc` to exit to normal mode
2. **Practice Navigation**: Use `hjkl` instead of arrow keys for efficiency
3. **Learn Word Movement**: `w`, `b`, `e` are much faster than character movement
4. **Use Text Objects**: Commands like `dw` (delete word) are more efficient than `x` repeatedly
5. **Leverage Visual Mode**: Select text first, then perform operations
6. **Remember Undo**: `u` can undo any changes
7. **Use Repetition**: Number prefixes like `3dd` can speed up operations

## Common Command Combinations

- `ciw` - Change inner word (delete word and enter insert mode)
- `di"` - Delete text inside quotes
- `yi(` - Yank text inside parentheses
- `>ip` - Indent paragraph
- `dap` - Delete a paragraph
- `ggVG` - Select entire buffer
- `:%s/old/new/g` - Replace all occurrences (if search/replace is implemented)

## Getting Help

- This document covers the standard vim keybindings available in VimReadline
- For application-specific features, refer to your application's documentation
- Practice in a safe environment to build muscle memory
- Consider using a vim tutorial or cheat sheet for additional practice

---

*This help is for VimReadline - a vim-mode implementation for text input based on prompt-toolkit.*