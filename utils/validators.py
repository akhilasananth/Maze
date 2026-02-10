from typing import Type, Any


def check_type(value: Any, expected_type: Type) -> None:
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Expected {expected_type.__name__}, got {type(value).__name__}"
        )
