from enum import Enum


class GlobalScopeBeanAttributesItem(str, Enum):
    NOTSELECTABLE = "notSelectable"
    DEFAULTVALUE = "defaultValue"

    def __str__(self) -> str:
        return str(self.value)
