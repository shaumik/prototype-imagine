#!/bin/sh
PHANTOM_PROJECT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$PHANTOM_PROJECT/build/Highway Phantom.app/Contents/MacOS/Godot"  --path "$PHANTOM_PROJECT"
