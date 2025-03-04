import http.server
import socketserver
import urllib.request

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        url = self.path[1:]  # Remove the leading slash
        if not url:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No target URL specified')
            return

        try:
            with urllib.request.urlopen(url) as response:
                self.send_response(response.status)
                for header in response.getheaders():
                    self.send_header(header[0], header[1])
                self.end_headers()
                self.wfile.write(response.read())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Proxy error: {e}'.encode())

def run(server_class=http.server.HTTPServer, handler_class=Proxy, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Proxy server running on http://localhost:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
