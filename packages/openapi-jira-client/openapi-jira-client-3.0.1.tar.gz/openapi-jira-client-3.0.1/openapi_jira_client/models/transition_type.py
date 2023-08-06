from enum import Enum


class TransitionType(str, Enum):
    GLOBAL_ = "global"
    INITIAL = "initial"
    DIRECTED = "directed"

    def __str__(self) -> str:
        return str(self.value)
