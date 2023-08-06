from enum import Enum


class MoveFieldBeanPosition(str, Enum):
    EARLIER = "Earlier"
    LATER = "Later"
    FIRST = "First"
    LAST = "Last"

    def __str__(self) -> str:
        return str(self.value)
