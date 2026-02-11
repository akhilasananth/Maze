import random

from components.cell import Cell
from components.grid import Grid
import pytest
from pytest import MonkeyPatch
from dataclasses import dataclass

from enums.direction_enums import QuadDirection


@dataclass
class TestObjects:
    middle_cell_pos: tuple[int, int]
    top_right_corner_cell_pos: tuple[int, int]
    bottom_left_corner_cell_pos: tuple[int, int]
    grid: "Grid"


@pytest.fixture
def test_objects() -> TestObjects:
    grid = Grid(3, 3)
    return TestObjects(
        middle_cell_pos=(1, 1),
        top_right_corner_cell_pos=(0, 2),
        bottom_left_corner_cell_pos=(2, 0),
        grid=grid,
    )


@pytest.fixture
def fixed_random_choice(monkeypatch: MonkeyPatch) -> None:
    """
    Fixture that monkeypatches random.choice to always pick the first element.
    Can be used in any test that needs deterministic random.choice.
    """
    monkeypatch.setattr(random, "choice", lambda x: x[0])


# Create Grid
def test_create_grid_dimensions() -> None:
    g = Grid(3, 4)
    grid = g.create_grid()

    assert len(grid) == 3
    assert all(len(row) == 4 for row in grid)


def test_create_grid_contains_cells() -> None:
    g = Grid(2, 2)
    grid = g.create_grid()

    assert isinstance(grid[0][0], Cell)
    assert grid[0][0].pos == (0, 0)
    assert grid[1][1].pos == (1, 1)


# Full Grid
def test_tostr_grid_full(test_objects: TestObjects) -> None:
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
def test_tostr_grid_middle_no_north(test_objects: TestObjects) -> None:
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


def test_tostr_grid_middle_no_east(test_objects: TestObjects) -> None:
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


def test_tostr_grid_middle_no_south(test_objects: TestObjects) -> None:
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


def test_tostr_grid_middle_no_west(test_objects: TestObjects) -> None:
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
def test_tostr_grid_top_right_corner_no_north(test_objects: TestObjects) -> None:
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


def test_tostr_grid_top_right_corner_no_west(test_objects: TestObjects) -> None:
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


def test_tostr_grid_top_right_corner_no_east(test_objects: TestObjects) -> None:
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


def test_tostr_grid_top_right_corner_no_south(test_objects: TestObjects) -> None:
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
def test_tostr_grid_bottom_left_corner_no_north(test_objects: TestObjects) -> None:
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


def test_tostr_grid_bottom_left_corner_no_east(test_objects: TestObjects) -> None:
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


def test_tostr_grid_bottom_left_corner_no_south(test_objects: TestObjects) -> None:
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


def test_tostr_grid_bottom_left_corner_no_west(test_objects: TestObjects) -> None:
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
