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
        elif userInput == "Date (dd/mm/yyyy): ":
            #check that the format is correct
            #TODO: check format is correct
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

    while True:
        selection = input("Type in the number: ")
        print("")
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
        else:
            print("Please try again...")
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
        prompt = "Enroute Location[" + str(i) + "]: "
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

def sendMessage(driver, userEmail, rno):
    # send a message to the driver
    print("Type in your message below and press ENTER twice in")
    print("a row to send it\n")
    print("Message Content: ")
    messageContent = ""
    while True:
        line = input()
        if line == "":
            print("Sending the message...")
            break
        messageContent = messageContent + line

    # send the message to the dataBase
    #dataConn.send_message(driver, Date.now, userEmail, messageContent, rno, "n")
    print("Message has been sent. Back to main menu...")
    return

def searchRideUI():
    # This is the search ride UI for the application. The user should be able to
    # search for rides that they are interested in
    print("SEARCH FOR RIDES:\nThis function will allow you to search for rides")
    print("within 1-3 locations.")
    print("Please provide below the 1-3 locations")
    numLocations = int(input("How many locations will you be searching?: "))
    searchLocations = []
    for i in range(1, numLocations+1):
        prompt = "Search Location[" + str(i) + "]: "
        if not checkInput(prompt, searchLocations):
            return # leave the function
    # Query for all of the locations
    resultRides = None # dataConn(searchLocations)
    # display all of the search results
    page_limit = 5
    i = 0
    print("-------------------------------------------------------------------------")
    print("RIDE INFORMATION")
    print("All ride information will be shown below. Only a max of 5 rides will")
    print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
    print("'q' and press ENTER. To message the driver of a ride, enter in the")
    print("number of the RIDE SELECTION and type in a message. After message, ")
    print("the system will take you back to the main menu.")
    for ride in resultRides:
        # display all of the ride information
        if i%5 == 0:
            while True:
                displayMore = input("[MORE?]:")
                if displayMore == "q":
                    print("Taking you back to main menu...")
                    return
                elif displayMore == "":
                    break
                selection = None
                try:
                    selection = int(displayMore)
                    if selection > i:
                        print("Not a valid selection")
                    else:
                        sendMessage(ride[7], username, ride[0])
                        return
                except ValueError:
                    print("Not a number")

        # user wants to see more
        print("///////////////////////////////////////////////////////")
        print("RIDE SELECTION: " + str(i+1))
        print("Ride Number: {}\nRide price: {}").format(ride[0], ride[1])
        print("Date: {}\nNumber of seats: {}").format(ride[2], ride[3])
        print("Luggage Description: {}\nStart location: {}").format(ride[4], ride[5])
        print("End Location: {}\nDriver: {}").format(ride[6], ride[7])
        print("CAR INFORMATION")
        print("Car number: {}\nMake: {}\nModel: {}").format(ride[8], ride[9], ride[10])
        print("Year: {}\nSeats: {}\nOwner: {}").format(ride[11], ride[12], ride[13])
        print("////////////////////////////////////////////////////////")


    return

def bookMembersUI():
    # This is the booking UI for the user. The user should be able to view
    # bookings that they have booked an should be able to cancel some

    return

def postRideRequestUI():
    # The user will be able to post a ride request that they want a driver to
    # start offering
    print("REQUEST A RIDE:\nThis function will allow you to post a ride request")
    print("on the application. You must provide a date(dd/mm/yyyy), pick up")
    print("location, drop off location, and the amount willing to pay for a")
    print("seat.\n")
    print("Please fill in the required fields below:")
    requestField = ["Date (dd/mm/yyyy): ", "Pick up location: ",
                    "Drop off location: ", "Amout per seat: $"]
    fieldResults = []
    for prompt in requestField:
        if not checkInput(prompt, fieldResults):
            return

    # with all of the information, insert it into the database
    print("Posting...")
    # dataConn.post_ride_request(fieldResults)
    print("Successfully posted ride request! Sending back to main menu...")
    return

def searchDeleteRequestUI():
    # search for requests and allow deletion of requests
    # give the choice to the user if they wish to display all of the requests
    # or search for a specific location of some requests
    print("SEARCH/DELETE RIDE REQUESTS:\nThis function will allow to you")
    print("search for the rides that you have requested. You will also have")
    print("the option to delete any of the ride requests that you have up.\n")
    print("Please select one of the following options:")
    print("1 - See all ride requests\n2 - Search for ride requests")
    print("3 - Go back to main menu")
    # ride Requests will hold all of the ride information
    rideRequests = None
    while True:
        userInput = input("Input the number selection: ")
        if userInput == "1":
            # get all ride requests
            print("Showing all ride requests...\n")
            #rideRequests = dataConn.get_ride_requests_by_email(username)
            break
        elif userInput == "2":
            # search for desired ride requests
            print("SEARCHING FOR RIDES:")
            print("In order to search for ride requests, you will need to provide")
            print("a location code or city name.\n")
            location = input("Provide the location: ")
            #rideRequests = dataConn.get_requests_by_location(location)
            break
        elif userInput == "3":
            # exit out of the function
            print("Exiting function...")
            return
        else:
            print("Not a valid selection! Try again...")

    # print all of the ride requests from the user
    page_limit = 5
    i = 0
    print("-------------------------------------------------------------------------")
    print("RIDE REQUEST INFORMATION")
    print("All ride request information will be shown below. Only a max of 5 requests will")
    print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
    print("'q' and press ENTER. To delete a request, enter in the")
    print("number of the REQUEST SELECTION. After deletion, ")
    print("the system will take you back to the main menu.")
    for ride in rideRequests:
        # display all of the ride information
        if i%5 == 0:
            while True:
                displayMore = input("[MORE?]:")
                if displayMore == "q":
                    print("Taking you back to main menu...")
                    return
                elif displayMore == "":
                    break
                selection = None
                try:
                    selection = int(displayMore)
                    if selection > i:
                        print("Not a valid selection")
                    else:
                        # the request must be deleted
                        sure = input("Are you sure? (y/n): ")
                        if sure == "y":
                            print("Deleting request...")
                            # dataConn.delete_ride_by_id(ride[0])
                            print("Request deleted. Back to main menu...")
                            return
                        elif sure == "n":
                            continue
                except ValueError:
                    print("Not a number")

        # user wants to see more
        print("///////////////////////////////////////////////////////")
        print("REQUEST SELECTION: " + str(i+1))
        print("Ride ID: {}\nEmail: {}").format(ride[0], ride[1])
        print("Date: {}\nPick up location: {}").format(ride[2], ride[3])
        print("Drop off location: {}\nAmount: {}").format(ride[4], ride[5])
        print("////////////////////////////////////////////////////////")

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
