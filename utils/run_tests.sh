#!/usr/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1

MODULE="tomatic"
PROGRAM="pytest"
REQUIREMENT="pytest pytest-cov"

[[ ! $( which $PROGRAM ) ]] && pip3 install $REQUIREMENT

ARGS="-vv"
TEST_FILES="${MODULE}/tests.py"

[[ $COV ]] && COVERAGE="--cov=${MODULE} --cov-report=html" || COVERAGE="--cov=${MODULE}"

$PROGRAM $ARGS $COVERAGE $TEST_FILES
