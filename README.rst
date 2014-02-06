txt2xls
==========================
.. image:: https://secure.travis-ci.org/lambdalisue/txt2xls.png?branch=master
    :target: http://travis-ci.org/lambdalisue/txt2xls
    :alt: Build status

.. image:: https://coveralls.io/repos/lambdalisue/txt2xls/badge.png?branch=master
    :target: https://coveralls.io/r/lambdalisue/txt2xls/
    :alt: Coverage

.. image:: https://pypip.in/d/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Downloads

.. image:: https://pypip.in/v/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Latest version

.. image:: https://pypip.in/wheel/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Wheel Status

.. image:: https://pypip.in/egg/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: Egg Status

.. image:: https://pypip.in/license/txt2xls/badge.png
    :target: https://pypi.python.org/pypi/txt2xls/
    :alt: License

txt2xls convert raw text data files into a single excel file.
It use `maidenhair <https://github.com/lambdalisue/maidenhair>`_ for reading raw
text files so any kind of raw text file can be used if there is a maidenhair
plugins.

Installation
------------
Use pip_ like::

    $ pip install txt2xls

.. _pip:  https://pypi.python.org/pypi/pip

Quick Usage
-------------
Assume there are several raw text data files like::

    # Sample1.txt
    0 10
    1 20
    2 30
    3 40
    4 50
    5 60
    # Sample2.txt
    0 15
    1 25
    2 35
    3 45
    4 55
    5 65
    # Sample3.txt
    0 12
    1 22
    2 32
    3 42
    4 52
    5 62

Then run *txt2xls* with

    % txt2xls -o output Sample*.txt

It will produce ``output.xls`` file.
The excel file have ``Sample1``, ``Sample2``, and ``Sample3`` sheets.

Usage
------

::

    usage: txt2xls [-h] [-v] [-o OUTPUT] [--raise-exceptions] [-p PARSER]
                [-l LOADER] [-a] [--unite-basecolumn UNITE_BASECOLUMN]
                [-u USING] [--relative] [--relative-origin RELATIVE_ORIGIN]
                [--relative-basecolumn RELATIVE_BASECOLUMN]
                [--baseline BASELINE] [--baseline-column BASELINE_COLUMN]
                [--baseline-function BASELINE_FUNCTION]
                infiles [infiles ...]

    positional arguments:
    infiles               Path list of data files or directories which have data
                            files.

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -o OUTPUT, --output OUTPUT
                            An output filename without extensions. The required
                            filename extension will be automatically determined
                            from an output format.
    --raise-exceptions    If it is specified, raise exceptions.
    -p PARSER, --parser PARSER
                            A maidenhair parser name which will be used to parse
                            the raw text data. If it is not specified, a parser
                            which was specified in a txt2xls configure file will
                            be used.
    -l LOADER, --loader LOADER
                            A maidenhair loader name which will be used to load
                            the raw text data. If it is not specified, a parser
                            which was specified in a txt2xls configure file will
                            be used.
    -a, --auto-unite      Automatically unite thedataset which filename middle
                            extensions have only integers. See "Filename middle
                            extensions" also.
    --unite-basecolumn UNITE_BASECOLUMN
                            A column number which will be used to regulate data
                            regions for automatical unite. See `--auto` option
                            also.
    -u USING, --using USING
                            A colon separated column number of the raw text data
                            which will be used to determine X and Y columns.
    --relative            If it is True, the raw data will be converted to
                            relative data from the specified origin, based on the
                            specified column. See `--relative-origin` and
                            `--relative-basecolumn` also.
    --relative-origin RELATIVE_ORIGIN
                            A dataset number which will be used as an orign of the
                            relative data. It is used with `--relative` option.
    --relative-basecolumn RELATIVE_BASECOLUMN
                            A column number which will be used as a base column to
                            make the data relative. It is used with `--relative`
                            option.
    --baseline BASELINE   If it is specified, the specified data file is used as
                            a baseline of the dataset. See `--baseline-column` and
                            `--baseline-function` also.
    --baseline-column BASELINE_COLUMN
                            A column number which will be proceeded for baseline
                            regulation. It is used with `--baseline` option.
    --baseline-function BASELINE_FUNCTION
                            A python code of a "lambda" function which is used to
                            determine the baseline value from the data. `columns`
                            and `column` variables are available in the code.


Preference
-----------
You can create configure file as ``~/.config/txt2xls/txt2xls.cfg`` (Linux),
``~/.txt2xls.cfg`` (Mac), or ``%APPDATA%\txt2xls\txt2xls.cfg`` (Windows).

The default preference is equal to the configure file as below::

    [main]
    # --output
    output = 'output'
    # --raise-exception
    raise_exception = False

    [maidenhair]
    # --parser
    parser = 'parsers.PlainParser'
    # --loader
    loader = 'loaders.PlainLoader'
    # --using
    using = list(0,1)
    # --auto-unite
    auto_unite = False
    # --unite-basecolumn
    unite_basecolumn = 0

    [filters]
    relative = False
    relative_origin = 0
    relative_basecolumn = 1
    baseline = False
    baseline_column = 1
    baseline_function = 'columns[column][0]'

I don't use Microsoft Windows so the location of the configure file in Windows
might be wrong.
Let me know if there are any mistakes.
