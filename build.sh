#!/bin/bash

reportfolder="coverage"
docsfolder="docs"
jsonreport="coverage.json"
buildsfolder="dist"
virtualenv="buildvenv"
releaseenv="releaseenv"

# create the folders if they don't exist
mkdir -p $reportfolder
mkdir -p $docsfolder
mkdir -p $buildsfolder

# create the virtual environment
python -m venv $virtualenv
# activate the virtual environment
source $virtualenv/bin/activate
# install the requirements
pip install --upgrade pip
pip install -r requirements.txt
pip install coverage pdoc3 build

# run all test, pipe all output to stdout and grep for the OK string
result=$(python -m unittest discover -s ./tests -p "test*.py" -q 2>&1 | grep OK)

# if the result is empty, then the tests failed
if [ -z "$result" ]
then
    echo -e "\033[1;31mTests failed. Exiting.\033[0m"
    deactivate
    exit 1
else
    echo -e "\033[1;32mTests passed. Continuing.\033[0m"
fi

# compute the coverage
coverage run --omit="*/test*" -m unittest discover -s ./tests -p "test*.py" -q
echo -e "\033[1;32mCoverage computed and saved in $reportfolder\033[0m"
# generate the coverage report in html
coverage html -d $reportfolder
echo -e "\033[1;32mCoverage report generated in $reportfolder\033[0m"
# generate the coverage report in json
coverage json -o $jsonreport
echo -e "\033[1;32mJSON file generated in $jsonreport\033[0m"
# build the documentation
cd src
pdoc --html -o ../$docsfolder customdataclass.py
echo -e "\033[1;32mDocumentation generated in $docsfolder\033[0m"
# rename the file so it is currently displayed in gihub pages
mv ../$docsfolder/customdataclass.html ../$docsfolder/index.html
# return to the root folder
cd ..
# clean the build folder
rm -rf $buildsfolder
# build the package
python -m build -o $buildsfolder
echo -e "\033[1;Builds saved in $buildsfolder\033[0m"
# zip the builds
tar -czvf $buildsfolder.tar.gz $buildsfolder
echo -e "\033[1;32mBuilds zipped in $buildsfolder.tar.gz\033[0m"
# try to install the package
echo -e "\033[1;32mInstalling the package\033[0m"
# find the package name
package=$(ls $buildsfolder | grep .whl)
# install the package, if it fails, exit
pip install $buildsfolder/$package
# deactivate the virtual environment
deactivate
# delete the virtual environment
rm -rf $virtualenv

if [ $? -ne 0 ]
then
    echo -e "\033[1;31mInstallation failed. Exiting.\033[0m"
    exit 1
fi

# ask the user if he wants to push the package to pypi (in yellow)
read -p $'\033[1;33mDo you want to push the package to PyPi? (y/n) \033[0m' -n 1 -r
echo

# if the user doesn't want to push the package, exit
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo -e "\033[1;31mExiting.\033[0m"
    exit 1
fi

# create a virtual environment for the build
python -m venv $releaseenv
# activate the virtual environment
source $releaseenv/bin/activate
# install the requirements
pip install twine
# install twine
echo -e "\033[1;32mInstalling twine\033[0m"
pip install twine
# push the page to pypi using twine
echo -e "\033[1;32mPushing to PyPi\033[0m"
twine upload $buildsfolder/*
# deactivate the virtual environment
deactivate
# delete the virtual environment
rm -rf $releaseenv