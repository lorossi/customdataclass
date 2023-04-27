#!/bin/bash

# activate virtual environment
source venv/bin/activate
# run all tests
python3 -m unittest discover -s ./tests -p "test*.py"
# compute the coverage
coverage run -m unittest discover -s ./tests -p "test*.py"
# generate the report
coverage html
# open the report
firefox htmlcov/index.html
# build the documentation
cd src
pdoc --html -o ../docs customdataclass.py --force