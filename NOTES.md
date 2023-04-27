# Notes

- to build the documentation
  - go to the `src` directory
  - make sure that `pdoc3` is installed
  - run `pdoc --html -o ../docs customdataclass.py --force`
- to run the tests
  - go to the `root` directory
  - run `python3 -m unittest discover -v -s ./tests -p "test*.py"`
- to compute the coverage
  - go to the root directory
  - run `coverage run -m unittest discover -s ./tests -p "test*.py"`
  - run `coverage report -m` to see the report in the terminal
  - run `coverage html` to see the report in the browser

Use `build.sh` to build the documentation, run the tests and compute the coverage.