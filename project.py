#This is the pain code for the python interface for riders and drivers
#NOTE: for this project we will be coding for python3 rather than python
#       therefore when executing the application you must use "python3" in the
#       beginning of the command

#NOTE: for the sake of handling all of the applications
import sqlite3
import time
from dataConn import * #this will get all of the class functions
from tkinter import *

connection = None
cursor = None



def main():
    #the main code for the software applications
    #enable a print to ask the user for their username

    #testing tkinter
    root = Tk()
    theLabel = Label(root, text="CMPUT291 Mini-Project")
    theLabel.pack()
    theLabel.mainloop()

    return

if __name__ == "__main__":
    main()
