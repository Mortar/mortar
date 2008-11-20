# Copyright (c) 2008 Simplistix Ltd
# See license.txt for license details.

# blah
storages = {}

def addStorage(name,storage):
    global storages
    storages[name]=storage

def getStorage(name):
    return storages[name]
