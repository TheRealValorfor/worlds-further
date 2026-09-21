#!/usr/bin/env bash
# macOS / Linux / Git Bash wrapper around the cross-platform Python script.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$DIR/apply-to-instance.py" "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python "$DIR/apply-to-instance.py" "$@"
fi
echo "Python 3 is required. Install it from https://www.python.org/downloads/ then retry." >&2
exit 1
