"""Assemble the playable development app using the official universal Godot binary."""
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
engine = Path(sys.argv[1])
app = root / "build" / "Highway Phantom.app"
shutil.copytree(engine, app, dirs_exist_ok=True)
contents = app / "Contents"
shutil.copy2(root / "build" / "HighwayPhantom.pck", contents / "Resources" / "HighwayPhantom.pck")
shutil.copytree(root / "licenses", contents / "Resources" / "licenses", dirs_exist_ok=True)
shutil.copy2(root / "build" / "Phantom.icns", contents / "Resources" / "Phantom.icns")
info_path = contents / "Info.plist"
with info_path.open("rb") as handle:
    info = plistlib.load(handle)
info.update(CFBundleName="Highway Phantom", CFBundleDisplayName="Highway Phantom", CFBundleIdentifier="com.highwayphantom.prototype", CFBundleExecutable="HighwayPhantom", CFBundleShortVersionString="0.1.0", CFBundleVersion="1")
info["CFBundleIconFile"] = "Phantom.icns"
info.pop("CFBundleDocumentTypes", None)
with info_path.open("wb") as handle:
    plistlib.dump(info, handle)
launcher = contents / "MacOS" / "HighwayPhantom"
launcher.write_text('''#!/bin/sh
PHANTOM_CONTENTS="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
exec "$PHANTOM_CONTENTS/MacOS/Godot" --main-pack "$PHANTOM_CONTENTS/Resources/HighwayPhantom.pck" "$@"
''')
launcher.chmod(0o755)
for name, options in [("Play.command", ""), ("Open in Godot.command", "--editor")]:
    script = root / name
    script.write_text('''#!/bin/sh
PHANTOM_PROJECT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$PHANTOM_PROJECT/build/Highway Phantom.app/Contents/MacOS/Godot" ''' + options + ''' --path "$PHANTOM_PROJECT"
''')
    script.chmod(0o755)
subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)], check=True)
print("Packaged", app)
