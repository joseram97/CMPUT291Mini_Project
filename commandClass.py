
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

    def login_user(self,email,pwd):
        user = check_login(email,pwd)
        return user

    def register_new_user(self,email,name,phone,password):
        try:
            register(email,name,phone,password)
        except:
            raise Exception("Non-Unique email")

    def get_unseen_messages(self,email):
        ret = get_unseen_messages_by_email(email)
        set_messages_to_seen(email)
        return ret

    def check_location(self,lCode):
        loc = get_locations_by_location_code(lCode)
        if type(loc) is type(None):
            return False
        else:
            return True



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

    def get_bookings_by_driver(self,driver):
        return get_bookings_by_driver(driver)

    def cancel_booking_by_bno(self,bno,email,sender,rno):
        remove_booking_by_id(bno,email,sender,rno)
        return

    def book_ride_for_member_by_driver(self,email,rno,seats,cost,src,dst,driver):
        book_member_for_ride_by_driver(rno,email,seats,cost,src,dst,driver)
        return

    def check_ride_ownership(self,email,rno):
        r = check_ride_ownership(email,rno)
        if type(r) is type(None):
            return False
        else:
            return True

    def get_rides_with_available_seats_by_member(self,driver):
        return get_rides_with_available_seats_by_member(driver)

    def delete_ride_request_by_id(self,rid):
        return delete_ride_request_by_id(rid)

    def get_ride_requests_by_email(self,email):
        return get_ride_requests_by_email(email)

    def check_car_ownership(self,cno,driver):
        c = get_car_by_driver_cno(cno,driver)
        if type(c) is type(None):
            return False
        else:
            return True

    def get_car_by_driver(self,driver):
        c = get_car_by_driver(driver)
        return c[0]

    def checkSeats(self,seats,cno):
        ##Checks both seat count and cno
        cars = get_car_by_cno(cno)
        return cars[4] >= seats and cno == cars[0]

    def get_locations_by_keyword(self,key):
        return get_locations_by_keyword(key)

    def get_requests_by_location(self,key):
        return get_requests_by_location(key)

    def send_message_to_member(self, email,sender,content,rno):
        try:
            send_message_to_member(email,sender,content,rno)
            print("message sent")
        except:
            print("given rno or email is not valid. Please try again")
        return
