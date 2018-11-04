#This is the pain code for the python interface for riders and drivers
#NOTE: for this project we will be coding for python3 rather than python
#       therefore when executing the application you must use "python3" in the
#       beginning of the command

#NOTE: for the sake of handling all of the applications
import sqlite3
import time
#from dataConn import * #this will get all of the class functions
#from tkinter import *

#these will be the global variables throughout the application
username = None

connection = None
cursor = None

def initializeData():
    # this will set the database connection
    print("Please enter the database path:\n")
    path = input("Database Path: ")
    # dataConn(path) OR dataConn.connect(path) NOTE: Whatever Curtis creates
    return

def getUserInformation(password):
    # get all of the user information from the database and assign it to the
    # essentially this is where we fill up the database
    query = "query string will be here"
    # table = dataConn.query(query) NOTE: Need curtis functionality
    return

def registerUser():
    # the user wants to be registered into the database
    print("REGISTRATION:\nPlease provide a unique e-mail, a name, a phone")
    print(" number, and your password.\n\n")
    email = None
    while(True):
        email = input("Username(e-mail): ")
        if (email == "EXIT"):
            print("Exiting...")
            return False
        # check the email if it already exists
        # TODO: creating email query for the database and return boolean
        isUnique = True
        if (isUnique):
            break
        else:
            print("This email is not unique. Please try again.")
            print(" If you want to exit, type int EXIT\n")
    # done the while loop
    # get the rest of the information
    name = input("Full Name: ")
    phone = input("Phone Number(###-###-####): ")
    # TODO: check if the formatting of the phone number is good
    password = input("Password: ")

    # Now insert the user data into the database and return to the login screen
    # dataConn.insert(TODO: query for creating the user into the database)
    return True

def loginUser():
    # get the user to login to the application
    print("Please type in your Username and Password...\n")
    username = input("Username(e-mail): ")
    password = input("Password: ")
    getUserInformation(password)
    return

def loginPrompt():
    #This will be the first page that the user will see
    print("Hello! Welcome to CMPUT 291 RidesApp!!\n")
    print("Please select one of the following:\n\n")
    print("1 - Login\n\n2 - Register\n\n")
    selection = input("Type in the number: ")
    # User has selected what they want
    if selection == "1":
        #user has selected that they want to login
        loginUser()
    elif selection == "2":
        #user wants to register for the application
        if registerUser():
            # get the user to login officially
            loginUser()
        else:
            #they were unable to register. exit the application
            print("Unable to register. Try again later.\n")
            print("Exiting application...")
    return

def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    initializeData()

    # show the login prompt
    loginPrompt()

if __name__ == "__main__":
    main()
