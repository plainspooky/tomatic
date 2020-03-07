#!/usr/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1
[[ ! -n $MODULE ]] && echo "Set 'MODULE' variable first!" && exit 1

PROGRAM="pdoc3"
REQUIREMENTS="requirements-${PROGRAM}.txt"

ROOT_DIR="$(dirname "$(readlink -f "$0")")"

[[ ! $( which $PROGRAM ) ]] && pip3 install $PROGRAM

REPORT_DIR="./reports"
mkdir -p "$REPORT_DIR/$MODULE"

TEMPLATE_DIR="$ROOT_DIR/template.d"

cp "$TEMPLATE_DIR/*.{jpg,png}" "$REPORT_DIR/$MODULE"

ARGS="--force --config show_source_code=False --html --template-dir $TEMPLATE_DIR --output-dir $REPORT_DIR"

${PROGRAM} ${ARGS} ${MODULE}
