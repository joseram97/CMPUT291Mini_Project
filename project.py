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
        elif userInput == "Date (yyyy-mm-dd): ":
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
        if sure is "n":
            return
        elif sure is "y":
            # remove the booking
            print("Deleting booking [{}]").format(booking[0])
            #dataConn.remove_booking_by_id(booking[0])
            cancelMessage = "Your booking for [" + str(booking[2]) + "]" + " has been cancelled!"
            #dataConn.send_message_to_member(booking[1], user, cancelMessage)
            print("Successfully removed the booking")
            break
    return

def bookMember(rideOffer):
    # book a member
    print("You wish to book a member. You are required to provide the following:")
    print("the members email, the number of seats booked, cost per seat, pick up")
    print("location code, and drop off location code.")
    print("Please fill in the following fields below:")
    bookingList = ["Member email: ", "Number of booked seats: ",
                   "Cost per seat: $", "Pick up location [code]: ",
                   "Drop off location [code]: "]
    inputResults = []
    for prompt in bookingList:
        if prompt == "Number of booked seats: ":
            # check that the number of seats is not over booked
            while True:
                numSeats = input(prompt)
                if (numSeats == "EXIT"):
                    print("Exiting function...")
                    return
                overbooked = False #use the number of seats to check
                if overbooked:
                    # display if the user wants to overide it
                    allow = input("Will you allow overbooking? [y/n]: ")
                    if allow == "y":
                        inputResults.append(numSeats)
                        break
                    elif allow == "n":
                        print("Please change the number of booked seats.")
        elif not checkInput(prompt, inputResults):
            return

    # all the inputs are gathered and must be inserted into the database
    print("Booking member [{}] to rno [{}]...").format(inputResults[0], rideOffer[0])
    # dataConn.book_member_for_ride(rideOffer[0], inputResults[0],
    #                               inputResults[1], inputResults[2], inputResults[3],
    #                               inputResults[4])
    print("Member is now booked! Returning to main menu...")
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
        if type(resultList) is type(None):
            print("No rides matching")
            return
        option = doRideSearch(resultList)
        if option is not "":
            row = option
            content = input("What would you like to send to the user:")
            rnum = row[0]
            cmd.send_message_to_member(row[7],user[0],content,rnum)
    elif functionType == "SEARCH":
        if type(resultList) is type(None):
            print("No locations matching {0}".format(loc))
            return
        option = doRequestSearch(resultList)
        if option is not "":
            row = option
            content = input("What would you like to send to the user:")
            rnum = input("Please enter the VALID rno you want to message about:")
            cmd.send_message_to_member(row[1],user[0],content,rnum)

    elif functionType == "REQUEST":
        print("-------------------------------------------------------------------------")
        print("RIDE REQUEST INFORMATION")
        print("All ride request information will be shown below.")
        print("To delete a request, enter the request index (NOT rid) in the input")
        i = 0
        for row in resultList:
            print("{0} -- rid:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, cost:{5}".format(i,row[0],row[2],row[3],row[4],row[5]))
            i += 1

        print("To cancel a request, type the index on the left. Otherwise leave it empty and hit enter")
        option = input("Make a selection: ")
        if option is not "":
            op = int(option)
            row = resultList[op]
            cmd.delete_ride_request_by_id(row[0])
    elif functionType == "OFFER":
        print("-------------------------------------------------------------------------")
        print("RIDE OFFER INFORMATION")
        print("----------Offered rides-------------")
        ret = doOfferBookings(resultList)
        if ret is not "":
            bookMemberforDriver(ret[0],ret[1])
    elif functionType == "BOOK":
        print("-------------------------------------------------------------------------")
        print("BOOKINGS INFORMATION")
        print("All bookings information will be shown below. Only a max of 5 bookings will")
        print("be shown at a time. To keep seeing 5 more, press ENTER. To leave type")
        print("'q' and press ENTER. To cancel a booking, enter in the")
        print("number of the BOOKING SELECTION.")
        print("----------Booking info-------------")
        i = 0
        for row in resultList:
            print("{0} -- bno:{1}, email:{2}, rno:{3}, cost:{4}, seats:{5}, pickup:{6}, dropoff:{7}".format(i,row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            i += 1
        print("")
        print("To cancel a booking, type the index on the left. Otherwise leave it empty and hit enter")
        option = input("Make a selection: ")
        if option is not "":
            op = int(option)
            row = resultList[op]
            cmd.cancel_booking_by_bno(row[0],row[1],user[0],row[2]) ##remove booking

    return

def doRideSearch(l):
    i = 0
    max = len(l)
    print("----------Searched Rides Results-----------")
    print("Hit the number to make a selection to being messaging a user:")

    while(True):
        flag = False
        print("1 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i][0],l[i][1],l[i][2],l[i][3],l[i][4],l[i][5],l[i][6],l[i][7],l[i][8]))
        r1 = cmd.get_car_by_cno(l[i][8])
        print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r1[0],r1[1],r1[2],r1[3],r1[4],r1[5]))

        print("2 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+1][0],l[i+1][1],l[i+1][2],l[i+1][3],l[i+1][4],l[i+1][5],l[i+1][6],l[i+1][7],l[i+1][8]))
        r2 = cmd.get_car_by_cno(l[i+1][8])
        print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r2[0],r2[1],r2[2],r2[3],r2[4],r2[5]))

        print("3 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+2][0],l[i+2][1],l[i+2][2],l[i+2][3],l[i+2][4],l[i+2][5],l[i+2][6],l[i+2][7],l[i+2][8]))
        r3 = cmd.get_car_by_cno(l[i+2][8])
        print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r3[0],r3[1],r3[2],r3[3],r3[4],r3[5]))

        print("4 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+3][0],l[i+3][1],l[i+3][2],l[i+3][3],l[i+3][4],l[i+3][5],l[i+3][6],l[i+3][7],l[i+3][8]))
        r4 = cmd.get_car_by_cno(l[i+3][8])
        print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r4[0],r4[1],r4[2],r4[3],r4[4],r4[5]))

        print("5 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+4][0],l[i+4][1],l[i+4][2],l[i+4][3],l[i+4][4],l[i+4][5],l[i+4][6],l[i+4][7],l[i+4][8]))
        r5 = cmd.get_car_by_cno(l[i+4][8])
        print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r5[0],r5[1],r5[2],r5[3],r5[4],r5[5]))
        try:
            print("1 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i][0],l[i][1],l[i][2],l[i][3],l[i][4],l[i][5],l[i][6],l[i][7],l[i][8]))
            r1 = cmd.get_car_by_cno(l[i][8])
            print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r1[0],r1[1],r1[2],r1[3],r1[4],r1[5]))

            print("2 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+1][0],l[i+1][1],l[i+1][2],l[i+1][3],l[i+1][4],l[i+1][5],l[i+1][6],l[i+1][7],l[i+1][8]))
            r2 = cmd.get_car_by_cno(l[i+1][8])
            print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r2[0],r2[1],r2[2],r2[3],r2[4],r2[5]))

            print("3 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+2][0],l[i+2][1],l[i+2][2],l[i+2][3],l[i+2][4],l[i+2][5],l[i+2][6],l[i+2][7],l[i+2][8]))
            r3 = cmd.get_car_by_cno(l[i+2][8])
            print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r3[0],r3[1],r3[2],r3[3],r3[4],r3[5]))

            print("4 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+3][0],l[i+3][1],l[i+3][2],l[i+3][3],l[i+3][4],l[i+3][5],l[i+3][6],l[i+3][7],l[i+3][8]))
            r4 = cmd.get_car_by_cno(l[i+3][8])
            print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r4[0],r4[1],r4[2],r4[3],r4[4],r4[5]))

            print("5 - rno:{0}, price:{1}, rdate:{2}, seats:{3}, lugDesc:{4}, src:{5}, dst:{6}, driver:{7}, cno:{8}".format(l[i+4][0],l[i+4][1],l[i+4][2],l[i+4][3],l[i+4][4],l[i+4][5],l[i+4][6],l[i+4][7],l[i+4][8]))
            r5 = cmd.get_car_by_cno(l[i+4][8])
            print("Car info ---> cno: {0}, make: {1}, model: {2}, year: {3}, seats: {4}, owner: {5}".format(r5[0],r5[1],r5[2],r5[3],r5[4],r5[5]))
        except:
            flag = True
        print("6 - Next Five Choices")
        print("7 - Exit")
        inp = input("Make a selection: ")
        if(inp is "6"):
            if flag:
                i = 0
            else:
                i+=5
        if(inp is "7"):
            return ""
        if(inp is "1"):
            return l[i]
        if(inp is "2"):
            return l[i+1]
        if(inp is "3"):
            return l[i+2]
        if(inp is "4"):
            return l[i+3]
        if(inp is "5"):
            return l[i+4]

    return


