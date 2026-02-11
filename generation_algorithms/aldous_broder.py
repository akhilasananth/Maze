# Aldous Broder: https://tinyurl.com/y78a2edz

from components.grid import Grid


def generate_aldous_broder_maze(grid_rows: int, grid_cols: int) -> Grid:
    grid = Grid(grid_rows, grid_cols)
    start_char = "X"
    current_cell = grid.get_random_border_cell()
    grid.open_maze(current_cell)
    current_cell.is_visited = True

    visited_count = 1
    total_cells = grid.rows * grid.cols

    while visited_count < total_cells:
        # Pick a random neighbor (visited or not)
        neighbour, direction = grid.get_random_neighbour(current_cell)

        # If neighbour is unvisited, remove wall and mark visited
        if not neighbour.is_visited:
            grid.remove_grid_wall(*current_cell.pos, direction)
            neighbour.is_visited = True
            visited_count += 1

        # Move to the neighbor regardless
        current_cell = neighbour

    current_cell.set_cell_content(start_char)
    return grid

