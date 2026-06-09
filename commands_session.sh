#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then PYTHON_BIN=python3;
  elif command -v python >/dev/null 2>&1; then PYTHON_BIN=python;
  else echo "ERROR: Python 3 is required but was not found on PATH." >&2; exit 1; fi
fi

# Lightweight reviewer path: validate packaged result artifacts.
"$PYTHON_BIN" scripts/check_reproducibility.py
"$PYTHON_BIN" scripts/generate_scientific_plots.py

# Optional: execute notebooks if Jupyter is installed.
if command -v jupyter >/dev/null 2>&1; then
  for nb in Codes/*.ipynb; do
    jupyter nbconvert --to notebook --execute --inplace "$nb"
  done
else
  echo "jupyter not found; skipped notebook execution. Run 'pip install -r requirements.txt' to enable it."
fi
