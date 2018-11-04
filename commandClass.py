
import sqlite3
import datetime
import dataConn.py

class command:
    ##This will act as the application controller
    global data

    ##All args are strings besides enroute, which is a list of locations
    def offer_ride(date, driver seats, price, lugDesc, src, dst, cno, enroute):
        ##Check date
        if not checkDate(date):
            print("Improper date format, try again");
            ##TODO: send back to UI class to take input
        if not checkSeats(seats,cno):
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
        ##TODO: Implement seat check.. Query DB
        cars = get_car_by_cno(cno)
        return cars[4] is seats and cno is cars[0]

def main():
    c = command()
    print(c.checkDate("2018-09-02"))
    print(c.checkDate("20812-12-12"))
    print(c.checkDate("2018-121-12"))
    print(c.checkDate("2018-12-121"))

    return

if __name__ == "__main__":
    main()
