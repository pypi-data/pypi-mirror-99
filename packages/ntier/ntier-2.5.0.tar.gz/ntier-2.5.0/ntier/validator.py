"""Validator and Validations."""
import inspect
import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import (Any, Awaitable, Callable, List, Mapping, MutableMapping,
                    Optional, Sequence, Set, Type, Union, cast)

from .validation_result import ValidationResult

Record = Mapping[str, Any]
MutableRecord = MutableMapping[str, Any]
ValidateFieldSync = Callable[[Any], bool]
ValidateFieldAsync = Callable[[Any], Awaitable[bool]]
ValidateField = Union[ValidateFieldSync, ValidateFieldAsync]
ValidateRecordSync = Callable[[Record], bool]
ValidateRecordAsync = Callable[[Record], Awaitable[bool]]
ValidateRecord = Union[ValidateRecordSync, ValidateRecordAsync]

NUMBER_TYPES = (int, float, Decimal)
Number = Union[int, float, Decimal]


@dataclass
class FieldValidator:
    """Information to validate a single field."""

    prop_name: str
    message: str
    validator: ValidateField
    field_name: Optional[str] = None

    async def validate(self, value: Any) -> bool:
        """Properly calls the validator."""
        if inspect.iscoroutinefunction(self.validator):
            return await cast(ValidateFieldAsync, self.validator)(value)
        return cast(ValidateFieldSync, self.validator)(value)

    @property
    def output_name(self) -> str:
        return self.field_name if self.field_name else self.prop_name


@dataclass
class RecordValidator:
    """Information to validate a whole record."""

    message: str
    validator: ValidateRecord
    output_name: Optional[str]

    async def validate(self, record: Record) -> bool:
        """Properly calls the validator."""
        if inspect.iscoroutinefunction(self.validator):
            return await cast(ValidateRecordAsync, self.validator)(record)
        return cast(ValidateRecordSync, self.validator)(record)


ValidatorType = Union[FieldValidator, RecordValidator]


class Validator:
    """Records validators for a record."""

    def __init__(self, validators: Optional[List[ValidatorType]] = None):
        self.validators: List[ValidatorType] = validators or []

    @staticmethod
    def field(
        prop_name: str,
        message: str,
        validate: ValidateField,
        field_name: Optional[str] = None,
    ) -> FieldValidator:
        """Helper to create a FieldValidator."""
        return FieldValidator(prop_name, message, validate, field_name)

    @staticmethod
    def record(
        message: str, validate: ValidateRecord, output_name: str = None
    ) -> RecordValidator:
        return RecordValidator(message, validate, output_name)

    async def validate(
        self, record: Optional[Record], *, fail_fast: bool = False
    ) -> ValidationResult:
        """Validate data."""
        if record is None:
            return ValidationResult().add_general_message("no data")
        return await ValidatorInstance(self, record).validate(fail_fast)


class ValidatorInstance:
    """Holds results for a run of validation."""

    def __init__(self, validator: Validator, record: Record) -> None:
        self.validator = validator
        self.record = record
        self.validation_result = ValidationResult()

    async def validate(self, fail_fast: bool) -> ValidationResult:
        """Executes all validators against the record.

        When a validation fails further validations against the entire record, or against the field
        that failed, will not be run.
        """
        for validator in self.validator.validators:
            if isinstance(validator, FieldValidator):
                # Do not run validation on fields that have already failed
                if self.validation_result.has_failed_for(validator.output_name):
                    continue
                await self.validate_field(validator)
            elif isinstance(validator, RecordValidator):
                # Do not run record validators if any validations have already failed
                if self.validation_result:
                    await self.validate_record(validator)
            else:
                raise Exception("Invalid validator")

            if fail_fast and not self.validation_result:
                return self.validation_result

        return self.validation_result

    async def validate_field(self, validator: FieldValidator) -> None:
        """Validate a single field."""
        value = self.record.get(validator.prop_name, None)
        result = await validator.validate(value)

        if not result:
            self.validation_result.add_message(validator.output_name, validator.message)

    async def validate_record(self, validator: RecordValidator) -> None:
        """Validate an entire record."""
        result = await validator.validate(self.record)

        if not result:
            if validator.output_name:
                self.validation_result.add_message(
                    validator.output_name, validator.message
                )
            else:
                self.validation_result.add_general_message(validator.message)


class Validators:
    """Contains validator methods."""

    @staticmethod
    def is_present(val: Any) -> bool:
        """Validate that a value is not None"""
        if val is None:
            return False
        return True

    @staticmethod
    def optional(validator: ValidateFieldSync) -> ValidateFieldSync:
        """Makes a validator ignore None values"""

        def checker(val: Any) -> bool:
            if val is None:
                return True
            return validator(val)

        return checker

    @staticmethod
    def any(validators: List[ValidateFieldSync]) -> ValidateFieldSync:
        """Validates a value matches at least one validator."""

        def checker(val: Any) -> bool:
            for validator in validators:
                if validator(val):
                    return True
            return False

        return checker

    @staticmethod
    def is_type(typ: Type) -> ValidateFieldSync:
        """Validates that a value is of a type."""

        def checker(val: Any) -> bool:
            return isinstance(val, typ)

        return checker

    @staticmethod
    def is_member(members: Union[Sequence, Set]) -> ValidateFieldSync:
        """Validates that a value is a member of a sequence."""

        def checker(val: Any) -> bool:
            return val in members

        return checker

    @staticmethod
    def is_not_empty(val: Any) -> bool:
        """Validates that a collection is not empty."""

        if isinstance(val, (str, list, tuple, set, dict)):
            return len(val) != 0
        return False

    @staticmethod
    def is_match(pattern: str) -> ValidateFieldSync:
        """Validates that a value matches a regular expression"""

        def checker(val: Any) -> bool:
            if not isinstance(val, str):
                return False
            return bool(re.match(pattern, val))

        return checker

    @staticmethod
    def equals(value: Any) -> ValidateFieldSync:
        """Checks that a value exactly equals another"""

        def checker(val: Any) -> bool:
            return val == value

        return checker

    @staticmethod
    def is_length(min_len: Optional[int], max_len: Optional[int]) -> ValidateFieldSync:
        """Validates that a string value is within certain length bounds"""

        def checker(val: Any) -> bool:
            if not isinstance(val, str):
                return False
            if min_len is not None and len(val) < min_len:
                return False
            if max_len is not None and max_len < len(val):
                return False
            return True

        return checker

    @staticmethod
    def is_greater(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val > bound

        return checker

    @staticmethod
    def is_lesser(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val < bound

        return checker

    @staticmethod
    def is_greater_or_equal(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val >= bound

        return checker

    @staticmethod
    def is_lesser_or_equal(bound: Number) -> ValidateFieldSync:
        """Validates that a number is greater than a bound."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return val <= bound

        return checker

    @staticmethod
    def is_between(lbound: Number, ubound: Number) -> ValidateFieldSync:
        """Validates that a number is between two other numbers, inclusive."""

        def checker(val: Any) -> bool:
            if not isinstance(val, NUMBER_TYPES):
                return False
            return lbound <= val <= ubound

        return checker

    @staticmethod
    def has_timezone(val: Any) -> bool:
        """Checks that a value is a datetime and has a timezone (is not naive)"""

        if not isinstance(val, datetime):
            return False
        return bool(val.tzinfo)
