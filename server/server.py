'''
Created on Mar 23, 2012

@author: eraldo
'''

import Pyro4, pickle

class items(object):    
    items = ['task 1', 'task 2', 'task 3']
    filename = "items"
    def show(self):
        "Output list of items on server."
        for i, v in enumerate(self.items):
            print(i, ": ", v)
        #print(*self.items, sep='\n')
    def get(self):
        "returns the list of items from server"
        return self.items
    def add(self, item):
        "add a new item to the list of items on server"
        self.items.append(item)
        msg = "added: {0}".format(item)
        print(msg)
        return msg
    def delete(self, index):
        "delete item with given index from the list of items on server"
        if index >= 0 and index < self.items.__len__():
            self.items.pop(index)
            msg = "deleted: {0}".format(index)
            print(msg)
        else:
            msg = "Invalid item number."
        return msg
    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.items, file)
        msg = "saved items to: '{0}'".format(self.filename)
        print(msg)
        return msg
    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                self.items = pickle.load(file)
            msg = "loaded items from: '{0}'".format(self.filename)
        except EOFError:
            msg = "Nothing to load."
        print(msg)
        return msg
    def test(self):
        return "Test is working."

# create a new items list instance
items = items()

daemon = Pyro4.Daemon()         # make a Pyro daemon
ns = Pyro4.locateNS()           # find the name server
uri = daemon.register(items)    # register the items list as a Pyro object
ns.register("items", uri)       # register the object with a name in the name server

print("Ready.")
items.show()
daemon.requestLoop()            # start the event loop of the server to wait for calls