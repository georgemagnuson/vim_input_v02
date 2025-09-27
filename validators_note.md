# Validators Architecture Decision

## Design Rationale: Single File vs. Individual Files

This document explains the architectural decision for organizing validators in the VimReadline validation system.

## Current Implementation: Single `validators.py` File

All validator classes are contained in `vim_readline/validators.py`:

- `Validator` (base class)
- `EmailValidator`
- `DateValidator`
- `IntegerValidator`
- `FloatValidator`
- `RegexValidator`
- `LengthValidator`
- `FunctionValidator`
- `CompositeValidator`

## Trade-offs Analysis

### ✅ **Advantages of Single File Approach**

1. **Simple Imports**
   ```python
   from vim_readline.validators import EmailValidator, IntegerValidator
   from vim_readline import email, integer  # Convenience functions
   ```

2. **Discoverability**
   - All validators visible in one location
   - Easy to browse available validation options
   - Single point of reference for validation capabilities

3. **Maintenance**
   - Easier to maintain consistency across validators
   - Shared patterns and conventions in one place
   - Single file to review for validator-related changes

4. **Project Scale**
   - Appropriate for current scale (~8 validator types)
   - Reduces file system complexity
   - Smaller cognitive load for contributors

5. **Cohesion**
   - All validators are tightly related
   - Often used together (composite validation)
   - Share common patterns and base functionality

### ❌ **Disadvantages of Single File Approach**

1. **File Growth**
   - Could become large with many validators
   - All validators loaded even if only using one

2. **Extensibility**
   - Harder for third-party validator extensions
   - Less modular for plugin architectures

## Alternative: Individual Files Per Validator

### Structure
```
vim_readline/
├── validators/
│   ├── __init__.py      # Exports all validators
│   ├── base.py          # Validator base class
│   ├── email.py         # EmailValidator
│   ├── date.py          # DateValidator
│   ├── numeric.py       # IntegerValidator, FloatValidator
│   ├── regex.py         # RegexValidator
│   ├── length.py        # LengthValidator
│   └── composite.py     # CompositeValidator
```

### ✅ **Advantages of Individual Files**

1. **Lazy Loading**
   - Only import validators actually used
   - Smaller memory footprint for simple use cases

2. **Extensibility**
   - Easier third-party validator plugins
   - Clear extension points

3. **Separation of Concerns**
   - Each validator fully isolated
   - Independent testing and development

### ❌ **Disadvantages of Individual Files**

1. **Import Complexity**
   ```python
   from vim_readline.validators.email import EmailValidator
   from vim_readline.validators.numeric import IntegerValidator
   ```

2. **Navigation Overhead**
   - More files to browse
   - Harder to get overview of available validators

3. **Potential Circular Imports**
   - Especially with composite validators

## Decision: Single File Approach

For VimReadline's validation system, the **single file approach is optimal** because:

### Current Context
- **Scale**: ~8 validator types (manageable in one file)
- **Usage Pattern**: Validators often used together
- **Project Focus**: Vim readline library, not validation framework
- **User Base**: Developers wanting simple, clean validation

### Future Considerations
**When to reconsider and split into individual files:**

1. **Scale Threshold**: 15+ validator types
2. **Complexity**: Individual validators exceed 100+ lines
3. **Domain Specificity**: Validators become specialized (web, finance, etc.)
4. **Plugin Ecosystem**: Third-party validator extensions needed
5. **Performance**: Lazy loading becomes critical

## Implementation Notes

The current design maintains flexibility:

```python
# Base class is extensible
class CustomValidator(Validator):
    def validate(self, text: str) -> ValidationResult:
        # Custom logic here
        pass

# Composite validators support mixing
validator = combine(
    email(),
    length(min_length=5),
    custom(my_custom_check)
)
```

## Conclusion

The single-file approach balances simplicity, maintainability, and functionality for VimReadline's current and anticipated future needs. This decision can be revisited if the validation system grows significantly or usage patterns change.

---
*Decision made: 2025-09-27*
*Review date: When validator count reaches 15 or individual files exceed 200 lines*