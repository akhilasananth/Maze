from utils.validators import check_type


def get_cell_content(char: str) -> str:
    """
    Get the cell content if it's a single character and a string.
    :param char: Cell content char.
    """

    check_type(char, str)

    if len(char) == 0:
        return " "

    if len(char) > 1:
        raise ValueError("The cell content must be exactly 1 character")

    return char
