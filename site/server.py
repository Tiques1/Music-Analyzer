from http.server import BaseHTTPRequestHandler, HTTPServer

# python -m http.server [port]
with open('static/html/slider.html', 'rb') as file:
    slider_html = file.read()
with open('static/css/slider.css', 'rb') as file:
    slider_css = file.read()
with open('static/js/slider.js', 'rb') as file:
    slider_js = file.read()


class CustomRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.html()
            elif self.path == '/static/css/slider.css':
                self.css()
            elif self.path == '/static/js/slider.js':
                self.js()
            else:
                self.send_response(404)
                self.end_headers()
                return

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(slider_html)

    def css(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/css; charset=utf-8')
        self.end_headers()
        self.wfile.write(slider_css)

    def js(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript; charset=utf-8')
        self.end_headers()
        self.wfile.write(slider_js)


def run(server_class=HTTPServer, handler_class=CustomRequestHandler, port=8080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server started on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
