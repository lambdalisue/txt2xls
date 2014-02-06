#!/usr/bin/env bash
(cd docs; make clean; make man)
cp -rf docs/_build/man/txt2xls.1 .
