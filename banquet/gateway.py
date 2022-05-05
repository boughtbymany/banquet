from http.server import BaseHTTPRequestHandler


class BanquetGateway(BaseHTTPRequestHandler):
    def __init__(self, *args, router=None, **kwargs):
        if router is None:
            raise Exception("No router available!")

        self.router = router

        super().__init__(*args, **kwargs)

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _handle_404(self):
        self._set_headers(404)
        self.wfile.write("Not Found.".encode("utf8"))

    def do_GET(self):
        handler, path_params = self.router.resolve("GET", self.path)

        if handler is None:
            self._handle_404()
            return

        self._set_headers()
        response = handler.call({"params": path_params}, {})
        self.wfile.write(str(response).encode("utf8"))

    def do_POST(self):
        handler, path_params = self.router.resolve("POST", self.path)

        if handler is None:
            self._handle_404()
            return

        self._set_headers()
        response = handler.call({"params": path_params}, {})
        self.wfile.write(str(response).encode("utf8"))

    def do_DELETE(self):
        handler, path_params = self.router.resolve("DELETE", self.path)

        if handler is None:
            self._handle_404()
            return

        self._set_headers()
        response = handler.call({"params": path_params}, {})
        self.wfile.write(str(response).encode("utf8"))
