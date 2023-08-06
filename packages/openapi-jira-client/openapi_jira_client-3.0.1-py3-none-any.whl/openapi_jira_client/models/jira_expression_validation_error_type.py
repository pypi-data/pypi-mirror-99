from enum import Enum


class JiraExpressionValidationErrorType(str, Enum):
    SYNTAX = "syntax"
    TYPE = "type"
    OTHER = "other"

    def __str__(self) -> str:
        return str(self.value)
