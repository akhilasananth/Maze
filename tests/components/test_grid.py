import random
from components.quad.quad_cell import QuadCell, QuadDirection
from constants import CellType
from components.quad.quad_grid import Grid
import pytest
from dataclasses import dataclass


@dataclass
class TestObjects:
    middle_cell_pos: tuple[int, int]
    top_right_corner_cell_pos: tuple[int, int]
    bottom_left_corner_cell_pos: tuple[int, int]
    grid: "Grid"


@pytest.fixture
def test_objects():
    grid = Grid(3, 3)
    return TestObjects(
        middle_cell_pos=(1, 1),
        top_right_corner_cell_pos=(0, 2),
        bottom_left_corner_cell_pos=(2, 0),
        grid=grid,
    )


@pytest.fixture
def fixed_random_choice(monkeypatch):
    """
    Fixture that monkeypatches random.choice to always pick the first element.
    Can be used in any test that needs deterministic random.choice.
    """
    monkeypatch.setattr(random, "choice", lambda x: x[0])


# Create Grid
def test_create_grid_dimensions():
    g = Grid(3, 4)
    grid = g.create_grid()

    assert len(grid) == 3
    assert all(len(row) == 4 for row in grid)


def test_create_grid_contains_cells():
    g = Grid(2, 2)
    grid = g.create_grid()

    assert isinstance(grid[0][0], QuadCell)
    assert grid[0][0].pos == (0, 0)
    assert grid[1][1].pos == (1, 1)


# Full Grid
def test_tostr_grid_full(test_objects):
    grid = test_objects.grid

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


# Middle Cell Tests
def test_tostr_grid_middle_no_north(test_objects):
    grid = test_objects.grid
    r, c = test_objects.middle_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.NORTH)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+   +---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_middle_no_east(test_objects):
    grid = test_objects.grid
    r, c = test_objects.middle_cell_pos

    grid.remove_grid_wall(r, c + 1, QuadDirection.WEST)  # shared wall

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │       │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_middle_no_south(test_objects):
    grid = test_objects.grid
    r, c = test_objects.middle_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.SOUTH)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+   +---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_middle_no_west(test_objects):
    grid = test_objects.grid
    r, c = test_objects.middle_cell_pos

    grid.remove_grid_wall(r, c - 1, QuadDirection.EAST)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│       │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


# Top Right Corner Cell Tests
def test_tostr_grid_top_right_corner_no_north(test_objects):
    grid = test_objects.grid
    r, c = test_objects.top_right_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.NORTH)

    expected = (
        "+---+---+   +\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_top_right_corner_no_west(test_objects):
    grid = test_objects.grid
    r, c = test_objects.top_right_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.WEST)

    expected = (
        "+---+---+---+\n"
        "│   │       │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_top_right_corner_no_east(test_objects):
    grid = test_objects.grid
    r, c = test_objects.top_right_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.EAST)

    expected = (
        "+---+---+---+\n"
        "│   │   │    \n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_top_right_corner_no_south(test_objects):
    grid = test_objects.grid
    r, c = test_objects.top_right_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.SOUTH)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+   +\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


# Bottom Left Corner Cell Tests
def test_tostr_grid_bottom_left_corner_no_north(test_objects):
    grid = test_objects.grid
    r, c = test_objects.bottom_left_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.NORTH)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+   +---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_bottom_left_corner_no_east(test_objects):
    grid = test_objects.grid
    r, c = test_objects.bottom_left_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.EAST)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│       │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_bottom_left_corner_no_south(test_objects):
    grid = test_objects.grid
    r, c = test_objects.bottom_left_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.SOUTH)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+   +---+---+"
    )

    assert str(grid) == expected


def test_tostr_grid_bottom_left_corner_no_west(test_objects):
    grid = test_objects.grid
    r, c = test_objects.bottom_left_corner_cell_pos

    grid.remove_grid_wall(r, c, QuadDirection.WEST)

    expected = (
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "│   │   │   │\n"
        "+---+---+---+\n"
        "    │   │   │\n"
        "+---+---+---+"
    )

    assert str(grid) == expected


# Random Cell
def test_get_random_cell_returns_unvisited_cell(test_objects):
    g = test_objects.grid

    # All cells are unvisited initially
    cell = g.get_random_any_cell()
    assert isinstance(cell, QuadCell)
    assert cell.is_visited is False


def test_get_random_cell_returns_different_cells(test_objects, fixed_random_choice):
    g = test_objects.grid

    first_cell = g.get_random_any_cell()
    first_cell.is_visited = True  # mark as visited

    next_cell = g.get_random_any_cell()
    assert next_cell != first_cell  # should pick a different unvisited cell


def test_get_random_cell_raises_when_all_visited(test_objects):
    g = test_objects.grid

    # Mark all cells visited
    for row in g.grid:
        for cell in row:
            cell.is_visited = True

    # Expect RuntimeError
    with pytest.raises(
        RuntimeError,
        match=f"{CellType.ALL.value} cells in the grid have already been visited.",
    ):
        g.get_random_any_cell()


# Random Unvisited Neighbour
def test_random_unvisited_neighbour_returns_none_if_all_visited(test_objects):
    g = test_objects.grid
    middle_r, middle_c = test_objects.middle_cell_pos
    cell = g.grid[middle_r][middle_c]

    # mark all 4 neighbors visited
    g.grid[0][1].is_visited = True  # NORTH
    g.grid[2][1].is_visited = True  # SOUTH
    g.grid[1][2].is_visited = True  # EAST
    g.grid[1][0].is_visited = True  # WEST

    assert g.get_random_unvisited_neighbour(cell) is None


def test_random_unvisited_neighbour_returns_only_available_neighbor(
    test_objects, fixed_random_choice
):
    g = test_objects.grid
    middle_r, middle_c = test_objects.middle_cell_pos
    cell = g.grid[middle_r][middle_c]

    # For the middle cell, mark 3 visited, leave 1 unvisited
    g.grid[0][1].is_visited = True
    g.grid[2][1].is_visited = True
    g.grid[1][0].is_visited = True
    g.grid[1][2].is_visited = False  # EAST only available

    neighbor, direction = g.get_random_unvisited_neighbour(cell)

    assert neighbor == g.grid[1][2]
    assert direction == QuadDirection.EAST


def test_random_unvisited_neighbour_corner_cell_bounds(
    test_objects, fixed_random_choice
):
    g = test_objects.grid
    top_right_r, top_right_c = test_objects.top_right_corner_cell_pos
    cell = g.grid[top_right_r][top_right_c]

    # mark all visited except one valid neighbor
    g.grid[0][1].is_visited = False  # WEST
    g.grid[1][2].is_visited = True  # SOUTH

    neighbor, direction = g.get_random_unvisited_neighbour(cell)

    assert neighbor == g.grid[0][1]
    assert direction == QuadDirection.WEST
