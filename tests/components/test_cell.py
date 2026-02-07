import pytest
from components.cell import Cell, Direction


@pytest.fixture
def test_cell():
    return Cell(0,0)

def test_tostr_all_walls(test_cell):
    assert str(test_cell) == "---\n│ │\n---"

def test_tostr_no_north_wall(test_cell):
    test_cell.walls[Direction.NORTH] = False
    assert str(test_cell) == "│ │\n---"

def test_tostr_no_south_wall(test_cell):
    test_cell.walls[Direction.SOUTH] = False
    assert str(test_cell) == "---\n│ │"

def test_tostr_no_west_wall(test_cell):
    test_cell.walls[Direction.WEST] = False
    assert str(test_cell) == "---\n  │\n---"

def test_tostr_no_east_wall(test_cell):
    test_cell.walls[Direction.EAST] = False
    assert str(test_cell) == "---\n│  \n---"

def test_tostr_no_walls(test_cell):
    for direction in Direction:
        test_cell.walls[direction] = False
    assert str(test_cell) == "   "

def test_tostr_remove_wall(test_cell):
    test_cell.remove_wall(Direction.NORTH)
    assert test_cell.walls[Direction.NORTH] == False
    assert str(test_cell) == "│ │\n---"