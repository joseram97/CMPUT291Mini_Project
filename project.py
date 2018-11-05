#This is the pain code for the python interface for riders and drivers
#NOTE: for this project we will be coding for python3 rather than python
#       therefore when executing the application you must use "python3" in the
#       beginning of the command

#NOTE: for the sake of handling all of the applications
import sqlite3
import time
from commandClass import command
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
    global cmd
    # this will set the database connection
    print("Please enter the database path:")
    path = input("Database Path: ")
    try:
        cmd = command(path)
    except:
        print("Invalid DB path.. try again")
        initializeData()
    return

# The following functions are for the login portion of the application
#--------------------------LOGIN------------------------------------
def getUserInformation(username, password):
    global user
    # get all of the user information from the database and assign it to the
    # essentially this is where we fill up the database
    query = "query string will be here"
    userData = cmd.login_user(username,password)
    if userData is None:
        print("Invalid username and password.. Redirected back to login")
        loginPrompt()
        return False
    else:
        user = (userData[0],userData[1],userData[2],userData[3])
        return True

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
        break
    # done the while loop
    # get the rest of the information
    name = input("Full Name: ")
    phone = input("Phone Number(###-###-####): ")
    password = input("Password: ")
    print("\n")
    print("You will now be returned to the login screen...\n")
    # Now insert the user data into the database and return to the login screen
    try:
        cmd.register_new_user(email,name,phone,password)
        return True
    except:
        print("Non-unique email address.. returned to login")
        loginPrompt()
        return False

def loginUser():
    # get the user to login to the application
    print("Please type in your Username and Password...")
    username = input("Username(e-mail): ")
    password = input("Password: ")
    return getUserInformation(username, password)


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

def cancelBooking(booking):
    # cancel the booking that is selected
    while True:
        sure = input("Are you sure you want to cancel the booking? (y/n)")
        if sure == "n":
            return
        elif sure == "y":
            # remove the booking
            print("Deleting booking [{}]").format(booking[0])
            #dataConn.remove_booking_by_id(booking[0])
            print("Successfully removed the booking")
            break
    return

def bookMember(booking):
    # book a member
    return
