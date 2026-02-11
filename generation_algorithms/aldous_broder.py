# Aldous Broder: https://tinyurl.com/y78a2edz

from components.grid import Grid


def is_valid_input(dimension: str) -> bool:
    try:
        return int(dimension) > 0
    except ValueError:
        return False


print("Let's generate a Maze!")
print("Please specify the dimensions of your maze")

rows, cols = 0, 0

while True:
    rows_input = input("> 👉 Rows: ").strip()
    if is_valid_input(rows_input):
        rows = int(rows_input)
        break
    print("❌ Invalid input. Enter a positive integer.")

while True:
    cols_input = input("> 👉 Cols: ").strip()
    if is_valid_input(cols_input):
        cols = int(cols_input)
        break
    print("❌ Invalid input. Enter a positive integer.")

# Create Grid
grid = Grid(rows, cols)

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

print(grid)
