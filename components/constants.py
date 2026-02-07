from enum import Enum
from typing import Self

CELL_WIDTH = 3 # make sure this is an odd number to accommodate a char in the middle
CELL_HEIGHT = 1
HORIZONTAL_CHAR = "-"
VERTICAL_CHAR = "│"
IN_BETWEEN_CELLS_CHAR = "+"

class Direction(Enum):
    # (row, column)
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def get_opposite(self) -> Self | None:
        if self == Direction.NORTH:
            return Direction.SOUTH
        elif self == Direction.SOUTH:
            return Direction.NORTH
        elif self == Direction.EAST:
            return Direction.WEST
        elif self == Direction.WEST:
            return Direction.EAST
        return None

def build_cell_line(is_left: bool | None,
                    is_middle: bool | None,
                    is_right: bool | None,
                    cell_content_char: str | None = None):

    def side_segment(exists: bool | None) -> str:
        if exists is None:
            return IN_BETWEEN_CELLS_CHAR
        return VERTICAL_CHAR if exists else " "

    if is_middle is None:
        middle = (cell_content_char or " ").center(CELL_WIDTH)
    else:
        middle = (HORIZONTAL_CHAR if is_middle else " ") * CELL_WIDTH

    return side_segment(is_left) + middle + side_segment(is_right)