# the parameters are the following:
#      resultList <- contains all the data for visuals
#      functionType <- the type of function that was deploted (e.g. "REQUEST",
#                                                                   "BOOK",
#                                                                   "RIDE")
def listSelection(resultList, functionType):
    # this function will be in charge of formatting the output of lists of
    # data for the system
    page_limit = 5
    i = 0
    if functionType == "RIDE":
        print("-------------------------------------------------------------------------")
        print("RIDE INFORMATION")
        print("All ride information will be shown below. Only a max of 5 rides will")
        print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
        print("'q' and press ENTER. To message the driver of a ride, enter in the")
        print("number of the RIDE SELECTION and type in a message. After message, ")
        print("the system will take you back to the main menu.")
    elif functionType == "REQUEST":
        print("-------------------------------------------------------------------------")
        print("RIDE REQUEST INFORMATION")
        print("All ride request information will be shown below. Only a max of 5 requests will")
        print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
        print("'q' and press ENTER. To delete a request, enter in the")
        print("number of the REQUEST SELECTION. After deletion, ")
        print("the system will take you back to the main menu.")
    elif functionType == "BOOK":
        print("-------------------------------------------------------------------------")
        print("BOOKINGS INFORMATION")
        print("All bookings information will be shown below. Only a max of 5 requests will")
        print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
        print("'q' and press ENTER. To cancel a booking or book a member, enter in the")
        print("number of the REQUEST SELECTION.")

    for ride in resultList:
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
                        if functionType == "RIDE":
                            sendMessage(resultList[selection-1][7],
                                        username, resultList[selection-1][0])
                        elif functionType == "REQUEST":
                            # the request must be deleted
                            sure = input("Are you sure? (y/n): ")
                            if sure == "y":
                                print("Deleting request...")
                                # TODO: dataConn.delete_ride_by_id(resultList[selection-1][0])
                                print("Request deleted. Back to main menu...")
                                return
                            elif sure == "n":
                                continue
                        elif functionType == "BOOK":
                            # the user will be prompted to wither cancel the
                            # booking or book a member
                            print("Please select the following action:")
                            print("1 - Cancel booking\n2 - Book member")
                            print("3 - Main Menu")
                            while True:
                                option = input("Input selection: ")
                                if option == "1":
                                    # cancel the booking
                                    cancelBooking(resultList[selection-1])
                                    print("Back to main menu...")
                                elif option == "2":
                                    #book a member
                                    bookMember(resultList[selection-1])
                                    print("Back to main menu...")
                                elif option == "3":
                                    print("Back to main menu...")
                                    return
                                else:
                                    print("Not a valid selection")

                        return
                except ValueError:
                    print("Not a number")

        if functionType == "RIDE":
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
        elif functionType == "REQUEST":
            print("///////////////////////////////////////////////////////")
            print("REQUEST SELECTION: " + str(i+1))
            print("Ride ID: {}\nEmail: {}").format(ride[0], ride[1])
            print("Date: {}\nPick up location: {}").format(ride[2], ride[3])
            print("Drop off location: {}\nAmount: {}").format(ride[4], ride[5])
            print("////////////////////////////////////////////////////////")
        elif functionType == "BOOK":
            print("///////////////////////////////////////////////////////")
            print("BOOKING SELECTION: " + str(i+1))
            print("Booking Number: {}\nSeats booked: {}").format(ride[0], ride[4])
            print("////////////////////////////////////////////////////////")

    return

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
    promptReqList = ["Date (yyyy-mm-dd): ", "Number of seats: ", "Price per seat: $",
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
    if not cmd.checkDate(inputList[0]):
        print("Invalid Date")
        offerRideUI()
    ##Src is not proper loc
    srcChoice = inputList[4]
    dstChoice = inputList[5]
    if not cmd.check_location(inputList[4]):
        l = cmd.get_locations_by_keyword(inputList[4])
        if type(l) is type(None):
            print("No matching src locations.. restarting")
            offerRideUI()
        else:
            dstChoice = printFive(l)



    ##Dst is not proper loc
    if not cmd.check_location(inputList[5]):
        l = cmd.get_locations_by_keyword(inputList[5])
        if type(l) is type(None):
            print("No matching dst locations.. restarting")
            offerRideUI()
        else:
            srcChoice = printFive(l)
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

    if inputList[-1] is "":
        try:
            inputList[-1] = get_car_by_driver(user[0])
        except:
            print("you do not own any vehicles!")
            runApp()


    if not cmd.check_car_ownership(inputList[-1],user[0]):
        print("You do not own this vehicle")
        offerRideUI()
    # now that we have all of the information, we query for the rides
    # TODO: COMPLETE THE OFFER RIDES FUNCTION
    cmd.offer_ride(inputList[0],user[0],inputList[1],inputList[2],inputList[3],srcChoice,dstChoice,inputList[-1],enroute)
    print("Successfully added offered ride! Returning to the main menu...\n")
    return

def printFive(l):
    i = 0
    max = len(l)
    print("Matching Locations:")
    print("Hit the number to make a selection:")
    while(True):
        flag = False
        try:
            print("1 - {0} City: {1}, Prov: {2}, Address: {3}".format(l[i][0],l[i][1],l[i][2],l[i][3]))
            print("2 - {0} City: {1}, Prov: {2}, Address: {3}".format(l[i+1][0],l[i+1][1],l[i+1][2],l[i+1][3]))
            print("3 - {0} City: {1}, Prov: {2}, Address: {3}".format(l[i+2][0],l[i+2][1],l[i+2][2],l[i+2][3]))
            print("4 - {0} City: {1}, Prov: {2}, Address: {3}".format(l[i+3][0],l[i+3][1],l[i+3][2],l[i+3][3]))
            print("5 - {0} City: {1}, Prov: {2}, Address: {3}".format(l[i+4][0],l[i+4][1],l[i+4][2],l[i+4][3]))
        except:
            flag = True
        print("6 - Next Five Choices")
        inp = input("Make a selection: ")
        if(inp is "6"):
            if flag:
                i = 0
            else:
                i+=5
        if(inp is "1"):
            return l[i][0]
        if(inp is "2"):
            return l[i+1][0]
        if(inp is "3"):
            return l[i+2][0]
        if(inp is "4"):
            return l[i+3][0]
        if(inp is "5"):
            return l[i+4][0]

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
    listSelection(resultRides, "RIDE")

    return

def bookMembersUI():
    # This is the booking UI for the user. The user should be able to view
    # bookings that they have booked an should be able to cancel some of
    # their bookings
    print("BOOKING MEMBERS:\nThis function will allow you to view all of your")
    print("rides that are booked by members. You will be able to cancel anyones")
    print("booking, or add a member to the booking.\n")
    print("Showing all of your bookings")
    # query to get all of the bookings related to the member.
    bookings = None #TODO dataConn.get_bookings_by_driver(username)
    listSelection(bookings, "BOOK")
    print("Please select from the following:")
    print("1 - ")

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
    listSelection(rideRequests, "REQUEST")


    return

def generateMessages():
    # generate all unseen messages from the user
    #print all of the messages
    mes = cmd.get_unseen_messages(user[0])
    if(len(mes)>0):
        for row in mes:
            print("--------------------------------------------------------------------")
            print("Email from: {0}".format(row[0]))
            print("Date: {0}".format(row[1]))
            print("Ride #: {0}\n".format(row[4]))
            print("Content: {0}".format(row[3]))
            print("--------------------------------------------------------------------")
    return

def runApp():
    print("Succesfully Logged In! Generating unseen messages...\n")
    # this function will run the main part of the application and their UI
    # elements

    # the first thing that will be visible is all of the messages that the
    # user has not seen yet
    generateMessages()


    # set up all of the possible options for the user to interact with
    print("The following selections may be chosen to proceed within the app:")
    print("1 - Offer a ride\n2 - Search for a ride\n3 - Book members or " +
          "cancel bookings\n4 - Post a ride request\n5 - Search and delete" +
          " ride requests\n6 - Exit application\n")
    selection = input("Please type in the desired selection(number): ")
    while True:
        if selection == "1":
            offerRideUI()
            break
        elif selection == "2":
            searchRideUI()
            break
        elif selection == "3":
            bookMembersUI()
            break
        elif selection == "4":
            postRideRequestUI()
            break
        elif selection == "5":
            searchDeleteRequestUI()
            break
        elif selection == "6":
            print("Logging out of application...")
            break
        else:
            print("Invalid selection. Try again...")

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
