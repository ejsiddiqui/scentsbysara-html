"""Simple HTTP server for serving HTML mockup files."""

import http.server
import threading
import socket
import os


class MockupServer:
    """Serves the /html/ directory over HTTP for Playwright to access."""

    def __init__(self, html_dir: str, port: int = 8080):
        self.html_dir = os.path.abspath(html_dir)
        self.port = port
        self._server = None
        self._thread = None

    @staticmethod
    def _find_free_port(preferred: int, max_attempts: int = 20) -> int:
        """Return the preferred port if free, else find the next free port."""
        for offset in range(max_attempts):
            port = preferred + offset
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    continue
        raise RuntimeError(
            f"Could not find a free port starting from {preferred} "
            f"after {max_attempts} attempts."
        )

    def start(self):
        """Start the server in a background thread. Auto-selects a free port if preferred is busy."""
        self.port = self._find_free_port(self.port)

        handler = http.server.SimpleHTTPRequestHandler
        self._server = http.server.HTTPServer(
            ("127.0.0.1", self.port),
            lambda *args, **kwargs: handler(*args, directory=self.html_dir, **kwargs),
        )
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        print(f"  Mockup server started at http://127.0.0.1:{self.port} (serving {self.html_dir})")

    def stop(self):
        """Shut down the server."""
        if self._server:
            self._server.shutdown()
            self._thread.join(timeout=5)
            self._server = None
            self._thread = None

    @property
    def base_url(self):
        return f"http://127.0.0.1:{self.port}"


if __name__ == "__main__":
    import sys
    html_dir = sys.argv[1] if len(sys.argv) > 1 else "html"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    server = MockupServer(html_dir, port)
    server.start()
    print(f"Serving {html_dir} at http://127.0.0.1:{port} — press Ctrl+C to stop")
    try:
        server._thread.join()
    except KeyboardInterrupt:
        server.stop()
