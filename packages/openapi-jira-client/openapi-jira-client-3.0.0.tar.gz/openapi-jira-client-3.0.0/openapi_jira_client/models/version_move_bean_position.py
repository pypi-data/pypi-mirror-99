from enum import Enum


class VersionMoveBeanPosition(str, Enum):
    EARLIER = "Earlier"
    LATER = "Later"
    FIRST = "First"
    LAST = "Last"

    def __str__(self) -> str:
        return str(self.value)
