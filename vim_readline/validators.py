"""
Validation system for VimReadline input.

Provides a set of built-in validators and a framework for custom validation.
"""
import re
import datetime
from typing import Callable, Optional, Union, Any
from abc import ABC, abstractmethod


class ValidationResult:
    """Result of a validation check."""

    def __init__(self, is_valid: bool, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message

    def __bool__(self):
        return self.is_valid


class Validator(ABC):
    """Base class for all validators."""

    @abstractmethod
    def validate(self, text: str) -> ValidationResult:
        """Validate the given text."""
        pass

    @property
    def allow_empty(self) -> bool:
        """Whether empty input is considered valid."""
        return True


class EmailValidator(Validator):
    """Validates email addresses."""

    def __init__(self, allow_empty: bool = True):
        self._allow_empty = allow_empty
        # Basic email regex - can be made more sophisticated
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip():
            if self.allow_empty:
                return ValidationResult(True)
            else:
                return ValidationResult(False, "Email address is required")

        if self.email_pattern.match(text.strip()):
            return ValidationResult(True)
        else:
            return ValidationResult(False, "Invalid email format")


class DateValidator(Validator):
    """Validates dates in various formats."""

    def __init__(self, date_format: str = "%Y-%m-%d", allow_empty: bool = True):
        self.date_format = date_format
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip():
            if self.allow_empty:
                return ValidationResult(True)
            else:
                return ValidationResult(False, "Date is required")

        try:
            datetime.datetime.strptime(text.strip(), self.date_format)
            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, f"Invalid date format. Expected: {self.date_format}")


class IntegerValidator(Validator):
    """Validates integer input with optional min/max bounds."""

    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None,
                 allow_empty: bool = True):
        self.min_value = min_value
        self.max_value = max_value
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip():
            if self.allow_empty:
                return ValidationResult(True)
            else:
                return ValidationResult(False, "Integer value is required")

        try:
            value = int(text.strip())

            if self.min_value is not None and value < self.min_value:
                return ValidationResult(False, f"Value must be at least {self.min_value}")

            if self.max_value is not None and value > self.max_value:
                return ValidationResult(False, f"Value must be at most {self.max_value}")

            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, "Invalid integer format")


class FloatValidator(Validator):
    """Validates float input with optional min/max bounds."""

    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None,
                 allow_empty: bool = True):
        self.min_value = min_value
        self.max_value = max_value
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip():
            if self.allow_empty:
                return ValidationResult(True)
            else:
                return ValidationResult(False, "Number is required")

        try:
            value = float(text.strip())

            if self.min_value is not None and value < self.min_value:
                return ValidationResult(False, f"Value must be at least {self.min_value}")

            if self.max_value is not None and value > self.max_value:
                return ValidationResult(False, f"Value must be at most {self.max_value}")

            return ValidationResult(True)
        except ValueError:
            return ValidationResult(False, "Invalid number format")


class RegexValidator(Validator):
    """Validates input against a regular expression pattern."""

    def __init__(self, pattern: Union[str, re.Pattern], error_message: str = "Invalid format",
                 allow_empty: bool = True):
        if isinstance(pattern, str):
            self.pattern = re.compile(pattern)
        else:
            self.pattern = pattern
        self.error_message = error_message
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip():
            if self.allow_empty:
                return ValidationResult(True)
            else:
                return ValidationResult(False, "Input is required")

        if self.pattern.match(text):
            return ValidationResult(True)
        else:
            return ValidationResult(False, self.error_message)


class LengthValidator(Validator):
    """Validates input length."""

    def __init__(self, min_length: Optional[int] = None, max_length: Optional[int] = None,
                 allow_empty: bool = True):
        self.min_length = min_length
        self.max_length = max_length
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text and self.allow_empty:
            return ValidationResult(True)

        length = len(text)

        if self.min_length is not None and length < self.min_length:
            if self.min_length == 1:
                return ValidationResult(False, "Input is required")
            else:
                return ValidationResult(False, f"Must be at least {self.min_length} characters")

        if self.max_length is not None and length > self.max_length:
            return ValidationResult(False, f"Must be at most {self.max_length} characters")

        return ValidationResult(True)


class FunctionValidator(Validator):
    """Validates input using a custom function."""

    def __init__(self, validator_func: Callable[[str], Union[bool, ValidationResult, tuple]],
                 allow_empty: bool = True):
        """
        Args:
            validator_func: Function that takes text and returns:
                - bool: True for valid, False for invalid
                - ValidationResult: Complete validation result
                - tuple: (is_valid, error_message)
        """
        self.validator_func = validator_func
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        if not text.strip() and self.allow_empty:
            return ValidationResult(True)

        result = self.validator_func(text)

        if isinstance(result, ValidationResult):
            return result
        elif isinstance(result, bool):
            return ValidationResult(result, "Invalid input" if not result else "")
        elif isinstance(result, tuple) and len(result) == 2:
            return ValidationResult(result[0], result[1])
        else:
            raise ValueError("Validator function must return bool, ValidationResult, or (bool, str) tuple")


class CompositeValidator(Validator):
    """Combines multiple validators with AND logic."""

    def __init__(self, validators: list[Validator], allow_empty: bool = True):
        self.validators = validators
        self._allow_empty = allow_empty

    @property
    def allow_empty(self) -> bool:
        return self._allow_empty

    def validate(self, text: str) -> ValidationResult:
        # If text is empty, check if all validators allow empty
        if not text.strip():
            if self.allow_empty and all(v.allow_empty for v in self.validators):
                return ValidationResult(True)
            # If any validator doesn't allow empty, run validation to get proper error

        for validator in self.validators:
            result = validator.validate(text)
            if not result.is_valid:
                return result

        return ValidationResult(True)


# Convenience functions for common validators
def email(allow_empty: bool = True) -> EmailValidator:
    """Create an email validator."""
    return EmailValidator(allow_empty=allow_empty)


def date(date_format: str = "%Y-%m-%d", allow_empty: bool = True) -> DateValidator:
    """Create a date validator."""
    return DateValidator(date_format=date_format, allow_empty=allow_empty)


def integer(min_value: Optional[int] = None, max_value: Optional[int] = None,
            allow_empty: bool = True) -> IntegerValidator:
    """Create an integer validator."""
    return IntegerValidator(min_value=min_value, max_value=max_value, allow_empty=allow_empty)


def float_num(min_value: Optional[float] = None, max_value: Optional[float] = None,
              allow_empty: bool = True) -> FloatValidator:
    """Create a float validator."""
    return FloatValidator(min_value=min_value, max_value=max_value, allow_empty=allow_empty)


def regex(pattern: Union[str, re.Pattern], error_message: str = "Invalid format",
          allow_empty: bool = True) -> RegexValidator:
    """Create a regex validator."""
    return RegexValidator(pattern=pattern, error_message=error_message, allow_empty=allow_empty)


def length(min_length: Optional[int] = None, max_length: Optional[int] = None,
           allow_empty: bool = True) -> LengthValidator:
    """Create a length validator."""
    return LengthValidator(min_length=min_length, max_length=max_length, allow_empty=allow_empty)


def custom(validator_func: Callable, allow_empty: bool = True) -> FunctionValidator:
    """Create a custom function validator."""
    return FunctionValidator(validator_func=validator_func, allow_empty=allow_empty)


def combine(*validators: Validator, allow_empty: bool = True) -> CompositeValidator:
    """Combine multiple validators with AND logic."""
    return CompositeValidator(list(validators), allow_empty=allow_empty)