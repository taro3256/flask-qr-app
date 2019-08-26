from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import FieldStorage

with open('index.html', mode='r') as f:
    index = f.read()
with open('next.html', mode='r') as f:
    next = f.read()

class HSH(BaseHTTPRequestHandler):

    def do_GET(self):
        global routes
        _url = urlparse(self.path)
        for r in routes:
            if r[0] == _url.path:
                eval('self.' + r[1] + '()')
                break
        else:
            self.error()
        return

    def do_POST(self):
        form = FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST'})
        res = form['textfield'].value
        self.send_response(200)
        self.end_headers()
        html = next.format(
            message = 'you typed: ' + res,
            data = form
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def index(self):
        _url = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        html = index.format(
            title = 'Hello',
            message = 'ようこそ、HTTPServerの世界へ！',
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def next(self):
        _url = urlparse(self.path)
        query = parse_qs(_url.query)
        id = query['id'][0]
        password = query['pass'][0]
        msg = 'id=' + id + ', password=' + password
        self.send_response(200)
        self.end_headers()
        html = next.format(
            data = query,
            message = msg
        )
        self.wfile.write(html.encode('utf-8'))
        return

    def xml(self):
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
        <data>
            <person>
                <name>Taro</name>
                <mail>taro@yamada</mail>
            </person>
            <message>Hello Python!!</message>
        </data>'''
        self.send_response(200)
        self.send_header('Content-Type', 'application/xml; charset=utf-8')
        self.end_headers()
        self.wfile.write(xml.encode('utf-8'))
        return

    def error(self):
        self.send_error(404, "CANNOT ACCESS")
        return

routes = []

def route(path, method):
    routes.append((path, method))

# add routes
route('/', 'index')
route('/index', 'index')
route('/next', 'next')
route('/xml', 'xml')

HTTPServer(('', 8000), HSH).serve_forever()