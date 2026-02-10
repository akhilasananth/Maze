from enum import Enum
from typing import Self, TypeAlias
from enums.direction_enums import QuadDirection


# class CellType(Enum):
#     BORDER = "Border"
#     ALL = "All"

class CellShape(Enum):
    QUAD = {
        "walls": {d: True for d in QuadDirection},
        "directions": QuadDirection,
    }