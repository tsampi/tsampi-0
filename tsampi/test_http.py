import tsampi
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
import cgitb
cgitb.enable(format='text')


class StringHTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message



request_text = r'''POST /123 HTTP/1.0
Content-Length: 8
Content-Type: application/x-www-form-urlencoded

val=2300
'''

request = StringHTTPRequest(request_text)

print request.error_code       # None  (check this first)
print request.command          # "GET"
print request.path             # "/who/ken/trust.html"
print request.request_version  # "HTTP/1.1"
print len(request.headers)     # 3
print request.headers.keys()   # ['accept-charset', 'host', 'accept']
#print request.headers['content-type']  # "cm.bell-labs.com"
content_len = int(request.headers.getheader('content-length', 0))
post_body = request.rfile.read(content_len)

print post_body



import cgi
from StringIO import StringIO as IO

parsed = cgi.FieldStorage(
    IO(post_body.encode('utf-8')),
    headers={'content-type': request.headers['content-type']},
    environ={'REQUEST_METHOD': request.command })



import cStringIO
from wsgiref import simple_server, util

from werkzeug.formparser import parse_form_data

input_string = """POST / HTTP/1.1
Host: example.com
User-Agent: curl/7.43.0
Accept: */*
Content-Type: multipart/form-data; boundary=---------------------------735323031399963166993862150
Content-Length: 834

-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="text1"

text default
-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="text2"

aωb
-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="file1"; filename="a.txt"
Content-Type: text/plain

Content of a.txt.

-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="file2"; filename="a.html"
Content-Type: text/html

<!DOCTYPE html><title>Content of a.html.</title>

-----------------------------735323031399963166993862150
Content-Disposition: form-data; name="file3"; filename="binary"
Content-Type: application/octet-stream

aωb
-----------------------------735323031399963166993862150--
"""

class FakeHandler(simple_server.WSGIRequestHandler):
    def __init__(self, rfile):
        self.rfile = rfile
        self.wfile = cStringIO.StringIO() # for error msgs
        self.server = self
        self.base_environ = {}
        self.client_address = ['?', 80]
        self.raw_requestline = self.rfile.readline()
        self.parse_request()

    def getenv(self):
        env = self.get_environ()
        util.setup_testing_defaults(env)
        env['wsgi.input'] = self.rfile
        return env









#handler = FakeHandler(rfile=cStringIO.StringIO(input_string))
#environ = handler.getenv()
import werkzeug_raw
environ = werkzeug_raw.environ(input_string)

print environ

from werkzeug.wrappers import Request
request = Request(environ)

print 'request' , '-' * 10
print request.__dict__
print 'request' , '-' * 10
'''
import werkzeug_raw
environ = werkzeug_raw.environ('GET /foo/bar?tequila=42 HTTP/1.1')
environ = werkzeug_raw.environ(request_text)

print wsgi_env

request = Request(environ)
print 'request' , '-' * 10
print request.__dict__
print 'request' , '-' * 10
stream, form, files =  parse_form_data(wsgi_env)
print stream.read()
print 'request' , '-' * 10
'''
