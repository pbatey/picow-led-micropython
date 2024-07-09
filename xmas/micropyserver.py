"""
MicroPyServer is a simple HTTP server for MicroPython projects.

@see https://github.com/troublegum/micropyserver

The MIT License

Copyright (c) 2019 troublegum. https://github.com/troublegum/micropyserver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

---
Changes made by pbatey on 2023-12-19:

1. Route handlers are now passed Request and Response objects to make
JSON handling easy.
2. Add static file handler

@example
from micropyserver import MicroPyServer, static_files
server = MicroPyServer()
server.add_route("/api/v1/version", lambda req,res: res.send({"version":"1.0.0"}))
server.add_route("/images", static_files("images"))
server.on_not_found(static_files(basedir="public"))
server.start()
"""
import re
import socket
import sys
import io
import json
import os


class MicroPyServer(object):

    def __init__(self, host="0.0.0.0", ip='localhost', port=80):
        """ Constructor """
        self._host = host
        self._ip = ip
        self._port = port
        self._routes = []
        self._connect = None
        self._on_request_handler = None
        self._on_not_found_handler = None
        self._on_error_handler = None
        self._sock = None
        self._allowed_content_types = {
            '.gif': 'image/gif',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.svg': 'image/svg+xml',
            '.txt': 'text/plain',
            '.htm': 'text/html',
            '.html': 'text/html',
            '.json': 'application/json',
        }

    def start(self):
        """ Start server """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen(1)
        port = ":" + self._port if self._port != 80 else ""
        print("listening at http://" + self._ip + port)
        while True:
            if self._sock is None:
                break
            try:
                self._connect, address = self._sock.accept()
                raw = self._get_request()
                req = Request(raw, address)
                res = Response(self)
                if len(raw) == 0:
                    self._connect.close()
                    continue
                if self._on_request_handler:
                    if not self._on_request_handler(req, res):
                        continue
                route = self.find_route(req)
                if route:
                    route["handler"](req, res)
                else:
                    self._route_not_found(req, res)
            except Exception as e:
                sys.print_exception(e)
                self._internal_error(e)
            finally:
                self._connect.close()

    def stop(self):
        """ Stop the server """
        self._connect.close()
        self._sock.close()
        self._sock = None
        print("Server stop")

    def add_route(self, path, handler, method="GET"):
        """ Add new route  """
        self._routes.append(
            {"path": path, "handler": handler, "method": method})

    def send(self, data):
        """ Send data to client """
        if self._connect is None:
            raise Exception("Can't send response, no connection instance")
        self._connect.sendall(data.encode())

    def find_route(self, req:'Request'):
        """ Find route """
        method = req.method
        path = req.path
        for route in self._routes:
            if method != route["method"]:
                continue
            if path == route["path"]:
                return route
            else:
                match = re.search("^" + route["path"] + "$", path)
                if match:
                    print(method, path, route["path"])
                    return route

    def _get_request(self, buffer_length=4096):
        """ Return request body """
        return str(self._connect.recv(buffer_length), "utf8")

    def on_request(self, handler):
        """ Set request handler """
        self._on_request_handler = handler

    def on_not_found(self, handler):
        """ Set not found handler """
        self._on_not_found_handler = handler

    def on_error(self, handler):
        """ Set error handler """
        self._on_error_handler = handler

    def _route_not_found(self, req:'Request', res:'Response'):
        """ Route not found handler """
        if self._on_not_found_handler:
            self._on_not_found_handler(req, res)
        else:
            """ Default not found handler """
            res.error(code=404)

    def _internal_error(self, error):
        """ Internal error handler """
        if self._on_error_handler:
            self._on_error_handler(error)
        else:
            """ Default internal error handler """
            if "print_exception" in dir(sys):
                output = io.StringIO()
                sys.print_exception(error, output)
                str_error = output.getvalue()
                output.close()
            else:
                str_error = str(error)
            self.send("HTTP/1.0 500 Internal Server Error\r\n")
            self.send("Content-Type: text/plain\r\n\r\n")
            self.send("Error: " + str_error)
            print(str_error)

