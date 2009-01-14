# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

# NB: not declared as a dependency yet
# from webob import Request, Response

class Root:
    pass

root = Root()

def process_url(path):
    obj = root
    for name in path:
        registrations = queryAdapter(IRegistrations,obj)
        if registrations:
            # xxx
            registrations.register()
        traverser = ITraverser(obj)
        path.pop(0)
        obj = traverser.traverse(obj,path)
        assert IContent.providedBy(obj)
    result = IView(obj)()
    assert isinstance(view,unicode)
    return result.encode('utf-8')
    
class Application:
    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = Response(
            'Hello %s!' % req.params.get('name', 'World'))
        return resp(environ, start_response)

app = Application()
