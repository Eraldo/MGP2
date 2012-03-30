'''
Created on Mar 23, 2012

@author: Eraldo Helal
'''

import Pyro4, pickle


class items():    
    '''
    Representing a collection of items.
    '''
    items = ['task 1', 'task 2', 'task 3']
    filename = "items"


    def show(self):
        '''
        Output list of items on server.
        '''
        for i, v in enumerate(self.items):
            print(i, ": ", v)
        #print(*self.items, sep='\n')


    def get(self):
        '''
        Returns the list of items from server.
        '''
        return self.items

    
    def add(self, item):
        '''
        Add a new item to the list of items on server.
        @param item:
        '''
        self.items.append(item)
        msg = "added: {0}".format(item)
        print(msg)
        return msg
    
    
    def delete(self, index):
        '''
        Delete item with given index from the list of items on server.
        @param index:
        '''
        if index >= 0 and index < self.items.__len__():
            item = self.items.pop(index)
            msg = "deleted: #{0}: {1}".format(index+1, item)
            print("deleted: #{0}: {1}".format(index, item))
        else:
            msg = "Invalid item number."
        return msg

    
    def save(self):
        '''
        Save the items collection into a pickled file on server.
        '''
        with open(self.filename, 'wb') as file:
            pickle.dump(self.items, file)
        msg = "saved items to: '{0}'".format(self.filename)
        print(msg)
        return msg
    
    
    def load(self):
        '''
        Load the items collection from a pickled file on server.
        '''
        try:
            with open(self.filename, 'rb') as file:
                self.items = pickle.load(file)
            msg = "loaded items from: '{0}'".format(self.filename)
        except (EOFError, IOError):
            msg = "Nothing to load."
        print(msg)
        return msg


def start_name_server():
    '''
    Start name server in shell.
    '''
    from subprocess import call
    call(["/usr/local/bin/python3", "-m", "Pyro4.naming"])


def start_server(obj, name):
    print("Starting server..")
    daemon = Pyro4.Daemon()         # make a Pyro daemon
    ns = Pyro4.locateNS()           # find the name server
    uri = daemon.register(obj)   # register the items list as a Pyro object
    ns.register(name, uri)          # register the object with a name in the name server
    print("..server started.")
    daemon.requestLoop()            # start the event loop of the server to wait for calls


def main():
    '''
    Setup server and wait for calls.
    (also creates dummy items)
    '''
    # create a new items list instance
    items_obj = items()
    items_obj.show()
#    start_name_server()
    start_server(items_obj, "items")


if __name__ == "__main__":
    main()