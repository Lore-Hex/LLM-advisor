"""Loopback-only review harness for the real public advisor MCP endpoint.

This is a developer walkthrough, not a mock ChatGPT UI. No credentials, cookies
or user data are forwarded. Set --local to exercise an isolated QR test app.
"""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = "https://trustedrouter.com/mcp/advisor"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8176)
    parser.add_argument("--local", action="store_true")
    args = parser.parse_args()
    client = None
    if args.local:
        import os

        os.environ["TR_STORAGE_BACKEND"] = "memory"
        from fastapi.testclient import TestClient
        from trusted_router.config import Settings
        from trusted_router.main import create_app

        client = TestClient(create_app(Settings(environment="test", storage_backend="memory", service_surface="public")))

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def respond(self, body, status=200, content_type="application/json"):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            paths = {
                "/": (ROOT / "submission/review/demo.html", "text/html; charset=utf-8"),
                "/logo.svg": (ROOT / "submission/packages/trustedrouter-model-advisor/assets/trustedrouter.svg", "image/svg+xml"),
            }
            if self.path == "/mode":
                self.respond(json.dumps({"endpoint": "local test application" if client else ENDPOINT}).encode())
                return
            if self.path not in paths:
                self.respond(b"{}", 404)
                return
            path, content_type = paths[self.path]
            self.respond(path.read_bytes(), content_type=content_type)

        def do_POST(self):
            if self.path != "/call" or int(self.headers.get("Content-Length", "0")) > 4096:
                self.respond(b"{}", 400)
                return
            payload = self.rfile.read(int(self.headers.get("Content-Length", "0")))
            try:
                parsed = json.loads(payload)
                if parsed.get("method") not in {"initialize", "tools/list", "tools/call"}:
                    raise ValueError("Unsupported review request")
                if client:
                    response = client.post("/mcp/advisor", json=parsed)
                    self.respond(response.content, response.status_code)
                else:
                    request = Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
                    with urlopen(request, timeout=30) as response:
                        self.respond(response.read())
            except (OSError, ValueError, RuntimeError) as exc:
                self.respond(json.dumps({"error": {"message": type(exc).__name__}}).encode(), 502)

    print(f"Review harness: http://127.0.0.1:{args.port}; backend={'local test' if client else ENDPOINT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
