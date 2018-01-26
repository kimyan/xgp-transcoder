#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import socket


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        udp_ip_address = 'localhost'
        udp_port = 3001

        content_len = int(self.headers.getheader('content-length'))
        post_body = self.rfile.read(content_len)
        post_data = json.loads(post_body)

        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto("{0}".format(post_data['evaluation']), (udp_ip_address, udp_port))

        data, addr = client.recvfrom(4096)
        print(data)

        parsed_path = urlparse(self.path)
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            'method': self.command,
            'path': self.path,
            'real_path': parsed_path.query,
            'query': parsed_path.query,
            'request_version': self.request_version,
            'protocol_version': self.protocol_version,
            'body': post_data
        }).encode())
        return


if __name__ == '__main__':
    http_ip_address = 'localhost'
    http_port = 8002

    server = HTTPServer((http_ip_address, http_port), RequestHandler)
    print('Starting server at http://{0}:{1}'.format(http_ip_address, http_port))
    server.serve_forever()