def doRequestSearch(l):
    i = 0
    max = len(l)
    print("----------Requested Rides Search Results-----------")
    print("Hit the number to make a selection to being messaging a user:")

    while(True):
        flag = False
        try:
            print("1 - rid:{0}, email:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, amount:{5}".format(l[i][0],l[i][1],l[i][2],l[i][3],l[i][4],l[i][5]))
            print("2 - rid:{0}, email:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, amount:{5}".format(l[i+1][0],l[i+1][1],l[i+1][2],l[i+1][3],l[i+1][4],l[i+1][5]))
            print("3 - rid:{0}, email:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, amount:{5}".format(l[i+2][0],l[i+2][1],l[i+2][2],l[i+2][3],l[i+2][4],l[i+2][5]))
            print("4 - rid:{0}, email:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, amount:{5}".format(l[i+3][0],l[i+3][1],l[i+3][2],l[i+3][3],l[i+3][4],l[i+3][5]))
            print("5 - rid:{0}, email:{1}, rdate:{2}, pickup:{3}, dropoff:{4}, amount:{5}".format(l[i+4][0],l[i+4][1],l[i+4][2],l[i+4][3],l[i+4][4],l[i+4][5]))
        except:
            flag = True
        print("6 - Next Five Choices")
        print("7 - Exit")
        inp = input("Make a selection: ")
        if(inp is "6"):
            if flag:
                i = 0
            else:
                i+=5
        if(inp is "7"):
            return ""
        if(inp is "1"):
            return l[i]
        if(inp is "2"):
            return l[i+1]
        if(inp is "3"):
            return l[i+2]
        if(inp is "4"):
            return l[i+3]
        if(inp is "5"):
            return l[i+4]

    return

