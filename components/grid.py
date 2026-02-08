import random

from components.cell import Cell, Direction
from components.constants import CellType


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list[Cell]] = self.create_grid()

    def __str__(self):
        lines: list[str] = []

        for r, row in enumerate(self.grid):
            # Prepare lists of get_cell_lines for each cell
            row_lines = [cell.get_cell_lines() for cell in row]
            # remove last line of all cells if this row is not the last row
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

    def create_grid(self) -> list[list[Cell]]:
        return [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]

    def get_unvisited_cells(self) -> list[tuple[int, int]]:
        return [
            (r, c)
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if not cell.is_visited
        ]

    def get_random_cell(self, unvisited_cells: list[tuple[int, int]], cell_type: CellType) -> Cell:
        if not unvisited_cells:
            raise RuntimeError(f"{cell_type} cells in the grid have already been visited.")

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
            dr, dc = direction.value # direction relative to the current cell
            r, c = cell.pos[0] + dr, cell.pos[1] + dc

            # Check bounds
            if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]):
                neighbor = self.grid[r][c]
                if not neighbor.is_visited:
                    neighbors.append((neighbor, direction))

        if not neighbors:
            return None

        return random.choice(neighbors)

    def remove_shared_wall(self, curr_cell_pos: tuple[int, int], wall_direction: Direction): pass

