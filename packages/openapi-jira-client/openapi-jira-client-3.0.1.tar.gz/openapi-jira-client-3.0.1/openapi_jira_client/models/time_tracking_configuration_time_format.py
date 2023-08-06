from enum import Enum


class TimeTrackingConfigurationTimeFormat(str, Enum):
    PRETTY = "pretty"
    DAYS = "days"
    HOURS = "hours"

    def __str__(self) -> str:
        return str(self.value)
