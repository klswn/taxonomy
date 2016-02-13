import taxonomy
import os
import pickle

def main():
    isRunning = 1

    while (isRunning):
        input = raw_input("Taxonomy commands: insert <path>, list <path>, quit\n")
        command = input.split(" ")

        if (command[0] == "quit"):
            isRunning = 0
        elif (command[0] == "insert"):
            if ( command[1] ):
                pathList = command[1].split("/")
                categoryName = pathList.pop(0)
                order = taxonomy.Taxonomy(categoryName, "Order")
                path = "/".join(pathList)
                order.insert(path)
                order.serialize()
            else:
                print "Invalid path. Please try again"
        elif (command[0] == "list"):
            if ( command[1] ):
                pathList = command[1].split("/")
                categoryName = pathList.pop(0)
                order = taxonomy.Taxonomy(categoryName, "Order")
                print order.list()
            else:
                print "Invalid path. Please try again"
        else:
            print "improper syntax. plesae try again"

if __name__=="__main__":
    main()