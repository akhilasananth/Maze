from components.cell import Cell
from constants import (
    CELL_HEIGHT,
)
from enums.direction_enums import QuadDirection


class QuadCell(Cell):

    def __init__(self, row: int, col: int):
        super().__init__(
            pos=(row, col)
        )

    def __str__(self):
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
                has_content= True if i == CELL_HEIGHT // 2 else False
            )
            for i in range(CELL_HEIGHT)
        ]

        # Bottom border
        bottom_line = self.build_cell_line(
            is_left=None, is_middle=self.walls[QuadDirection.SOUTH], is_right=None
        )

        return [top_line, *middle_lines, bottom_line]