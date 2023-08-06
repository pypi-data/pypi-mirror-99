from enum import Enum


class FieldReferenceDataAuto(str, Enum):
    TRUE = "true"
    FALSE = "false"

    def __str__(self) -> str:
        return str(self.value)