def doOfferBookings(l):
    i = 0
    max = len(l)
    print("----------Offered future rides-----------")
    print("Hit the number to make a selection to being booking a user:")

    while(True):
        flag = False
        try:
            print("1 - rno: {0}, Available Seats: {1}".format(l[i][0],l[i][1]))
            print("2 - rno: {0}, Available Seats: {1}".format(l[i+1][0],l[i+1][1]))
            print("3 - rno: {0}, Available Seats: {1}".format(l[i+2][0],l[i+2][1]))
            print("4 - rno: {0}, Available Seats: {1}".format(l[i+3][0],l[i+3][1]))
            print("5 - rno: {0}, Available Seats: {1}".format(l[i+4][0],l[i+4][1]))
        except:
            flag = True
        print("6 - Next Five Choices")
        print("7 - Exit")
        inp = input("Make a selection: ")
        if(inp is "6"):
            if flag:
                i = 0
            else:
                i+=5
        if(inp is "7"):
            return ""
        if(inp is "1"):
            return (l[i][0],l[i][1])
        if(inp is "2"):
            return (l[i+1][0],l[i+1][1])
        if(inp is "3"):
            return (l[i+2][0],l[i+2][1])
        if(inp is "4"):
            return (l[i+3][0],l[i+3][1])
        if(inp is "5"):
            return (l[i+4][0],l[i+4][1])

    return

def bookMemberforDriver(rno,seats):
    name = input("Please enter member email: ")
    numSeats = input("Please enter how many seats:")
    if(int(numSeats) > int(seats)):
        pr = input("Ride will be overbooked, continue? (y/n):")
        if pr is not "y":
            return
    cost = input("please enter the cost per seat: ")
    src = input("please enter the pickup: ")
    if not cmd.check_location(src):
        print("pickup location does not exist")
        return
    dst = input("please enter the dropoff: ")
    if not cmd.check_location(dst):
        print("dropoff location does not exist")
        return

    if not cmd.check_ride_ownership(user[0],rno):
        print("You do not own this ride and cannot book for it")
        return

    cmd.book_ride_for_member_by_driver(name,rno,numSeats,cost,src,dst,user[0])
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
            srcChoice = printFive(l)



    ##Dst is not proper loc
    if not cmd.check_location(inputList[5]):
        l = cmd.get_locations_by_keyword(inputList[5])
        if type(l) is type(None):
            print("No matching dst locations.. restarting")
            offerRideUI()
        else:
            dstChoice = printFive(l)
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
    if numLocations > 3:
        numLocations = 3
    searchLocations = []
    for i in range(1, numLocations+1):
        prompt = "Search Location[" + str(i) + "]: "
        if not checkInput(prompt, searchLocations):
            return # leave the function
    # Query for all of the locations
    print("Executing search.. This may take some time")
    resultRides = cmd.search_for_rides(searchLocations)
    # display all of the search results
    listSelection(resultRides, "RIDE")

    return

