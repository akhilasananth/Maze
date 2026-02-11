from constants import CELL_HEIGHT, IN_BETWEEN_CELLS_CHAR, VERTICAL_CHAR, CELL_WIDTH, HORIZONTAL_CHAR
from utils.helpers import get_cell_content
from enum import Enum

from enums.direction_enums import QuadDirection
from utils.validators import check_type

class Cell:
    def __init__(
        self,
        pos: tuple[int, int],
        content: str = " "
    ):
        self.pos: tuple[int, int] = pos
        self.content: str = get_cell_content(content)
        self.is_visited = False
        self.direction = QuadDirection
        self.walls: dict[Enum, bool] = {d: True for d in self.direction}

    def __str__(self) -> str:
        return "\n".join(self.get_cell_lines())


    def get_cell_lines(self) -> list[str]:
        """
        Get a list consisting of the 3 border-lines of a cell.
        A cell is made of 3 border-lines: top, middle and bottom.
        """

        # Top border
        top_line = self.build_cell_line(
            is_left=None, is_middle=self.walls[QuadDirection.NORTH], is_right=None
        )

        # Middle get_cell_lines
        middle_lines = [
            self.build_cell_line(
                is_left=self.walls[QuadDirection.WEST],
                is_middle=None,
                is_right=self.walls[QuadDirection.EAST],
                has_content=True if i == CELL_HEIGHT // 2 else False,
            )
            for i in range(CELL_HEIGHT)
        ]

        # Bottom border
        bottom_line = self.build_cell_line(
            is_left=None, is_middle=self.walls[QuadDirection.SOUTH], is_right=None
        )

        return [top_line, *middle_lines, bottom_line]

    def build_cell_line(
        self,
        is_left: bool | None,
        is_middle: bool | None,
        is_right: bool | None,
        has_content: bool = False,
    ) -> str:
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
            return VERTICAL_CHAR if exists else " "

        if is_middle is None:
            middle = self.content.center(CELL_WIDTH) if has_content else " "
        else:
            middle = (
                HORIZONTAL_CHAR if is_middle else " "
            ) * CELL_WIDTH  # Draw horizontal line.

        return side(is_left) + middle + side(is_right)

    def remove_wall(self, wall_direction: QuadDirection) -> None:
        check_type(wall_direction, QuadDirection)
        if wall_direction not in self.direction:
            raise ValueError(
                f"{str(wall_direction)} is an invalid wall direction"
            )
        self.walls[wall_direction] = False

    def set_cell_content(self, char: str) -> None:
        self.content = get_cell_content(char)
