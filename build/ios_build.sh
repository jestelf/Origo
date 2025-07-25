#!/usr/bin/env bash
set -e
DIR="$(dirname "$0")"
python "$DIR/build_game.py" --platform ios "$@"
