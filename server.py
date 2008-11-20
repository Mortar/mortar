from wsgiref.simple_server import make_server
from mortar.application import app
httpd = make_server('', 8000, app)
print "Serving HTTP on port 8000..."
# Respond to requests until process is killed
httpd.serve_forever()
