import random

from components.cell import Cell, Direction
from components.constants import CellType


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list[Cell]] = self.create_grid()

    def create_grid(self) -> list[list[Cell]]:
        return [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def get_cell_coord_in_direction(self, cell: Cell, direction: Direction) -> tuple[int, int] | None:
        dr, dc = direction.value
        r, c = cell.pos
        nr, nc = r + dr, c + dc # neighbour coord

        if nr < 0 or nr > self.rows-1 or nc < 0 or nc > self.cols-1:
            print("There are no neighbouring cells in this direction")
            return None

        return nr, nc


    def remove_grid_wall(self, row, col, wall_direction: Direction):
        self.grid[row][col].remove_wall(wall_direction)

        opposite_direction = wall_direction.get_opposite()
        opposite_cell_coord = self.get_cell_coord_in_direction(self.grid[row][col], wall_direction)

        if opposite_cell_coord:
            nr, nc = opposite_cell_coord
            self.grid[nr][nc].remove_wall(opposite_direction)


    def __str__(self):
        lines: list[str] = []

        for r, row in enumerate(self.grid):
            # Prepare lists of cell_lines for each cell
            row_lines = [cell.get_cell_lines() for cell in row]

            # To avoid repeated row borders: the south line of all cells except for the last is skipped
            if r < len(self.grid) - 1:
                for lines_of_cell in row_lines:
                    lines_of_cell.pop()

            # Merge each line of all cells in the row
            for i in range(len(row_lines[0])):  # top/middle/bottom
                merged_line = ""
                for j, cell_line in enumerate(row_lines):
                    if j == 0:
                        merged_line += cell_line[i]  # include left wall of first cell
                    else:
                        # Skip first char of each subsequent cell to avoid double left wall
                        merged_line += cell_line[i][1:]
                lines.append(merged_line)

        return "\n".join(lines)

    def get_unvisited_cells(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if not cell.is_visited
        ]

    def get_random_cell(self, unvisited_cells: list[tuple[int, int]], cell_type: CellType) -> Cell:
        if not unvisited_cells:
            raise RuntimeError(f"{cell_type.value} cells in the grid have already been visited.")

        r, c = random.choice(unvisited_cells)
        return self.grid[r][c]

    def get_random_any_cell(self) -> Cell:
        return self.get_random_cell(self.get_unvisited_cells(), CellType.ALL)

    def get_random_border_cell(self) -> Cell:
        border_unvisited_cells = [
            (r, c)
            for r, c in self.get_unvisited_cells()
            if r == 0 or r == self.rows-1 or c == 0 or c == self.cols-1
        ]
        return self.get_random_cell(border_unvisited_cells, CellType.BORDER)

    def open_maze(self, border_cell: Cell) -> None:
        # If the cell is a border cell, then remove the outer border, opening up the maze
        # This is for the cell from which the game will be starting

        r,c = border_cell.pos

        if not(r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1):
            print("The input cell is not a border cell. Please input a border cell")
            return None

        # top left corner
        if border_cell.pos == (0,0):
            border_cell.remove_wall(random.choice([Direction.NORTH, Direction.WEST]))

        # top right corner
        if border_cell == (0,self.cols-1):
            border_cell.remove_wall(random.choice([Direction.NORTH, Direction.EAST]))

        # bottom left corner
        if border_cell == (self.rows-1,0):
            border_cell.remove_wall(random.choice([Direction.SOUTH, Direction.WEST]))

        # bottom right corner
        if border_cell == (self.rows-1, self.cols-1):
            border_cell.remove_wall(random.choice([Direction.SOUTH, Direction.EAST]))

        # north border cell
        if r == 0:
            border_cell.remove_wall(Direction.NORTH)

        # east border cell
        if c == self.cols-1:
            border_cell.remove_wall(Direction.EAST)

        # south border cell
        if r == self.rows-1:
            border_cell.remove_wall(Direction.SOUTH)

        # west border cell
        if c == 0:
            return border_cell.remove_wall(Direction.WEST)

        return None

    def get_random_unvisited_neighbour(self, cell: Cell) -> tuple[Cell, Direction] | None:
        """
        returns a tuple of the random unvisited neighbor Cell and its direction relative to the current cell
        or None if the cells in all 4 directions are visited
        """
        neighbors: list[tuple[Cell, Direction]] = []

        for direction in Direction:
            n_cell_coord = self.get_cell_coord_in_direction(cell, direction)

            if n_cell_coord:
                nr, nc = n_cell_coord
                neighbor = self.grid[nr][nc]

                if not neighbor.is_visited:
                    neighbors.append((neighbor, direction))

        if not neighbors:
            return None

        return random.choice(neighbors)


