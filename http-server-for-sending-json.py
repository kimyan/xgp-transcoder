import stomp
import time

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json


class MyListener(stomp.ConnectionListener):

    messages = []

    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        self.messages.append(message)
        print('received a message "%s"' % message)


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        conn = stomp.Connection()

        listener = MyListener()
        conn.set_listener('listener', listener)
        conn.start()
        conn.connect('admin', 'admin', wait=True)
        conn.subscribe(destination='/queue/udpstring', id='1')

        wait_count = 0

        while wait_count < 3:
            if len(listener.messages) == 0:
                time.sleep(1)
                wait_count = wait_count + 1
            else:
                parsed_path = urlparse(self.path)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(json.dumps({
                    'method': self.command,
                    'path': self.path,
                    'real_path': parsed_path.query,
                    'query': parsed_path.query,
                    'request_version': self.request_version,
                    'protocol_version': self.protocol_version,
                    'body': {
                        'has_messages': True,
                        'messages': listener.messages
                    }
                }).encode())
                listener.messages.clear()
                conn.disconnect()
                return

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version,
            'body': {
                'has_messages': False,
                'messages': []
            }
        }).encode())
        conn.disconnect()
        return


if __name__ == '__main__':
    http_ip_address = 'localhost'
    http_port = 8001

    server = HTTPServer((http_ip_address, http_port), RequestHandler)
    print('Starting server at http://{0}:{1}'.format(http_ip_address, http_port))
    server.serve_forever()