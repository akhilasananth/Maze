from abc import ABC
from enum import Enum

from enums.direction_enums import DirectionType, QuadDirection
from utils.validators import check_type

class CellShape(ABC):
    def __init__(self, name: str, directions: DirectionType):
        self.name: str = name
        self.directions: DirectionType = directions
        self.walls: dict[DirectionType, bool] = self._get_directions()

    def validate_wall_direction(self, wall_direction: DirectionType)-> None:
        check_type(wall_direction, DirectionType)
        if wall_direction not in self.directions:
            raise ValueError(
                f"{str(wall_direction)} is an invalid wall direction for this cell shape: {self.name}"
            )

    def _get_directions(self) -> dict[DirectionType|Enum, bool]:
        return {d: True for d in self.directions.get_directions()}

    def get_number_of_walls(self) -> int:
        return len(self.walls)

    def remove_wall(self, wall_direction: DirectionType) -> None:
        self.validate_wall_direction(wall_direction=wall_direction)
        self.walls[wall_direction] = False

    def add_wall(self, wall_direction: DirectionType) -> None:
        self.validate_wall_direction(wall_direction)
        self.walls[wall_direction] = True


class QuadCellShape(CellShape):
    def __init__(self) -> None:
        super().__init__(name="Quadratic", directions=QuadDirection)