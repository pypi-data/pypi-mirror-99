from enum import Enum


class IssueFieldOptionConfigurationAttributesItem(str, Enum):
    NOTSELECTABLE = "notSelectable"
    DEFAULTVALUE = "defaultValue"

    def __str__(self) -> str:
        return str(self.value)
