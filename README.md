# Code coverage

We're aiming for 100% code coverage on the project, track our progress here:  [![codecov](https://codecov.io/gh/debrief/python-import-library/branch/develop/graph/badge.svg)](https://codecov.io/gh/debrief/python-import-library)

# Jupyter demo

Link to working demo of datafile import: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/debrief/python-import-library/master?filepath=jupyter%2FDataStore_sqliteExperiment.ipynb)

Placeholder for live Jupyter view of whole repo
[![Master branch](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/debrief/python-import-library/master)

# Setup

To prepare for running ensure these tools and packages are installed:
* Python 3 - at least Python 3.6.4 or later
* SQL Alchemy 1.3

For Postgres support and unit tests these packages are also required:
* geoalchemy2
* psycopg2
* nose2 (0.9.1)

### Dependencies

Install the python dependencies with: `pip install -r requirements.txt`

Was: _To install packages use `pip install <package>` or `py -3 -m pip install <package>` depending on your installation_

### Unit tests

* Run the unit test suite with:  `coverage3 run -m unittest discover -v`
* View the unit test coverage with: `coverage report`

# Command Line Instructions

To run from the command line go to the top level directory of the library in your bash shell or terminal program

Run by specifying the program as a module with `-m` and leaving off the .py file extension

The exact executable name for invoking python will depend how you have it installed, but most commonly it's just `python`
  
For example run the Sqlite example using:  
```python -m Experiments.DataStore_sqliteExperiment```

# IntelliJ Instructions

To run from inside IntelliJ open the project  
Mark the `Store` package as source by right clicking on the directory and selecting `Mark Directory as -> Source Root`

Open any python module you want to run in the main editor window, right click anywhere in the editor and choose the `Run` or `Debug` option


