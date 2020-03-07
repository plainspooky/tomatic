#!/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1
[[ ! -n $MODULE ]] && echo "Set 'MODULE' variable first!" && exit 1

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

PROGRAM="pytest"
REQUIREMENTS="requirements-${PROGRAM}.txt"

run_steps(){
    #
    #   run each file with execution attribute in a directory
    #
    local step_dir="$ROOT_DIR/${1}/*"

    [[ ! -d $step_dir ]] && return 0

    for step in $step_dir; do
        [[ -x $step ]] && $step
    done
}

[[ ! $( which $PROGRAM ) ]] && pip3 install -r $REQUIREMENTS

ARGS="-vv"
TEST_FILES="${MODULE}/tests.py"

[[ $COV ]] && COVERAGE="--cov=${MODULE} --cov-report=html" || COVERAGE="--cov=${MODULE}"

run_steps "before_tests.d"

$PROGRAM $ARGS $COVERAGE $TEST_FILES

run_steps "after_tests.d"
