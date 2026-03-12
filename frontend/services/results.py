from enum import Enum
class AddDutyResult(Enum):
    SUCCESS = 1
    EMPTY_DESCRIPTION = 2
    DUPLICATE = 3
    ERROR = 4
    INVALID_INPUT = 5

class ToggleThemeResult(Enum):
    SUCCESS = 1
    UNAUTHORISED = 2