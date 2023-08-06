from enum import Enum


class IssueTypeCreateBeanType(str, Enum):
    SUBTASK = "subtask"
    STANDARD = "standard"

    def __str__(self) -> str:
        return str(self.value)
