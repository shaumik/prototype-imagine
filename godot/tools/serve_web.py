"""Serve the playable Godot export locally; no third-party packages required."""
import argparse
import errno
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen
import webbrowser

ROOT = Path(__file__).resolve().parents[1]

class GameHandler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, ".wasm": "application/wasm", ".pck": "application/octet-stream"}

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Highway-Phantom", "local-game")
        super().end_headers()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8067)
    parser.add_argument("--open", action="store_true", help="Open the browser when launched by the player")
    args = parser.parse_args()
    directory = ROOT / "build" / "web"
    if not (directory / "index.html").is_file():
        parser.error("Browser build missing. Export the Web preset in Godot first.")
    url = f"http://127.0.0.1:{args.port}"
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(GameHandler, directory=str(directory)))
    except OSError as error:
        if error.errno != errno.EADDRINUSE:
            raise
        try:
            with urlopen(url, timeout=2) as response:
                running = response.headers.get("X-Highway-Phantom") == "local-game"
        except OSError:
            running = False
        if not running:
            parser.error(f"Port {args.port} is already in use by another app; choose a different --port.")
        print(f"Highway Phantom is already ready at {url}", flush=True)
        if args.open:
            webbrowser.open(url)
        return
    print(f"Highway Phantom is ready at {url}", flush=True)
    if args.open:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
