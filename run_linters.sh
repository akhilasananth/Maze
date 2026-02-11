#!/bin/bash

echo -e "\033[1;31mRunning Black 🐸\033[0m"
black .
echo

echo -e "\033[1;31mRunning Ruff (check + fix) 🐸\033[0m"
ruff check . --fix
echo

echo "🏃🏻‍♀️Running Ruff (format)..."
#echo -e "\033[1;31mRunning Black 🐸\033[0m"
ruff format .
echo

echo "🏃🏻‍♀️Running Bandit..."
#echo -e "\033[1;31mRunning Black 🐸\033[0m"
bandit -r .
echo

echo "🏃🏻‍♀️Running Safety..."
safety check
echo

echo "🏃🏻‍♀️Running Pydocstyle..."
pydocstyle .
echo

# chmod +x run_linters.sh
# ./run_linters.sh