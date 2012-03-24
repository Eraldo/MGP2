'''
Created on Mar 23, 2012

@author: Eraldo Helal
'''
import Pyro4

items = Pyro4.Proxy("PYRONAME:items")       # use name server object lookup uri shortcut

def show_menu():
    '''
    Display a menu with choices for user.
    '''
    options = ["menu", "show items", "add item", "delete item", "save items", "load items", "exit"]
    print("--- MENU ---")
    for i, v in enumerate(options):
        print(i+1, ": ", v)

def main():
    '''
    Start client command line interface to server object. 
    '''
    show_menu()
    while True:
        choice = input("\nChose an action: ")
        if choice == "1" or choice.find("menu") != -1:
            show_menu()
        elif choice == "2" or choice.find("show") != -1 or choice.find("list") != -1: 
            for i, v in enumerate(items.get()):
                print(i+1, ": ", v)
        elif choice == "3" or choice.find("add") != -1:
            item = input("title for item to add: ")
            msg = items.add(item)
            print(msg)
        elif choice == "4" or choice.find("delete") != -1:
            item = input("index or full name of item to delete: ")
            index = None
            try:
                index = int(item)-1
            except ValueError:
                try:
                    index = items.get().index(item)
                except ValueError:
                    msg = "No such item found. (enter index or full title)"
            if index:
                msg = items.delete(index)
            print(msg)
        elif choice == "5" or choice.find("save") != -1:
            print(items.save())
        elif choice == "6" or choice.find("load") != -1:
            print(items.load())
        elif choice == "7" or choice.find("exit") != -1:
            break
        else:
            print("Invalid Option!")

def test_client():
    '''
    Testing automated user input.
    '''
    print("\nTesting: test")
    print(items.test())
    print("\nTesting: add")
    print(items.add("task 5"))
    print("\nTesting: get")
    print(items.get())
    print("\nTesting: show")
    print(items.show())

if __name__ == "__main__":
    main()