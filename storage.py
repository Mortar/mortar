# blah
storages = {}

def addStorage(name,storage):
    global storages
    storages[name]=storage

def getStorage(name):
    return storages[name]
