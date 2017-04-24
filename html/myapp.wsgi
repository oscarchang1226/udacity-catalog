#def application(environ, start_response):
#    status = '200 OK'
#    output = 'Hello World!'
#
#    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#    start_response(status, response_headers)
#
#    return [output]

import sys, os, logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html')
os.chdir('/var/www/html')
from application import app as application
application.secret_key = '\x1exog\xf0;\x0c\x1f\xf7R\xaa7/\x1c\x08i\x9d\xca\xdf\xf63\x7f\xf1%'
