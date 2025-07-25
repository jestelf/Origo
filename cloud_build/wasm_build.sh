#!/usr/bin/env bash
set -e
DIR="$(dirname "$0")/.."
python "$DIR/build/build_game.py" --platform wasm "$@"
