"""Re-export the Godot project for the local browser test page."""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--godot", help="Path to a Godot 4.6+ editor executable")
    parser.add_argument("--template", help="Path to an official single-threaded Web release template zip")
    args = parser.parse_args()
    engine = args.godot or shutil.which("godot") or str(ROOT / "build/Highway Phantom.app/Contents/MacOS/Godot")
    template = ROOT / "build/web-templates/web_release.zip"
    template.parent.mkdir(parents=True, exist_ok=True)
    if args.template:
        shutil.copy2(args.template, template)
    if not template.is_file():
        parser.error("Supply --template with an official web_nothreads_release.zip export template.")
    output = ROOT / "build/web/index.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([engine, "--headless", "--path", str(ROOT), "--editor", "--import", "--quit"], check=True)
    subprocess.run([engine, "--headless", "--path", str(ROOT), "--export-release", "Web", str(output)], check=True)
    print("Browser build ready. Run tools/serve_web.py or double-click Play in Browser.command.")

if __name__ == "__main__":
    main()