""" HTTP response codes """
HTTP_CODES = {
    100: 'Continue',
    101: 'Switching protocols',
    102: 'Processing',
    200: 'Ok',
    201: 'Created',
    202: 'Accepted',
    203: 'Non authoritative information',
    204: 'No content',
    205: 'Reset content',
    206: 'Partial content',
    207: 'Multi status',
    208: 'Already reported',
    226: 'Im used',
    300: 'Multiple choices',
    301: 'Moved permanently',
    302: 'Found',
    303: 'See other',
    304: 'Not modified',
    305: 'Use proxy',
    307: 'Temporary redirect',
    308: 'Permanent redirect',
    400: 'Bad request',
    401: 'Unauthorized',
    402: 'Payment required',
    403: 'Forbidden',
    404: 'Not found',
    405: 'Method not allowed',
    406: 'Not acceptable',
    407: 'Proxy authentication required',
    408: 'Request timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length required',
    412: 'Precondition failed',
    413: 'Request entity too large',
    414: 'Request uri too long',
    415: 'Unsupported media type',
    416: 'Request range not satisfiable',
    417: 'Expectation failed',
    418: 'I am a teapot',
    422: 'Unprocessable entity',
    423: 'Locked',
    424: 'Failed dependency',
    426: 'Upgrade required',
    428: 'Precondition required',
    429: 'Too many requests',
    431: 'Request header fields too large',
    500: 'Internal server error',
    501: 'Not implemented',
    502: 'Bad gateway',
    503: 'Service unavailable',
    504: 'Gateway timeout',
    505: 'Http version not supported',
    506: 'Variant also negotiates',
    507: 'Insufficient storage',
    508: 'Loop detected',
    510: 'Not extended',
    511: 'Network authentication required',
}

class Request(object):
    def __init__(self, raw:str, address):
        """ Constructor """
        self._raw = raw
        self.address = address
        self._line = raw.split("\r\n",1)[0]
        print(self._line)
        match = re.search(r'^([A-Z]+)\s+([^?\s]+)((?:[?&][^&\s]*)*)\s+(HTTP/.*)', self._line)
        if match is not None:
            self.method = match.group(1)
            self.path = match.group(2)
            self.query = match.group(3)
            self.proto = match.group(4)

    def query_params(self):
        if self.query_params is not None:
            return self.query_params
        else:
            pairs = self.query.lstrip('?').split('&')
            self.query_params = {}
            for pair in pairs:
                param = pair.split("=",1)
                key = param[0]
                value = param[1]
                self.query_params[key] = value
        return self.query_params

    def json(self):
        print('raw', self._raw)
        match = re.search("\r\n\r\n(.+)", self._raw)
        if match is None:
            print('no match for body')
            return None
        try:
            j = json.loads(match.group(1))
            return j
        except:
            print('json failure')
            return None

class Response(object):
    def __init__(self, server:MicroPyServer):
        """ Constructor """
        self.code = None
        self._server = server
        self.extend_headers = None

    def status(self, code):
        self.code = code
        return self

    def header(self, key, value):
        if self.extend_headers is None:
            self.extend_headers = {}
        self.extend_headers[key] = value
        return self

    def send(self, body=None, code=None, content_type='text/html'):
        code = code if code is not None else self.code if self.code is not None else 200 if body is not None else 201
        if isinstance(body, dict) or isinstance(body, list):
          content_type = "application/json"
          body = json.dumps(body)
        self._server.send("HTTP/1.0 " + str(code) + " " + HTTP_CODES.get(code) + "\r\n")
        self._server.send("Content type:" + content_type + "\r\n")
        if self.extend_headers is not None:
          for header in self.extend_headers:
            self._server.send(header + "\r\n")
        self._server.send("\r\n")
        if body is not None:
          self._server.send(body)
    
    def send_file(self, fname, code=None):
        try:
            ext = fname[fname.rfind('.'):]
            content_type = self._server._allowed_content_types[ext]
            with open(fname) as f:
                self.send(f.read(), code, content_type)
        except:
            print('File not found:', fname)
            return False
        
    def error(self, msg=None, code=None):
        code = code if code is not None else self.code if self.code is not None else 500
        msg = msg if msg is not None else str(code) + " " + HTTP_CODES.get(code)
        self.status(code).send("<html><body><code>" + msg + "<code><body><html>")

def _resolve(path):
    l = []
    p = path.split('/')
    for p in p:
        l.pop() if p == '..' else l.append(p)
    return '/'.join(l)

def _safe_path(basedir:str, fname:str, index="index.html"):
    if basedir[0] != '/':
      basedir = os.getcwd() + basedir
    path = _resolve(basedir.rstrip('/') + '/' + fname.lstrip('/'))
    if not path.startswith(basedir):
        return None
    try:
        if index is not None and index in os.listdir(path):
          return path + index
    except:
        pass
    return path


def static_files(basedir="public"):
    def handler(req, res):
        if req.method != 'GET':
            return res.error(code=405)
        path = _safe_path(basedir, req.path)
        if path == False:
            return res.error(code=404)
        res.send_file(path)
    return handler
