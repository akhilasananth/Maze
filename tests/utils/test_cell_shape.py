# get_number_of_walls
import pytest

from enums.direction_enums import TriangleDirection, QuadDirection


def test_get_number_of_walls(test_cell):
    assert test_cell.get_number_of_walls() == 4


# is_valid_wall


def test_is_valid_wall_incorrect_direction_type(test_cell):
    with pytest.raises(TypeError) as execute_is_valid_wall:
        test_cell.is_valid_wall("northwall")

    assert str(execute_is_valid_wall.value) == "Expected DirectionType, got str"


def test_is_valid_wall_incorrect_wall_direction(test_cell):
    with pytest.raises(ValueError) as execute_is_valid_wall:
        test_cell.is_valid_wall(TriangleDirection.NORTH_WEST)

    assert str(execute_is_valid_wall.value) == (
        "TriangleDirection.NORTH_WEST is an invalid wall direction for "
        "this cell shape: CellShape.QUAD"
    )


def test_is_valid_wall_correct_wall_direction(test_cell):
    try:
        test_cell.is_valid_wall(QuadDirection.NORTH)
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")
