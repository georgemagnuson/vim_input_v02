# Tests

This directory contains all test files for the vim-readline library and Rich integration experiments.

## Test Categories

### Basic Functionality Tests
- `test_basic.py` - Basic vim-readline functionality
- `test_install.py` - Installation and import tests

### Box Rendering Tests
- `test_box_alignment.py` - Box border alignment validation
- `test_box_structure.py` - Box structure and dimensions
- `test_complete_box_visual.py` - Complete box visual validation
- `test_full_box_validation.py` - Full box rendering validation

### Vim Mode Tests
- `test_mode_indicator.py` - Vim mode display testing
- `test_normal_mode_fix.py` - Normal mode functionality fixes
- `test_normal_mode_visible.py` - Normal mode visibility validation

### Rich Integration Tests
- `test_rich_integration.py` - Rich library integration
- `test_rich_interactive.py` - Rich interactive functionality
- `test_rich_native_box.py` - Rich native box rendering
- `test_simple_rich_quick.py` - Quick Rich integration tests

### Constraint Tests
- `test_constrained_box.py` - Box constraint functionality
- `test_constrained_simple.py` - Simple constraint validation

### Specialized Tests
- `test_true_box.py` - True box boundary testing

## Running Tests

Run individual tests:
```bash
python tests/test_basic.py
python tests/test_rich_integration.py
```

Or run all tests from the root directory:
```bash
for test in tests/test_*.py; do python "$test"; done
```

These tests document the evolution and validation of the vim-rich integration solution.