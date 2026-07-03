import json
import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(__file__))

from app import lambda_handler


def build_lambda_event(body: str, headers: dict | None = None, method: str = "POST") -> dict:
    """Build an event object compatible with the Lambda handler from an incoming request."""
    return {
        "httpMethod": method,
        "headers": headers or {},
        "body": body,
    }


class MoviePickerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._send_response(200, "", {"Access-Control-Allow-Origin": "*"})

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        event = {"httpMethod": "GET", "path": path}
        response = lambda_handler(event, None)
        self._send_response(
            response.get("statusCode", 200),
            response.get("body", ""),
            response.get("headers", {}),
        )

    def do_POST(self):
        if self.path != "/movie":
            self._send_response(404, json.dumps({"error": "not_found"}), {"Content-Type": "application/json"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        event = build_lambda_event(body, {"Content-Type": self.headers.get("Content-Type", "application/json")})
        response = lambda_handler(event, None)
        self._send_response(
            response.get("statusCode", 200),
            response.get("body", "{}"),
            response.get("headers", {}),
        )

    def log_message(self, format, *args):
        return

    def _send_response(self, status_code: int, body: str, headers: dict | None = None):
        response_headers = headers or {}
        if "Content-Type" not in response_headers and body:
            response_headers["Content-Type"] = "application/json"
        response_headers.setdefault("Access-Control-Allow-Origin", "*")
        response_headers.setdefault("Access-Control-Allow-Headers", "Content-Type")
        response_headers.setdefault("Access-Control-Allow-Methods", "OPTIONS,POST")

        self.send_response(status_code)
        for key, value in response_headers.items():
            self.send_header(key, value)
        self.end_headers()
        if body:
            self.wfile.write(body.encode("utf-8"))


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8000), MoviePickerHandler)
    print("Local movie API listening on http://127.0.0.1:8000/movie")
    server.serve_forever()


if __name__ == "__main__":
    main()
