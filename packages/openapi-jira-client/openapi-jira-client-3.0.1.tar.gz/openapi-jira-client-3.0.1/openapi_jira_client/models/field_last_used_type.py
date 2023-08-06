from enum import Enum


class FieldLastUsedType(str, Enum):
    TRACKED = "TRACKED"
    NOT_TRACKED = "NOT_TRACKED"
    NO_INFORMATION = "NO_INFORMATION"

    def __str__(self) -> str:
        return str(self.value)
