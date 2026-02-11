from enum import Enum
from typing import Self

class QuadDirection(Enum):
    # (row, column)
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def __str__(self) -> str:
        return self.name.capitalize()

    def get_opposite(self) -> Self:
        return {
            self.NORTH: self.SOUTH,
            self.SOUTH: self.NORTH,
            self.EAST: self.WEST,
            self.WEST: self.EAST,
        }[self]