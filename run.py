import subprocess
import sys


def run(cmd: list[str]) -> int:
    result = subprocess.run(cmd)
    return result.returncode


if __name__ == "__main__":
    mypy_code = run(["pipenv", "run", "mypy", "."])
    if mypy_code != 0:
        print("\n❌ mypy failed. Fix type errors before running.\n")
        sys.exit(mypy_code)

    program_code = run(
        ["pipenv", "run", "python", "generation_algorithms/aldous_broder.py"]
    )
    sys.exit(program_code)
