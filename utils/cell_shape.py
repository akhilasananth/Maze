from abc import ABC
from enums.direction_enums import DirectionType, QuadDirection
from utils.validators import check_type


class CellShape(ABC):
    def __init__(self, name: str, directions: DirectionType):
        self.name: str = name
        self.directions: DirectionType = directions
        self.walls: dict[DirectionType, bool] = self._get_directions()

    def is_valid_wall(self, wall_direction: DirectionType):
        check_type(wall_direction, DirectionType)
        if wall_direction not in self.directions:
            raise ValueError(
                f"{wall_direction} is an invalid wall direction for this cell shape: {self.name}"
            )

    def _get_directions(self):
        return {d: True for d in self.directions}

    def get_number_of_walls(self):
        return len(self.walls)


class QuadCellShape(CellShape):
    def __init__(self):
        super().__init__(name="Quadratic", directions=QuadDirection)
