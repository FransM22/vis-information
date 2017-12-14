#!/usr/bin/env python3

# This script provides a simple server handling static files. Files inside the
# www/ directory can be accessed by a web browser on the port specified.
# 
# Run with
# > python3 ./runserver.py
#
import http.server
import socketserver
import os

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

os.chdir('www/')
with socketserver.TCPServer(("", PORT), Handler) as httpd:
  print("Server can be accessed by a browser on http://localhost:{}/\nClose with Ctrl+C.".format(PORT))
  httpd.serve_forever()
