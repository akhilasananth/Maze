import pytest
from components.quad.quad_cell import QuadCell, QuadDirection, get_cell_content, build_cell_line
from constants import (
    VERTICAL_CHAR,
    IN_BETWEEN_CELLS_CHAR,
    HORIZONTAL_CHAR,
    CELL_WIDTH,
    CELL_HEIGHT,
)


@pytest.fixture
def test_cell():
    return QuadCell(0, 0)


# get cell content


# build_cell_line



# To String tests
def test_tostr_all_walls(test_cell):
    assert str(test_cell) == "+---+\n│   │\n+---+"


def test_tostr_no_north_wall(test_cell):
    test_cell.walls[QuadDirection.NORTH] = False
    assert str(test_cell) == "+   +\n│   │\n+---+"


def test_tostr_no_south_wall(test_cell):
    test_cell.walls[QuadDirection.SOUTH] = False
    assert str(test_cell) == "+---+\n│   │\n+   +"


def test_tostr_no_west_wall(test_cell):
    test_cell.walls[QuadDirection.WEST] = False
    assert str(test_cell) == "+---+\n    │\n+---+"


def test_tostr_no_east_wall(test_cell):
    test_cell.walls[QuadDirection.EAST] = False
    assert str(test_cell) == "+---+\n│    \n+---+"


def test_tostr_no_walls(test_cell):
    for direction in QuadDirection:
        test_cell.walls[direction] = False
    assert str(test_cell) == "+   +\n     \n+   +"


def test_tostr_remove_wall(test_cell):
    test_cell.remove_wall(QuadDirection.NORTH)
    assert str(test_cell) == "+   +\n│   │\n+---+"


def test_tostr_add_wall(test_cell):
    test_cell.remove_wall(QuadDirection.NORTH)
    test_cell.remove_wall(QuadDirection.SOUTH)
    test_cell.add_wall(QuadDirection.SOUTH)
    assert str(test_cell) == "+   +\n│   │\n+---+"


# get_cell_lines
def test_get_cell_lines_structure(test_cell, monkeypatch):
    # mock CELL_HEIGHT
    monkeypatch.setattr("components.constants.CELL_HEIGHT", 3)

    # Set up a cell
    walls = {
        QuadDirection.NORTH: True,
        QuadDirection.SOUTH: False,
        QuadDirection.EAST: True,
        QuadDirection.WEST: False,
    }
    content = "X"
    test_cell.walls = walls
    test_cell.set_cell_content(content)

    cell_lines = test_cell.get_cell_lines()

    # Check the total number of cell_lines
    assert len(cell_lines) == CELL_HEIGHT + 2  # Middle + top + bottom.

    # Check content appears exactly once vertically
    middle_lines = cell_lines[1:-1]  # Exclude top/bottom
    for i, line in enumerate(middle_lines):
        if i == CELL_HEIGHT // 2:
            assert content in line
        else:
            assert content not in line

    # Check content is centered horizontally
    middle_line = middle_lines[CELL_HEIGHT // 2]
    stripped_middle = middle_line.strip(
        VERTICAL_CHAR + " "
    )  # Remove borders and spaces
    assert stripped_middle == content

    # Top and bottom cell_lines match build_cell_line output
    assert cell_lines[0] == build_cell_line(None, walls[QuadDirection.NORTH], None)
    assert cell_lines[-1] == build_cell_line(None, walls[QuadDirection.SOUTH], None)


# _check_wall_direction
def test_check_is_wall_a_direction(test_cell):
    incorrect_direction = "inside"
    with pytest.raises(TypeError) as execute_is_direction:
        test_cell._check_wall_direction(incorrect_direction)

    assert (
        str(execute_is_direction.value)
        == f"{incorrect_direction} is not a defined Direction. The input has to be a direction."
    )


def test_check_wall_direction_undefined_in_cell(test_cell):
    with pytest.raises(ValueError) as execute_is_wall:
        test_cell._check_wall_direction(QuadDirection.NORTH_WEST)

    assert str(execute_is_wall.value) == "Please enter a valid wall direction."

# add and remove wall tests
def test_remove_wall(test_cell):
    test_cell.remove_wall(QuadDirection.NORTH)
    test_cell.remove_wall(QuadDirection.WEST)
    walls_dict = {
        QuadDirection.NORTH: False,
        QuadDirection.EAST: True,
        QuadDirection.SOUTH: True,
        QuadDirection.WEST: False,
    }
    assert test_cell.walls == walls_dict


def test_remove_wall_invalid(test_cell):
    pass


def test_add_wall(test_cell):
    pass


def test_add_wall_invalid(test_cell):
    pass



# set is_visited


def test_set_is_visited(test_cell):
    pass


def test_set_is_visited_invalid(test_cell):
    with pytest.raises(TypeError) as set_is_visited_info:
        test_cell.set_is_visited("yes")

    assert str(set_is_visited_info.value) == "is_visited must be a boolean"
