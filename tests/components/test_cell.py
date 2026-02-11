import pytest

from components.cell import QuadCell
from constants import VERTICAL_CHAR, IN_BETWEEN_CELLS_CHAR, HORIZONTAL_CHAR, CELL_WIDTH
from enums.direction_enums import QuadDirection


@pytest.fixture
def test_cell():
    return QuadCell(0, 0)


# set_is_visited


def test_set_is_visited_correct(test_cell):
    test_cell.set_is_visited(True)
    assert test_cell.is_visited == True


def test_set_is_visited_incorrect(test_cell):
    with pytest.raises(TypeError) as execute_is_visited:
        test_cell.set_is_visited("yes")

    assert str(execute_is_visited.value) == "Expected bool, got str"


# set_cell_content
def test_set_cell_content_correct(test_cell):
    test_cell.set_cell_content("X")
    assert test_cell.content == "X"


def test_set_cell_content_incorrect_char_len(test_cell):
    with pytest.raises(ValueError) as set_cell_info:
        test_cell.set_cell_content("Hello")

    assert str(set_cell_info.value) == "The cell content must be exactly 1 character"


def test_set_cell_content_incorrect_type(test_cell):
    with pytest.raises(TypeError) as set_cell_info:
        test_cell.set_cell_content(2)

    assert str(set_cell_info.value) == "Expected str, got int"


def test_set_cell_content_empty_str(test_cell):
    test_cell.set_cell_content("")
    assert test_cell.content == " "


# remove_wall
def test_remove_wall(test_cell):
    test_cell.remove_wall(wall_direction=QuadDirection.NORTH)
    assert test_cell.shape.walls[QuadDirection.NORTH] == False


# add_wall
def test_add_wall(test_cell):
    test_cell.shape.walls = {d: False for d in QuadDirection}
    test_cell.add_wall(QuadDirection.NORTH)
    assert test_cell.shape.walls[QuadDirection.NORTH] == True


# build_cell_line
def test_build_cell_line_vertical_borders_only(test_cell):
    test_cell.set_cell_content("x")
    # Only left and right walls
    line = test_cell.build_cell_line(True, None, True, True)
    expected = f"{VERTICAL_CHAR} x {VERTICAL_CHAR}"
    assert line == expected


def test_build_cell_line_no_vertical_borders(test_cell):
    test_cell.set_cell_content("x")

    # No left/right walls, content in the middle
    line = test_cell.build_cell_line(False, None, False, True)
    expected = f"  x  "
    assert line == expected


def test_build_cell_line_in_between_char(test_cell):
    test_cell.set_cell_content("x")

    # Left/right None should give IN_BETWEEN_CELLS_CHAR
    line = test_cell.build_cell_line(None, None, None, True)
    expected = f"{IN_BETWEEN_CELLS_CHAR} x {IN_BETWEEN_CELLS_CHAR}"
    assert line == expected


def test_build_cell_line_horizontal_line(test_cell):
    test_cell.set_cell_content("x")

    # Horizontal line only
    line = test_cell.build_cell_line(None, True, None, True)
    expected = (
        f"{IN_BETWEEN_CELLS_CHAR}{HORIZONTAL_CHAR * CELL_WIDTH}{IN_BETWEEN_CELLS_CHAR}"
    )
    assert line == expected


def test_build_cell_line_horizontal_and_vertical(test_cell):
    test_cell.set_cell_content("x")

    # All borders
    line = test_cell.build_cell_line(True, True, True, True)
    # "x" is ignored because is_middle is True.
    expected = f"{VERTICAL_CHAR}{HORIZONTAL_CHAR * CELL_WIDTH}{VERTICAL_CHAR}"
    assert line == expected


def test_build_cell_line_horizontal_false_verticals(test_cell):
    test_cell.set_cell_content("x")

    # Horizontal false, verticals True
    line = test_cell.build_cell_line(True, False, True, True)
    expected = f"{VERTICAL_CHAR}{" " * CELL_WIDTH}{VERTICAL_CHAR}"
    assert line == expected


def test_build_cell_line_content_length_one_centered(test_cell, monkeypatch):
    test_cell.set_cell_content("M")
    test_cell_width = 9
    monkeypatch.setattr("components.cell.CELL_WIDTH", test_cell_width)

    # Content should be centered
    line = test_cell.build_cell_line(True, None, True, True)
    spaces = " " * (test_cell_width // 2)
    expected = f"{VERTICAL_CHAR}{spaces}M{spaces}{VERTICAL_CHAR}"
    assert line == expected


import pytest
from components.cell import (
    QuadCell,
    QuadDirection,
    build_cell_line,
)
from constants import (
    VERTICAL_CHAR,
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
