"""mahi - a minimal Python backend using only the standard library."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

TODOS = []


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/":
            self._send(200, {"app": "mahi", "status": "ok"})
        elif self.path == "/health":
            self._send(200, {"healthy": True})
        elif self.path == "/todos":
            self._send(200, TODOS)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/todos":
            return self._send(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
            title = str(payload["title"]).strip()
            if not title:
                raise ValueError
        except (ValueError, KeyError, json.JSONDecodeError):
            return self._send(400, {"error": "'title' is required"})
        todo = {"id": len(TODOS) + 1, "title": title}
        TODOS.append(todo)
        self._send(201, todo)


if __name__ == "__main__":
    print("mahi running on http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
