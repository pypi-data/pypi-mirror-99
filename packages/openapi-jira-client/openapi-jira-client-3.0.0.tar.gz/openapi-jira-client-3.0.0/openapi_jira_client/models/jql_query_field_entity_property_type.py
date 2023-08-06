from enum import Enum


class JqlQueryFieldEntityPropertyType(str, Enum):
    NUMBER = "number"
    STRING = "string"
    TEXT = "text"
    DATE = "date"
    USER = "user"

    def __str__(self) -> str:
        return str(self.value)
