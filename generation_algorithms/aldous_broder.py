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

main_start_char = "X"
main_end_char = "M"


# Pick a random starting cell
current_cell = grid.get_random_cell()
current_cell.path_visited(main_start_char)
print(f"Starting at {main_start_char}: row: {current_cell.pos[0]+1} "
      f"col: {current_cell.pos[1]+1}")
count = 1
# Loop until all cells are visited
while grid.get_unvisited_cells():
    # Pick a random unvisited neighbour
    random_neighbour = grid.get_random_unvisited_neighbour(current_cell)

    if random_neighbour is not None:
        neighbour, direction = random_neighbour
        # print("Moving to:", neighbour.pos)

        # Remove walls between current cell and neighbour
        current_cell.remove_wall(direction)
        neighbour.remove_wall(direction.get_opposite())

        # Mark neighbour as visited
        neighbour.is_visited = True

        # Move to neighbour
        current_cell = neighbour
    else:
        if count > 0:
            current_cell.path_visited(main_end_char)
            count -= 1
        current_cell = grid.get_random_cell()
        current_cell.is_visited = True


print(grid)
