import numpy as np
import math
import time
from PIL import Image
from urllib.parse import urlparse, parse_qs
import json
from getHands import getHands

from http.server import HTTPServer, BaseHTTPRequestHandler


# Capture object

HOST = 'localhost'
PORT = 5001

#TODO: Rewrite server in flask
## HTTP Server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = json.loads(post_data)
        try:
            letter, conf = getHands(parsed_data['base64Img'].split(',')[-1])
            letter = letter.split('\n')[0].split(' ')[-1]
        except:
            letter = ''
            conf = ''
            print("No Hands Detected")
        res = json.loads(f'{{"letter": "{letter}", "conf": "{conf}"}}')
        
        self._set_response(200)
        self.wfile.write(json.dumps(res).encode('utf-8'))

        post_data = None
        parsed_data = None
        res = None
    
    def _set_response(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