def bookMembersUI():
    # This is the booking UI for the user. The user should be able to view
    # bookings that they have booked an should be able to cancel some of
    # their bookings
    print("BOOKING MEMBERS:\nThis function will allow you to view all of your")
    print("rides that are booked by members. You will be able to cancel anyones")
    print("booking, or add a member to an offred ride.\n")
    print("Please select one of the following:")
    print("1 - Show all bookings\n2 - Show all offered rides")
    print("3 - Main menu")
    # query to get all of the bookings related to the member.
    bookings = cmd.get_bookings_by_driver(user[0])
    offeredRides = cmd.get_rides_with_available_seats_by_member(user[0])
    exitFlag = False
    while not exitFlag:
        selectInput = input("Enter selection: ")
        if selectInput == "1":
            print("Showing all of your bookings...")
            listSelection(bookings, "BOOK")
            break
        if selectInput == "2":
            print("Showing all of you ride offers...")
            listSelection(offeredRides, "OFFER")
            break
        elif selectInput == "3":
            print("Main menu")
            exitFlag = True

    return

def postRideRequestUI():
    # The user will be able to post a ride request that they want a driver to
    # start offering
    print("REQUEST A RIDE:\nThis function will allow you to post a ride request")
    print("on the application. You must provide a date(yyyy-mm-dd), pick up")
    print("location, drop off location, and the amount willing to pay for a")
    print("seat.\n")
    print("Please fill in the required fields below:")
    requestField = ["Date (yyyy-mm-dd): ", "Pick up location: ",
                    "Drop off location: ", "Amout per seat: $"]
    fieldResults = []
    for prompt in requestField:
        if not checkInput(prompt, fieldResults):
            return

    print(fieldResults[0])
    if not cmd.checkDate(fieldResults[0]):
        print("Invalid Date")
        postRideRequestUI()
    ##Src is not proper loc
    srcChoice = fieldResults[1]
    dstChoice = fieldResults[2]
    if not cmd.check_location(fieldResults[1]):
        print("No matching src locations.. restarting")
        postRideRequestUI()

    ##Dst is not proper loc
    if not cmd.check_location(fieldResults[2]):
        print("No matching dst locations.. restarting")
        postRideRequestUI()

    # with all of the information, insert it into the database
    print("Posting...")
    cmd.post_new_ride_request(fieldResults[0],srcChoice,dstChoice,fieldResults[3],user[0])
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
            rideRequests = cmd.get_ride_requests_by_email(user[0])
            listSelection(rideRequests, "REQUEST")
            break
        elif userInput == "2":
            # search for desired ride requests
            print("SEARCHING FOR RIDES:")
            print("In order to search for ride requests, you will need to provide")
            print("a location code or city name.\n")
            location = input("Provide the location: ")
            rideRequests = cmd.get_requests_by_location(location)
            listSelection(rideRequests, "SEARCH")
            break
        elif userInput == "3":
            # exit out of the function
            print("Exiting function...")
            return
        else:
            print("Not a valid selection! Try again...")

    # print all of the ride requests from the user


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
    while True:
        print("The following selections may be chosen to proceed within the app:")
        print("1 - Offer a ride\n2 - Search for a ride\n3 - Book members or " +
              "cancel bookings\n4 - Post a ride request\n5 - Search and delete" +
              " ride requests\n6 - Exit application\n7 - Log out")
        selection = input("Please type in the desired selection(number): ")
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
            print("Exiting out of application...")
            break
        elif selection == "7":
            print("Logging out.. restaring app")
            user = None
            main()
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
