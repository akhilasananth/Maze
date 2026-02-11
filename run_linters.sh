#!/bin/bash

echo -e "\033[1;31mRunning Black 🐸\033[0m"
black .
echo

echo -e "\033[1;31mRunning Ruff (check + fix) 🐸\033[0m"
ruff check . --fix
echo

echo -e "\033[1;31m️Running Ruff (format) 🐸\033[0m"
ruff format .
echo
#
#echo -e "\033[1;31mRunning Bandit 🐸\033[0m"
#bandit -r .
#echo
#
#echo -e "\033[1;31mRunning Safety 🐸\033[0m"
#safety check
#echo

echo -e "\033[1;31mRunning Pydocstyle 🐸\033[0m"
pydocstyle .
echo

# chmod +x run_linters.sh
# ./run_linters.sh