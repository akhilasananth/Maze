import random

from components.cell import QuadDirection, Cell


class Grid:
    def __init__(self, rows: int, cols: int):
        self.rows: int = rows
        self.cols: int = cols
        self.grid: list[list[Cell]] = self.create_grid()
        self.all_cells: list[tuple[int, int]] = self.get_cells()

    def create_grid(self) -> list[list[Cell]]:
        return [
            [Cell((row, col)) for col in range(self.cols)] for row in range(self.rows)
        ]

    def get_cell_coord_in_direction(
        self, cell: Cell, direction: QuadDirection
    ) -> tuple[int, int] | None:
        dr, dc = direction.value
        r, c = cell.pos
        nr, nc = r + dr, c + dc  # neighbour coord

        if nr < 0 or nr > self.rows - 1 or nc < 0 or nc > self.cols - 1:
            return None

        return nr, nc

    def remove_grid_wall(
        self, row: int, col: int, wall_direction: QuadDirection
    ) -> None:
        self.grid[row][col].remove_wall(wall_direction)

        opposite_direction = wall_direction.get_opposite()
        opposite_cell_coord = self.get_cell_coord_in_direction(
            self.grid[row][col], wall_direction
        )

        if opposite_cell_coord:
            nr, nc = opposite_cell_coord
            self.grid[nr][nc].remove_wall(opposite_direction)

    def __str__(self) -> str:
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

    def get_cells(self) -> list[tuple[int, int]]:
        return [(r, c) for r, row in enumerate(self.grid) for c, cell in enumerate(row)]

    def _get_random_cell(self, cells: list[tuple[int, int]]) -> Cell:
        r, c = random.choice(cells)
        return self.grid[r][c]

    def get_random_any_cell(self) -> Cell:
        return self._get_random_cell(self.all_cells)

    def get_random_border_cell(self) -> Cell:
        border_cells = [
            (r, c)
            for r, c in self.get_cells()
            if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1
        ]
        return self._get_random_cell(border_cells)

    def open_maze(self, border_cell: Cell) -> None:
        # If the cell is a border cell, then remove the outer border, opening up the maze
        # This is for the cell from which the game will be starting

        r, c = border_cell.pos

        if not (r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1):
            print("The input cell is not a border cell. Please input a border cell")
            return None

        # top left corner
        if border_cell.pos == (0, 0):
            self.remove_grid_wall(
                r, c, random.choice([QuadDirection.NORTH, QuadDirection.WEST])
            )

        # top right corner
        if border_cell == (0, self.cols - 1):
            self.remove_grid_wall(
                r, c, random.choice([QuadDirection.NORTH, QuadDirection.EAST])
            )

        # bottom left corner
        if border_cell == (self.rows - 1, 0):
            self.remove_grid_wall(
                r, c, random.choice([QuadDirection.SOUTH, QuadDirection.WEST])
            )

        # bottom right corner
        if border_cell == (self.rows - 1, self.cols - 1):
            self.remove_grid_wall(
                r, c, random.choice([QuadDirection.SOUTH, QuadDirection.EAST])
            )

        # north border cell
        if r == 0:
            self.remove_grid_wall(r, c, QuadDirection.NORTH)

        # east border cell
        if c == self.cols - 1:
            self.remove_grid_wall(r, c, QuadDirection.EAST)

        # south border cell
        if r == self.rows - 1:
            self.remove_grid_wall(r, c, QuadDirection.SOUTH)

        # west border cell
        if c == 0:
            self.remove_grid_wall(r, c, QuadDirection.WEST)

        return None

    def get_random_neighbour(self, cell: Cell) -> tuple[Cell, QuadDirection] | None:
        """
        returns a tuple of the random neighbor Cell and its direction relative to the current cell
        or None if the cells in all 4 get_directions are visited
        """
        neighbors: list[tuple[Cell, QuadDirection]] = []

        for direction in QuadDirection:
            n_cell_coord = self.get_cell_coord_in_direction(cell, direction)

            if n_cell_coord:
                nr, nc = n_cell_coord
                neighbors.append((self.grid[nr][nc], direction))

        if neighbors:
            return random.choice(neighbors)
        return None

    def get_accessible_neighbours(self, cell):
        """
        Return a list of (direction, neighbour_cell) tuples where there is no wall.
        """
        accessible = []

        for direction in QuadDirection:  # assuming your directions are in an enum
            coord = self.get_cell_coord_in_direction(cell, direction)
            if coord is None:
                continue  # out of bounds
            r, c = coord
            neighbour = self.grid[r][c]
            # Check if there is no wall in that direction
            if not cell.walls[direction]:  # assuming walls dict uses QuadDirection keys
                accessible.append((direction, neighbour))

        return accessible

    def all_cells_accessible(self, start_cell):
        """Check if all cells in the maze are reachable from start_cell."""
        visited = set()
        stack = [start_cell]

        while stack:
            cell = stack.pop()
            if cell.pos in visited:
                continue
            visited.add(cell.pos)

            # Check neighbors that are accessible (no wall between)
            for direction, neighbour in self.get_accessible_neighbours(cell):
                if neighbour.pos not in visited:
                    stack.append(neighbour)

        return len(visited) == self.rows * self.cols
