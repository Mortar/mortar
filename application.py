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
    
