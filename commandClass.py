
import sqlite3
import datetime
from dataConn import *

class command:
    ##This will act as the application controller
    global data

    def __init__(self, path):
        connect(path)


    def post_new_ride_request(self,date,pLoc,dLoc,amount,email):
        if not self.checkDate(date):
            print("Improper date format, try again");
        rid = get_max_request_id()[0] + 1
        post_ride_request(date,pLoc,dLoc,amount,rid,email)
        return

    ##3 Keywords and Number of keywords passed!
    ## Leave key2,3 as "!" (STRING) if unused "!" will never match a location and act as if it
    ## does not exist
    def searchForRides(self,key1,key2,key3):
        ##TODO: Adapt to display rides
        return search_for_rides(key1,key2,key3)

    ##All args are strings besides enroute, which is a list of locations
    def offer_ride(self,date, driver, seats, price, lugDesc, src, dst, cno, enroute):
        ##Check date
        if not self.checkDate(date):
            print("Improper date format, try again");
            ##TODO: send back to UI class to take input
        if not self.checkSeats(seats,cno):
            print("Seats greater than seats in car")

        ##TODO check enroutes

        ##todo: check cno, src, dst


        offer_ride(date,driver,seats,price,lugDesc,src,dst,cno,enroute)
        return

    ##PROPER FORMAT: YYYY-MM-DD
    ##FALSE IF NOT THIS FORMAT
    def checkDate(self, date):
        try:
            match = datetime.datetime.strptime(date,"%Y-%m-%d")
            return True
        except:
            return False

    def checkSeats(self,seats,cno):
        ##Checks both seat count and cno
        cars = get_car_by_cno(cno)
        return cars[4] >= seats and cno == cars[0]

    def checkLocationCode(self, lCode):
        ##Returns either lCode if lCode is an lCode OR list of relevant locations if keyword
        loc = get_locations_by_location_code(lCode)
        if type(loc) is not type(None):
            return lCode
        else:
            return get_locations_by_keyword(lCode)

def main():
    c = command("./a2.db")
    print("Testing date validation: ")
    print(c.checkDate("2018-09-02"))
    print(c.checkDate("20812-12-12")) ##Date testing..
    print(c.checkDate("2018-121-12"))
    print(c.checkDate("2018-12-121"))

    print("Testing seat validation and ownership: ")
    print(c.checkSeats(5,4))
    print(c.checkSeats(4,4))
    print(c.checkSeats(3,4))

    ##c.post_new_ride_request("2018-02-01","cntr1","cntr2","12","don@mayor.yeg")
    ##c.offer_ride("2018-02-01","don@mayor.yeg",4,12,"desc","cntr1","cntr2",4,[])

    ##WORKING
    ##print("Testing location checks: ")
    ##print(c.checkLocationCode('cntr1'))
    for row in get_requests_by_location("nrth1"):
        print("{0}: {1} {2}".format(row[0],row[1],row[2]))
    return

if __name__ == "__main__":
    main()
