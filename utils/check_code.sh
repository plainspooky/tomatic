#!/usr/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1

MODULE="tomatic"
PROGRAM="mypy"
REQUIREMENT="mypy lxml"

[[ ! $( which $PROGRAM ) ]] && pip3 install $REQUIREMENT

REPORT_DIR="./reports/$PROGRAM"
mkdir -p ${REPORT_DIR}

# --no-warn-incomplete-stub
ARGS=" --html-report ${REPORT_DIR}"

$PROGRAM $ARGS $MODULE
