from enum import Enum


class ProjectInputBeanAssigneeType(str, Enum):
    PROJECT_LEAD = "PROJECT_LEAD"
    UNASSIGNED = "UNASSIGNED"

    def __str__(self) -> str:
        return str(self.value)
