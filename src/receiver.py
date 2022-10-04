"""Receives incoming game logs and passes them to
the correct interface"""

import http.server
import socketserver

class learning_http_handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length"))
        data = self.rfile.read(length)
        self.temp_str = data.decode()
        self.send_response(200)
        self.end_headers()
        return self.temp_str

if __name__ == "__main__":
    PORT = 8000
    IP = "localhost"
    HANDLER = learning_http_handler

    with socketserver.TCPServer((IP, PORT), HANDLER) as httpd:
        print(f"Serving at ip {IP} and port {PORT}")
        httpd.serve_forever()
