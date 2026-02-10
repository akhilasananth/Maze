import pytest

from components.cell import Cell
from components.quad.quad_cell import QuadCell
from constants import VERTICAL_CHAR, IN_BETWEEN_CELLS_CHAR, HORIZONTAL_CHAR, CELL_WIDTH
from enums.direction_enums import TriangleDirection, QuadDirection


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
