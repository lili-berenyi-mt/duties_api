from enum import Enum
class AddDutyResult(Enum):
    SUCCESS = 1
    EMPTY_DESCRIPTION = 2
    DUPLICATE = 3