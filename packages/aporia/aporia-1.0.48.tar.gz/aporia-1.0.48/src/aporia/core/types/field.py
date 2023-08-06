from datetime import datetime
from enum import Enum
from typing import Union

FieldValue = Union[float, int, str, bool, datetime]


class FieldType(Enum):
    """Field types."""

    NUMERIC = "numeric"
    CATEGORICAL = "categorical"
    STRING = "string"
    BOOLEAN = "boolean"
    DATETIME = "datetime"


class FieldCategory(Enum):
    """Field categories."""

    FEATURES = "features"
    PREDICTIONS = "predictions"
    METRICS = "metrics"
    RAW_INPUTS = "raw_inputs"

    @staticmethod
    def from_camel_case(value: str) -> "FieldCategory":
        """Builds a field cateogry from a camelCase string.

        Args:
            value (str): Category value

        Returns:
            FieldCategory: Category that matches the given value
        """
        if value == "rawInputs":
            return FieldCategory.RAW_INPUTS

        return FieldCategory(value)
