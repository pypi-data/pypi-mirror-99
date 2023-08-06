from enum import Enum


class WorkflowCompoundConditionOperator(str, Enum):
    AND_ = "AND"
    OR_ = "OR"

    def __str__(self) -> str:
        return str(self.value)
