from enum import Enum


class HierarchyLevelGlobalHierarchyLevel(str, Enum):
    SUBTASK = "SUBTASK"
    BASE = "BASE"
    EPIC = "EPIC"

    def __str__(self) -> str:
        return str(self.value)
