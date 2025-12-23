#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 -m venv "$ROOT/.venv" >/dev/null 2>&1 || true
source "$ROOT/.venv/bin/activate"
pip -q install -r "$ROOT/scripts/requirements.txt"
python "$ROOT/scripts/bibtex_to_yaml.py"
