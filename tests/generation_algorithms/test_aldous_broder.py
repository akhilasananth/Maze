import pytest
from generation_algorithms.aldous_broder import generate_aldous_broder_maze


@pytest.mark.parametrize(
    "rows,cols",
    [
        (2, 2),
        (5, 5),
        (10, 10),
        (1, 10),
        (10, 1),
    ],
)
def test_maze_accessibility(rows, cols):
    grid = generate_aldous_broder_maze(rows, cols)

    # Now test accessibility
    assert grid.all_cells_accessible(), "Some cells are inaccessible!"