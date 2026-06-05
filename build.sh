#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PYTHON_BIN="${PYTHON_BIN:-}"
if [ -z "$PYTHON_BIN" ]; then
  if command -v python3 >/dev/null 2>&1; then PYTHON_BIN=python3;
  elif command -v python >/dev/null 2>&1; then PYTHON_BIN=python;
  else echo "ERROR: Python 3 is required but was not found on PATH." >&2; exit 1; fi
fi

# Always validate the packaged CSV/SVG artifacts first. This path has no third-party Python dependencies.
"$PYTHON_BIN" scripts/check_reproducibility.py
"$PYTHON_BIN" scripts/generate_scientific_plots.py

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode RNNematode-Micropublication.tex
  latexmk -c RNNematode-Micropublication.tex >/dev/null 2>&1 || true
  cd report
  latexmk -pdf -interaction=nonstopmode RNNematode-TechnicalReport.tex
  latexmk -c RNNematode-TechnicalReport.tex >/dev/null 2>&1 || true
else
  echo "latexmk not found; skipped PDF rebuild. Existing PDFs remain in the package."
fi
