#!/bin/bash

echo "Running Black..."
black .

echo "Running Ruff (check + fix)..."
ruff check . --fix

echo "Running Ruff (format)..."
ruff format .

echo "Running Bandit..."
bandit -r .

echo "Running Safety..."
safety check

echo "Running Pydocstyle..."
pydocstyle .


# chmod +x run_linters.sh
# ./run_linters.sh