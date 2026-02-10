from abc import ABC, abstractmethod

from constants import IN_BETWEEN_CELLS_CHAR, VERTICAL_CHAR, CELL_WIDTH, HORIZONTAL_CHAR
from enums.direction_enums import DirectionType
from enums.enums import CellShape
from utils.helpers import get_cell_content
from utils.validators import check_type


class Cell(ABC):
    def __init__(self,
                 pos: tuple[int, int],
                 content: str = " ",
                 shape: CellShape = CellShape.QUAD,
        ):

        self.pos: tuple[int, int] = pos

        check_type(shape, CellShape)
        self.shape: CellShape = shape

        self.walls: dict[DirectionType, bool] = self.shape.value["walls"]
        self.content: str = get_cell_content(content)
        self.is_visited = False

    @abstractmethod
    def __str__(self):
        raise NotImplementedError("Subclasses must implement __str__")

    @abstractmethod
    def get_cell_lines(self) -> list[str]:
        raise NotImplementedError("Subclasses must implement get_cell_lines")

    def get_number_of_walls(self):
        return len(self.walls)

    def set_is_visited(self, is_visited: bool) -> None:
        check_type(is_visited, bool)
        self.is_visited = is_visited

    def set_cell_content(self, char: str) -> None:
        self.content = get_cell_content(char)

    def is_valid_wall(self, wall_direction: DirectionType):
        check_type(wall_direction, DirectionType)
        if wall_direction not in self.walls:
            raise ValueError(
                f"{wall_direction} is an invalid wall direction for this cell shape: {self.shape}"
            )
    def remove_wall(self, wall_direction: DirectionType) -> None:
        self.is_valid_wall(wall_direction)
        self.walls[wall_direction] = False

    def add_wall(self, wall_direction: DirectionType) -> bool:
        self.is_valid_wall(wall_direction)
        self.walls[wall_direction] = True

        return True

    def build_cell_line( self, is_left: bool | None, is_middle: bool | None, is_right: bool | None,
                         has_content: bool = False):
        """
        A border-line in the cell is made of 3 parts: [left] + [middle] + [right].
        :param is_left: On the left: None: there is no vertical border or True: a vertical border exists
                                    or False: no vertical border.
        :param is_middle: In the middle: None: there is no horizontal border or True: a horizontal border exists
                                         or False: no horizontal border.
        :param is_right: On the right: None: there is no vertical border or True: a vertical border exists
                                    or False: no vertical border.
        :param has_content: Does the line have content or empty middle if middle is not None
        :return: Border-line that is [left] + [middle] + [right].
        """

        def side(exists: bool | None) -> str:
            """
            Helper method to get the side part of the border-line. Left and Right.
            :param exists: None: there is no vertical border or True: a vertical border exists
                                or False: no vertical border.
            """
            if exists is None:
                return IN_BETWEEN_CELLS_CHAR
            return VERTICAL_CHAR if exists else  " "

        if is_middle is None:
            middle = self.content.center(CELL_WIDTH) if has_content else " "
        else:
            middle = (HORIZONTAL_CHAR if is_middle else " ") * CELL_WIDTH  # Draw horizontal line.

        return side(is_left) + middle + side(is_right)


