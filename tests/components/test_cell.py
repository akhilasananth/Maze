import pytest
from pytest import MonkeyPatch
from components.cell import Cell
from constants import VERTICAL_CHAR, IN_BETWEEN_CELLS_CHAR, HORIZONTAL_CHAR, CELL_WIDTH, CELL_HEIGHT
from enums.direction_enums import QuadDirection


@pytest.fixture
def test_cell() -> Cell:
    return Cell((0,0))

# To String tests
def test_tostr_all_walls(test_cell: Cell) -> None:
    assert str(test_cell) == "+---+\n│   │\n+---+"
def test_tostr_no_north_wall(test_cell: Cell) -> None:
    test_cell.walls[QuadDirection.NORTH] = False
    assert str(test_cell) == "+   +\n│   │\n+---+"
def test_tostr_no_south_wall(test_cell: Cell) -> None:
    test_cell.walls[QuadDirection.SOUTH] = False
    assert str(test_cell) == "+---+\n│   │\n+   +"
def test_tostr_no_west_wall(test_cell: Cell) -> None:
    test_cell.walls[QuadDirection.WEST] = False
    assert str(test_cell) == "+---+\n    │\n+---+"
def test_tostr_no_east_wall(test_cell: Cell) -> None:
    test_cell.walls[QuadDirection.EAST] = False
    assert str(test_cell) == "+---+\n│    \n+---+"
def test_tostr_no_walls(test_cell: Cell) -> None:
    for direction in QuadDirection:
        test_cell.walls[direction] = False
    assert str(test_cell) == "+   +\n     \n+   +"

# get_cell_lines
def test_get_cell_lines_structure(test_cell: Cell, monkeypatch: MonkeyPatch) -> None:
    # mock CELL_HEIGHT
    monkeypatch.setattr("constants.CELL_HEIGHT", 3)

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
    assert cell_lines[0] == test_cell.build_cell_line(None, walls[QuadDirection.NORTH], None)
    assert cell_lines[-1] == test_cell.build_cell_line(None, walls[QuadDirection.SOUTH], None)

# build_cell_line
def test_build_cell_line_vertical_borders_only(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")
    # Only left and right walls
    line = test_cell.build_cell_line(True, None, True, True)
    expected = f"{VERTICAL_CHAR} x {VERTICAL_CHAR}"
    assert line == expected
def test_build_cell_line_no_vertical_borders(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")

    # No left/right walls, content in the middle
    line = test_cell.build_cell_line(False, None, False, True)
    expected = f"  x  "
    assert line == expected
def test_build_cell_line_in_between_char(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")

    # Left/right None should give IN_BETWEEN_CELLS_CHAR
    line = test_cell.build_cell_line(None, None, None, True)
    expected = f"{IN_BETWEEN_CELLS_CHAR} x {IN_BETWEEN_CELLS_CHAR}"
    assert line == expected
def test_build_cell_line_horizontal_line(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")

    # Horizontal line only
    line = test_cell.build_cell_line(None, True, None, True)
    expected = (
        f"{IN_BETWEEN_CELLS_CHAR}{HORIZONTAL_CHAR * CELL_WIDTH}{IN_BETWEEN_CELLS_CHAR}"
    )
    assert line == expected
def test_build_cell_line_horizontal_and_vertical(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")

    # All borders
    line = test_cell.build_cell_line(True, True, True, True)
    # "x" is ignored because is_middle is True.
    expected = f"{VERTICAL_CHAR}{HORIZONTAL_CHAR * CELL_WIDTH}{VERTICAL_CHAR}"
    assert line == expected
def test_build_cell_line_horizontal_false_verticals(test_cell: Cell) -> None:
    test_cell.set_cell_content("x")

    # Horizontal false, verticals True
    line = test_cell.build_cell_line(True, False, True, True)
    expected = f"{VERTICAL_CHAR}{" " * CELL_WIDTH}{VERTICAL_CHAR}"
    assert line == expected
def test_build_cell_line_content_length_one_centered(test_cell: Cell, monkeypatch: MonkeyPatch) -> None:
    test_cell.set_cell_content("M")
    test_cell_width = 9
    monkeypatch.setattr("components.cell.CELL_WIDTH", test_cell_width)

    # Content should be centered
    line = test_cell.build_cell_line(True, None, True, True)
    spaces = " " * (test_cell_width // 2)
    expected = f"{VERTICAL_CHAR}{spaces}M{spaces}{VERTICAL_CHAR}"
    assert line == expected

# remove_wall
def test_tostr_remove_wall(test_cell: Cell) -> None:
    test_cell.remove_wall(QuadDirection.NORTH)
    assert str(test_cell) == "+   +\n│   │\n+---+"
def test_remove_wall(test_cell: Cell) -> None:
    test_cell.remove_wall(QuadDirection.NORTH)
    test_cell.remove_wall(QuadDirection.WEST)
    walls_dict = {
        QuadDirection.NORTH: False,
        QuadDirection.EAST: True,
        QuadDirection.SOUTH: True,
        QuadDirection.WEST: False,
    }
    assert test_cell.walls == walls_dict

# set_cell_content
def test_set_cell_content_correct(test_cell: Cell) -> None:
    test_cell.set_cell_content("X")
    assert test_cell.content == "X"
def test_set_cell_content_incorrect_char_len(test_cell: Cell) -> None:
    with pytest.raises(ValueError) as set_cell_info:
        test_cell.set_cell_content("Hello")

    assert str(set_cell_info.value) == "The cell content must be exactly 1 character"
def test_set_cell_content_empty_str(test_cell: Cell) -> None:
    test_cell.set_cell_content("")
    assert test_cell.content == " "