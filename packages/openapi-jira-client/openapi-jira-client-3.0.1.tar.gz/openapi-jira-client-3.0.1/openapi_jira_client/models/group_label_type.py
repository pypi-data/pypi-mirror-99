from enum import Enum


class GroupLabelType(str, Enum):
    ADMIN = "ADMIN"
    SINGLE = "SINGLE"
    MULTIPLE = "MULTIPLE"

    def __str__(self) -> str:
        return str(self.value)
