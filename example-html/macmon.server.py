import os
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer

class CORSStaticHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Normalize path: default to index.html
        if self.path == '/':
            path = 'index.html'
        else:
            path = self.path.lstrip('/')

        file_path = os.path.join(os.path.dirname(__file__), path)

        if os.path.isfile(file_path):
            content_type, _ = mimetypes.guess_type(file_path)
            if content_type is None:
                content_type = 'application/octet-stream'

            with open(file_path, 'rb') as f:
                data = f.read()

            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, CORSStaticHandler)
    print(f'Сервер запущен на http://localhost:{server_address[1]}')
    print('CORS разрешён для всех источников')
    httpd.serve_forever()