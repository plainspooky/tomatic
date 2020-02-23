#!/usr/bin/env bash
[[ ! -n $VIRTUAL_ENV  ]] && echo "not in a virtual environment!" && exit 1

MODULE="tomatic"
PROGRAM="pdoc3"
REQUIREMENT="pdoc3"

ROOT="$(dirname "$(readlink -f "$0")")"

[[ ! $( which $PROGRAM ) ]] && pip3 install $PROGRAM

REPORT_DIR="./reports"
mkdir -p "$REPORT_DIR"

TEMPLATE_DIR="$ROOT/template"

[[ ! -f "$REPORT_DIR/$MODULE/tomatic.png" ]] && cp "$TEMPLATE_DIR/tomatic.png" "$REPORT_DIR/$MODULE"

ARGS="--force --config show_source_code=False --html --template-dir $TEMPLATE_DIR --output-dir $REPORT_DIR"

${PROGRAM} ${ARGS} ${MODULE}
