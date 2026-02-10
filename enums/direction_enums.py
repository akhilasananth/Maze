from abc import ABC, abstractmethod
from enum import Enum
from typing import Self, Protocol

from typing import runtime_checkable

@runtime_checkable
class DirectionType(Protocol):
    value: tuple[int, int]
    def get_opposite(self) -> Self: ...

class QuadDirection(Enum):
    # (row, column)
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    EAST = (0, 1)
    WEST = (0, -1)

    def get_opposite(self) -> Self | None:
        return {
            self.NORTH: self.SOUTH,
            self.SOUTH: self.NORTH,
            self.EAST: self.WEST,
            self.WEST: self.EAST,
        }[self]

class TriangleDirection(Enum): # For test purposes for now
    # (row, column)
    NORTH_EAST = (-1, 1)
    SOUTH = (1, 0)
    NORTH_WEST = (0, -1)

    def get_opposite(self) -> Self | None:
        return {
            self.NORTH_EAST: self.NORTH_WEST,
            self.NORTH_WEST: self.NORTH_EAST,
        }[self]