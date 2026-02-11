import subprocess
import sys

from generation_algorithms.aldous_broder import generate_aldous_broder_maze
from utils.validators import is_valid_input


def run(cmd: list[str]) -> int:
    result = subprocess.run(cmd)
    return result.returncode

type_check = False

if __name__ == "__main__":
    if type_check:
        mypy_code = run(["pipenv", "run", "mypy", "."])
        if mypy_code != 0:
            print("\n❌ mypy failed. Fix type errors before running.\n")
            sys.exit(mypy_code)

    print("Let's generate a Maze!")
    print("Please specify the dimensions of your maze")

    rows, cols = 0, 0

    while True:
        rows_input = input("> 👉 Rows: ").strip()
        if is_valid_input(rows_input):
            rows = int(rows_input)
            break
        print("❌ Invalid input. Enter a positive integer.")

    while True:
        cols_input = input("> 👉 Cols: ").strip()
        if is_valid_input(cols_input):
            cols = int(cols_input)
            break
        print("❌ Invalid input. Enter a positive integer.")

    print(generate_aldous_broder_maze(rows, cols))
