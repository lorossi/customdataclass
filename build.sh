#!/bin/bash

# activate virtual environment
source venv/bin/activate
# run all test, pipe all output to stdout and grep for the OK string
result=$(python3 -m unittest discover -s ./tests -p "test*.py" -q 2>&1 | grep OK)

# if the result is empty, then the tests failed
if [ -z "$result" ]
then
    echo -e "\033[1;31mTests failed. Exiting.\033[0m"
    exit 1
else
    echo -e "\033[1;32mTests passed. Continuing.\033[0m"
fi

# compute the coverage and pipe all output to /dev/null
python3 -m unittest discover -s ./tests -p "test*.py" -q > /dev/null 2>&1
echo -e "\033[1;32mCoverage computed and saved in .coverage.\033[0m"
# generate the report and get the last word as the folder name
reportfolder=$(coverage html | rev | cut -f1 -d ' ' | rev)
echo -e "\033[1;32mCoverage report generated in $reportfolder\033[0m"
# build the documentation
cd src > /dev/null 2>&1
docsfolder=$(pdoc --html -o ../docs customdataclass.py --force | rev | cut -f2 -d '/' | rev)
echo -e "\033[1;32mDocumentation generated in $docsfolder\033[0m"
# return to the root folder
cd .. > /dev/null 2>&1
# build the package and get the last word as the package name
builds=$(python3 -m build | tail -n 1)
echo -e "\033[1;32m$builds\033[0m"