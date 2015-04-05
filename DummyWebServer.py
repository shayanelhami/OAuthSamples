from http.server import HTTPServer, BaseHTTPRequestHandler
from queue import Queue
from socketserver import ThreadingMixIn
import threading
from urllib.parse import parse_qsl


Messages = Queue()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        info = dict(parse_qsl(self.path[2:]))

        # Twitter (OAuth 1.0a)
        if 'oauth_verifier' in info:
            verifier = info['oauth_verifier']
            print("verifier detected:" + verifier)
            Messages.put(verifier)

        # OAuth 2
        if 'code' in info:
            code = info['code']
            print("code detected:" + code)
            Messages.put(code)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Done, you can now close this window".encode())


class DummyServer:

    def __init__(self, host, port):
        self.settings = (host, port)
        self.server = None

    def start(self):
        print("starting web server")
        self.server = ThreadedHTTPServer(self.settings, MyHandler)
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print("listening on %s:%d" % self.settings)

    def stop(self):
        print("stopping listener")
        self.server.shutdown()
