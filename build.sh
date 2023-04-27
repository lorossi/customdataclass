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

reportfolder="coverage"
docsfolder="docs"
jsonreport="coverage.json"
buildsfolder="dist"

# compute the coverage and pipe all output to /dev/null
coverage run -d $reportfolder -m unittest discover -s ./tests -p "test*.py" -q > /dev/null 2>&1
echo -e "\033[1;32mCoverage computed and saved in $reportfolder\033[0m"
coverage html -d $reportfolder > /dev/null 2>&1
echo -e "\033[1;32mCoverage report generated in $reportfolder\033[0m"
# generate the coverage as a json file
coverage json -o $jsonreport > /dev/null 2>&1
echo -e "\033[1;32mJSON file generated in $jsonreport\033[0m"
# build the documentation
cd src
pdoc --html -o ../$docsfolder customdataclass.py > /dev/null 2>&1
echo -e "\033[1;32mDocumentation generated in $docsfolder\033[0m"
# rename the file
mv ../$docsfolder/customdataclass.html ../$docsfolder/index.html
# return to the root folder
cd ..
# build the package and get the last word as the package name
python3 -m build -o $buildsfolder > /dev/null 2>&1
echo -e "\033[1;Builds saved in $buildsfolder\033[0m"