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

def checkInput(promptString, fieldList, optional = False):
    # this function will check if a field has been inputted and will be
    # looped until it is not empty
    userInput = None
    while True:
        userInput = input(promptString)
        if userInput == "EXIT":
            print("Exiting...\n")
            return False
        elif userInput != "" or optional:
            break
        print("Field can't be empty")
    fieldList.append(userInput)
    return True

def initializeData():
    # this will set the database connection
    print("Please enter the database path:")
    path = input("Database Path: ")
    print("\n")
    # dataConn(path) OR dataConn.connect(path) NOTE: Whatever Curtis creates
    return

# The following functions are for the login portion of the application
#--------------------------LOGIN------------------------------------
def getUserInformation(password):
    # get all of the user information from the database and assign it to the
    # essentially this is where we fill up the database
    query = "query string will be here"
    # table = dataConn.query(query) NOTE: Need curtis functionality
    return True # this is for now until I put in Curtis's functions

def registerUser():
    # the user wants to be registered into the database
    print("REGISTRATION:\nPlease provide a unique e-mail, a name, a phone" +
    " number, and your password.\n")
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
            print("This email is not unique. Please try again.\n")
            print(" If you want to exit, type in EXIT\n")
    # done the while loop
    # get the rest of the information
    name = input("Full Name: ")
    phone = input("Phone Number(###-###-####): ")
    # TODO: check if the formatting of the phone number is good
    password = input("Password: ")
    print("\n")
    print("You will now be returned to the login screen...\n")
    # Now insert the user data into the database and return to the login screen
    # dataConn.insert(TODO: query for creating the user into the database)
    return True

def loginUser():
    # get the user to login to the application
    print("Please type in your Username and Password...")
    username = input("Username(e-mail): ")
    password = input("Password: ")
    return getUserInformation(password)


def loginPrompt():
    #This will be the first page that the user will see
    print("Hello! Welcome to CMPUT 291 RidesApp!!")
    print("Please select one of the following:\n")
    print("1 - Login\n2 - Register\n3 - Exit")

    selection = input("Type in the number: ")
    print("\n")
    # User has selected what they want
    if selection == "1":
        #user has selected that they want to login
        return loginUser()
    elif selection == "2":
        #user wants to register for the application
        if registerUser():
            # get the user to login officially
            return loginUser()
        else:
            #they were unable to register. exit the application
            print("Unable to register. Try again later.")
            print("Exiting application...\n")
            return False
    elif selection == "3":
        print("Exiting application...\n")
        return False
    return
#-------------------END LOGIN------------------------------------

#The following functions are for the main application
def offerRideUI():
    # this is the offer ride UI for the user to selection the options from
    print("OFFER RIDES:\nThis function will allow you to offer a ride as a")
    print(" driver. You wil be promted to fill in some information to start")
    print(" offering a ride. You must provide a date, number of seats, ")
    print("price per seat, luggage description (i.e. what luggage you carry), ")
    print("source location, and a destination location.")
    print("There will be an option to add your car number and enroute locations.\n")
    print("Please fill out the prompts below")
    print("[REQUIRED]")
    inputList = []
    promptReqList = ["Date (dd/mm/yyyy): ", "Number of seats: ", "Price per seat: $",
                    "Luggage Description (Don't press enter till done): ",
                    "Source location (e.g. City Name, Location Code): ",
                    "Destination Location: "]
    promptOptList = ["Car number: "]
    for prompt in promptReqList:
        if not checkInput(prompt, inputList):
            return
    print("[OPTIONAL]")
    print("NOTE: For the optional fields, just leave it blank to skip the field.")
    print("For the enroute locations, you can enter as many locations as possible, ")
    print("and to finish, just leave the last location blank.")
    for prompt in promptOptList:
        if not checkInput(prompt, inputList, True):
            return

    # get a set of enroute locations
    enroute = []
    i = 1
    while True:
        prompt = "Enroute Location[" + Integer.toString(i) + "]"
        enrouteLocation = input(prompt)
        if enrouteLocation == "":
            break
        enroute.append(enrouteLocation)
        i = i + 1

    # now that we have all of the information, we query for the rides
    # TODO: COMPLETE THE OFFER RIDES FUNCTION
    #offer_ride(inputList[0], inputList[1], inputList[2], inputList[3],
    #            inputList[4], inputList[5], inputList[6], enroute)
    print("Successfully added offered ride! Returning to the main menu...\n")
    return

def searchRideUI():
    return

def bookMembersUI():
    return

def postRideRequestUI():
    return

def searchDeleteRequestUI():
    return

def generateMessages():
    # generate all unseen messages from the user
    # TODO: query all of the message that are unseen (<> y)
    unseenMessages = None #TODO: dataConn.getMessages(username)

    # display all of the messages to the user
    if not unseenMessages:
        print("No unseen messages!...\n")
        return
    #print all of the messages
    for message in unseenMessages:
        print("--------------------------------------------------------------------")
        print("Email from: {}").format(message["sender"])
        print("Date: {}").format(message["msgTimestamp"])
        print("Ride #: {}\n").format(message["rno"])
        print("Content: {}").format(message["content"])
        print("--------------------------------------------------------------------")
    return

def runApp():
    print("Succesfully Logged In! Generating unseen messages...\n")
    # this function will run the main part of the application and their UI
    # elements

    # the first thing that will be visible is all of the messages that the
    # user has not seen yet
    generateMessages()

    while(True):
        # set up all of the possible options for the user to interact with
        print("The following selections may be chosen to proceed within the app:")
        print("1 - Offer a ride\n2 - Search for a ride\n3 - Book members or " +
              "cancel bookings\n4 - Post a ride request\n5 - Search and delete" +
              " ride requests\n6 - Exit application\n")
        selection = input("Please type in the desired selection(number): ")
        print("\n")
        if selection == "1":
            offerRideUI()
        elif selection == "2":
            searchRideUI()
        elif selection == "3":
            bookMembersUI()
        elif selection == "4":
            postRideRequestUI()
        elif selection == "5":
            searchDeleteRequestUI()
        elif selection == "6":
            print("Logging out of application...")
            break

    return

def main():
    #the main code for the software applications
    #enable a print to ask the user for their username
    initializeData()

    # show the login prompt
    if not (loginPrompt()):
        return

    # the login was succesful
    # run the main portion of the code
    runApp()
    return

if __name__ == "__main__":
    main()
