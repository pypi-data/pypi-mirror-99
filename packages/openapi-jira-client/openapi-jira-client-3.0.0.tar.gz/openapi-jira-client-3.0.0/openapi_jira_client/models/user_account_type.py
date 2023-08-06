from enum import Enum


class UserAccountType(str, Enum):
    ATLASSIAN = "atlassian"
    APP = "app"
    CUSTOMER = "customer"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
