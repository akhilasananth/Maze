# Aldous Broder: https://tinyurl.com/y78a2edz

from components.grid import Grid

def is_valid_input(dimension: str) -> bool:
    try:
        return int(dimension) > 0
    except ValueError:
        print("❌ Invalid input. Enter a positive integer.")
        return False

print("Let's generate a Maze!")
print("Please specify the dimensions of your maze")

rows, cols = 0, 0

while True:
    rows_input = input("> 👉 Rows: ").strip()
    if is_valid_input(rows_input):
        rows = int(rows_input)
        break

while True:
    cols_input = input("> 👉 Cols: ").strip()
    if is_valid_input(cols_input):
        cols = int(cols_input)
        break

# Create Grid
grid = Grid(rows,cols)
delta = (1, 1)
display_rc = lambda pos: tuple(a + b for a, b in zip(pos, delta))

# Pick a random starting cell
current_cell = grid.get_random_cell()
current_cell.path_visited('X')
disp_rc = display_rc(current_cell.pos)
print(f"Starting at X: row: {disp_rc[0]} col: {disp_rc[1]}")

# Loop until all cells are visited
while True:
    # Pick a random unvisited neighbour
    random_neighbour = grid.get_random_unvisited_neighbour(current_cell)

    if random_neighbour is not None:
        neighbour, direction = random_neighbour
        # print("Moving to:", neighbour.pos)

        # Remove walls between current cell and neighbour
        current_cell.remove_wall(direction)
        neighbour.remove_wall(direction.get_opposite())

        # Mark neighbour as visited
        neighbour.path_visited('o')

        # Move to neighbour
        current_cell = neighbour
    else:
        disp_rc = display_rc(current_cell.pos)
        current_cell.path_visited('M')
        print(f"Ending at M: {disp_rc[0]} col: {disp_rc[1]}")
        break


print(grid)
