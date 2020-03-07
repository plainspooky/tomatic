#!/usr/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1
[[ ! -n $MODULE ]] && echo "Set 'MODULE' variable first!" && exit 1

PROGRAM="mypy"
REQUIREMENTS="requirements-${PROGRAM}.txt"

[[ ! $( which $PROGRAM ) ]] && pip3 install -r $REQUIREMENTS

REPORT_DIR="./reports/$PROGRAM"
mkdir -p ${REPORT_DIR}

ARGS=" --html-report ${REPORT_DIR}"

$PROGRAM $ARGS $MODULE
