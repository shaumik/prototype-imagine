#!/bin/sh
PHANTOM_PROJECT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$PHANTOM_PROJECT/tools/serve_web.py" --open
