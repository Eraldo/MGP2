'''
Created on Mar 23, 2012

@author: Eraldo Helal
'''

import sys

class App:
    items = None
    menu = None
    
    def get_items_from_server(self):
        import Pyro4
        # use name server object lookup uri shortcut
        self.items = Pyro4.Proxy("PYRONAME:items")
        
    def exit_action(self, param):
        print("Program has ended.")
        sys.exit()
    
    def menu_action(self, param):
        if self.menu:
            self.menu.display()
    
    def list_action(self, param):
        items = self.items.get()
        if items.__len__() == 0:
            print("The list is empty.")
        else:
            if param and param != "all": # assuming specific item
                item = param
                index = None
                try:
                    index = int(item)-1
                except ValueError:
                    try:
                        index = items.index(item)
                    except ValueError:
                        print("No such item found. (enter index or full title)")
                if index is not None:
                    if  index in range(0,items.__len__()):
                        print(index+1, ": ", items[index])
                    else:
                        print("No item found for index:", index+1)
            else: # show all items
                for i, v in enumerate(items):
                    print(i+1, ": ", v)

    
    def add_action(self, param):
        if param:
            item = param
        else:
            item = input("title for item to add: ").strip()
        msg = self.items.add(item)
        print(msg)
    
    def delete_action(self, param):
        if param:
            if param == "all":
                number_of_items = self.items.__len__() 
                for _ in range(number_of_items):
                    self.items.delete(0)
                print("Deleted all", number_of_items, "items.")
                return
            item = param
        else:
            item = input("index or full name of item to delete: ")
        index = None
        msg = ""
        
        try:
            index = int(item)-1
        except ValueError:
            try:
                index = self.items.get().index(item)
            except ValueError:
                msg = "No such item found. (enter index or full title)"
        if index is not None:
            msg = self.items.delete(index)
        print(msg)
    
    def save_action(self, param):
        msg = self.items.save()
        print(msg)
    
    def load_action(self, param):
        msg = self.items.load()
        print(msg)
    
    def help_action(self, param):
        self.menu.display_help(param)
    
    def init_menu(self):
        self.menu = Menu()
        
        menu_items = [["exit", "Terminate program.", "'exit|<alias>'", 
                       self.exit_action, ["0", "quit"]], 
                      ["menu", "Display the main menu.", "'menu|<alias>'", 
                       self.menu_action, ["1", "m"]], 
                      ["list", "Display the list of items.", "'list|<alias>'", 
                       self.list_action, ["2", "ls"]], 
                      ["add", "Add an item to the list.", 
                       "'add|<alias> [item]'", 
                       self.add_action, ["3", "a"]], 
                      ["delete", 
                       "Delete an item from the list.", 
                       "'delete|<alias> [item|all]'", 
                       self.delete_action, ["4", "d", "del"]], 
                      ["save", "Save the list.", "'save|<alias>'", 
                       self.save_action, ["5", "sa"]], 
                      ["load", "Load the list.", "'load|<alias>'", 
                       self.load_action, ["6", "lo"]], 
                      ["help", 
                       "Show help information.", "'help|<alias> [<topic>|all]'", 
                       self.help_action, ["7", "h"]], 
                      ]
        
        for item in menu_items:
            self.menu.add(MenuItem(*item))
    
    def start(self):
        self.init_menu()
        self.menu.display()
        
        while True:
            user_input = input("\nChose an action: ").strip()
            # get first word
            choice = user_input.split(' ', 1)[0]
            # get all but first word
            param = user_input[choice.__len__():].strip()
            
            found = False
            for item in self.menu.menu_items:
                if (choice == item.name) or (choice in item.aliases):
                    found = True
#                    print(item.name, item.aliases, choice, "-->", param)
                    item.action(param)
            if not found:
                print("Invalid menu option!")
                self.menu.display()


class Menu:
    
    menu_items = []
    
    def __init__(self, menu_items=[]):
        self.menu_items = menu_items
    
    def add(self, item):
        self.menu_items.append(item)
    
    def display(self):
        print("--- MENU ---")
        for index, item in enumerate(self.menu_items):
            print(index, ":", item.name)
    
    def display_help(self, topic):
#        self.display()
        print("--- MENU HELP ---")
        if topic:
            found = False
            for item in self.menu_items:
                if topic in ["all", item.name] or (topic in item.aliases):
                    found = True
                    print(item.name, ":\t", item.help_text, 
                          "\n\tsyntax:", item.syntax, 
                          "\n\taliases:", item.aliases, sep='')
            if not found:
                print("Topic", topic, "not found.")
        else:
            for item in self.menu_items:
                print(item.name, ":\t", item.help_text, sep='')
            print("For more information type: 'help <topic>|all'")
                


class MenuItem:
    
    name = ""
    help_text = ""
    syntax = ""
    action = None
    aliases = []
    
    def default_action(self):
        pass
    
    def __init__(self, name="---", help_text="No help provided.", syntax="", 
                 action=None, aliases=[]):
        self.name = name
        self.help_text = help_text
        self.syntax = syntax
        if action:
            self.action = action
        else:
            self.action = self.default_action()
        self.aliases = aliases


def main():
    '''
    Start client command line interface to server object. 
    '''
    
    client = App()
        
#    # debug run
#    client.get_items_from_server()
#    client.start()
    
    try:
        client.get_items_from_server()
        client.start()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit()

def test_client(self):
    '''
    Testing automated user input.
    '''
    print("\nTesting: test")
    print(self.items.test())
    print("\nTesting: add")
    print(self.items.add("task 5"))
    print("\nTesting: get")
    print(self.items.get())
    print("\nTesting: show")
    print(self.items.show())

if __name__ == "__main__":
    main()