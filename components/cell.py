from components.constants import Direction, CELL_HEIGHT, build_cell_line


def check_content(char: str):
    if char is not None and len(char) != 1:
        raise ValueError("Cell content must be exactly 1 character")
    else:
        return char


class Cell:

    def __init__(self, row: int, col: int, content:str|None = None):
        self.pos: tuple[int, int] = (row, col)
        self.is_visited: bool = False
        self.walls: dict[Direction, bool] = {d: True for d in Direction}
        self.content = check_content(content)


    def get_cell_lines_str(self) -> list[str]:
        # Top border
        top_line = build_cell_line(
            is_left=None,
            is_middle=self.walls[Direction.NORTH],
            is_right=None
        )

        # Middle get_cell_lines_str
        middle_lines = [
            build_cell_line(
                is_left=self.walls[Direction.WEST],
                is_middle=None,
                is_right=self.walls[Direction.EAST],
                cell_content_char=self.content if i == CELL_HEIGHT // 2 else None
            )
            for i in range(CELL_HEIGHT)
        ]

        # Bottom border
        bottom_line = build_cell_line(
            is_left=None,
            is_middle=self.walls[Direction.SOUTH],
            is_right=None
        )

        return [top_line, *middle_lines, bottom_line]

    def path_visited(self, char):
        self.is_visited = True
        self.content = check_content(char)

    def __str__(self):
        return "\n".join(self.get_cell_lines_str())

    def remove_wall(self, wall_direction: Direction):
        self.walls[wall_direction] = False