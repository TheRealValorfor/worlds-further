#!/bin/bash
# Double-click in macOS Finder, or run from Terminal.
cd "$(dirname "$0")" || exit 1
chmod +x start.sh install_java.sh 2>/dev/null
exec bash ./start.sh "$@"
