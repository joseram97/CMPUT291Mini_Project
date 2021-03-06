import sqlite3
from datetime import datetime
import os
#this is the data class that will hold all of the information for the
# mini-project

#The following is all code from the lab that I did for getting the data
# from the tables
connection = None
cursor = None

def connect(path):
    global connection, cursor
    if not os.path.isfile(path):
        raise Exception("Invalid path")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return



def offer_ride(date,driver,seats,price,desc,src,dst,cno,enroute):
    ##Needed for spec 1
    rno = get_max_ride_id()[0] + 1
    offer_ride=     '''
                    INSERT INTO rides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno) VALUES
                        (:rno,:price,:date,:seats,:desc,:src,:dst,:driver,:cno);
                    '''
    cursor.execute(offer_ride,{"rno":rno,"price":price,"date":date,"seats":seats,"desc":desc,"src":src,"dst":dst,"driver":driver,"cno":cno});
    connection.commit()
    return rno


def check_login(email,password):
    query = '''
            SELECT * FROM members WHERE email=:email AND pwd=:pass
            '''
    cursor.execute(query,{"email":email,"pass":password})
    connection.commit()
    return cursor.fetchone()

def register(email,name,phone,password):
    register=       '''
                    INSERT INTO members(email, name, phone, pwd) VALUES
                        (:email,:name,:phone,:pwd)
                    '''
    cursor.execute(register,{"email":email,"name":name,"phone":phone,"pwd":password})
    connection.commit()
    return

def check_email(email):
    q = '''
        SELECT * FROM members WHERE email=:email;
        '''
    cursor.execute(q,{"email":email})
    connection.commit()
    return cursor.fetchone()

#Returns all locations by lCode
def get_locations_by_location_code(lCode):
    get_locations =     '''
                        SELECT * FROM locations WHERE lcode = :lcode;
                        '''
    cursor.execute(get_locations,{"lcode":lCode});
    connection.commit()
    return cursor.fetchone()

def add_enroute(lcode,rno):
    add_enroute = '''
                  INSERT INTO enroute(rno,lcode) VALUES
                  (:rno,:lcode);
                  '''
    cursor.execute(add_enroute,{"rno":rno,"lcode":lcode});
    connection.commit()
    return

#Returns all locations by keyword **Used if lCode is not found**
def get_locations_by_keyword(keyword):
    keyword = '%'+keyword+'%'
    get_locations =     '''
                        SELECT * FROM locations WHERE city LIKE :keyword
                        UNION
                        SELECT * FROM locations WHERE prov LIKE :keyword
                        UNION
                        SELECT * FROM locations WHERE address LIKE :keyword;
                        '''
    cursor.execute(get_locations,{"keyword":keyword});
    connection.commit()
    return cursor.fetchall()

##NOTE: Incomplete
def search_for_rides(listKeys):
    # listKeys is a list of all of the location keywords
    keys = [""]*3
    i = 0
    for keyword in listKeys:
        keys[i] = keyword
        i = i + 1

    key1 = '%'+keys[0]+'%'
    key2 = '%'+keys[1]+'%'
    key3 = '%'+keys[2]+'%'

    ride_search =   '''
                    SELECT DISTINCT r.*
                    FROM rides r, enroute e, locations l
                    WHERE (r.rno = e.rno
                    AND e.lcode = l.lcode
                    OR r.src = l.lcode
                    OR r.dst = l.lcode)
                    AND (l.city LIKE :key1
                    OR l.prov LIKE :key1
                    OR l.address LIKE :key1
                    OR l.lcode = :key1)
                    INTERSECT
                    SELECT DISTINCT r.*
                    FROM rides r, enroute e, locations l
                    WHERE (r.rno = e.rno
                    AND e.lcode = l.lcode
                    OR r.src = l.lcode
                    OR r.dst = l.lcode)
                    AND (l.city LIKE :key2
                    OR l.prov LIKE :key2
                    OR l.address LIKE :key2
                    OR l.lcode = :key2)
                    INTERSECT
                    SELECT DISTINCT r.*
                    FROM rides r, enroute e, locations l
                    WHERE (r.rno = e.rno
                    AND e.lcode = l.lcode
                    OR r.src = l.lcode
                    OR r.dst = l.lcode)
                    AND (l.city LIKE :key3
                    OR l.prov LIKE :key3
                    OR l.address LIKE :key3
                    OR l.lcode = :key3);
                    '''
    cursor.execute(ride_search,{"key1":key1,"key2":key2,"key3":key3});
    connection.commit()
    return cursor.fetchall()

def post_ride_request(date, pLoc, dLoc, amount, rid, email):
    #Needed for Spec 4
    post_ride =     '''
                    INSERT INTO requests(rid, email, rdate, pickup, dropoff, amount) VALUES
                        (:rid,:email,:date,:pLoc,:dLoc,:amount);
                    '''
    cursor.execute(post_ride,{"rid":rid,"email":email,"date":date,"pLoc":pLoc,"dLoc":dLoc,"amount":amount});
    connection.commit()
    return

def get_ride_requests_by_email(email):
    #Needed for Spec 5
    get_rides =     '''
                    SELECT * FROM requests WHERE email = :email;
                    '''
    cursor.execute(get_rides,{"email":email});
    connection.commit()
    return cursor.fetchall()


def delete_ride_request_by_id(rid):
    #Needed for Spec 5
    delete_rides =      '''
                        DELETE FROM requests WHERE rid = :rid;
                        '''
    cursor.execute(delete_rides,{"rid":rid});
    connection.commit()
    return

def get_requests_by_location(lCode):
    lCodeP = '%'+lCode+'%'
    get_req =     '''
                    SELECT DISTINCT *
                    FROM requests r
                    WHERE r.pickup = :lcode
                    UNION
                    SELECT DISTINCT *
                    FROM requests r
                    WHERE r.pickup IN (SELECT lcode
                                       FROM locations
                                       WHERE city LIKE :lcodeP);
                    '''
    cursor.execute(get_req,{"lcode":lCode,"lcodeP":lCodeP});
    connection.commit()
    return cursor.fetchall()

def get_bookings_by_driver(driverEmail):
    ##Needed for Spec #3
    get_bookings =      '''
                        SELECT b.*
                        FROM bookings b, rides r
                        WHERE r.driver = :driverEmail
                        AND r.rno=b.rno;
                        '''
    cursor.execute(get_bookings,{"driverEmail":driverEmail});
    connection.commit()
    return cursor.fetchall()

def remove_booking_by_id(bno,email,sender,rno):
    ##Needed for Spec #3
    delete_booking =    '''
                        DELETE FROM bookings WHERE bno = :bno;
                        '''
    cursor.execute(delete_booking,{"bno":bno});
    connection.commit()
    send_message_to_member(email,sender,"Your booking has been cancelled",rno)
    return

def get_rides_with_available_seats_by_member(driver):
    ##Needed for Spec #3
    ##Gets all FUTURE rides that the person is offering with how many seats remaining
    get_rides = '''
                SELECT r.rno,(r.seats-IFNULL(SUM(b.seats),0))
                FROM rides r
                LEFT OUTER JOIN bookings b
                ON r.rno=b.rno
                WHERE r.driver=:driver
                AND r.rdate > date('now')
                GROUP BY b.rno

                '''
    cursor.execute(get_rides,{"driver":driver});
    connection.commit()
    return cursor.fetchall()

def check_ride_ownership(email,rno):
    get_owner = '''
                SELECT *
                FROM rides r
                WHERE driver=:email
                AND rno = :rno

                '''
    cursor.execute(get_owner,{"email":email,"rno":rno});
    connection.commit()
    return cursor.fetchone()


def book_member_for_ride(rno,email,seatsBooked,cost,src,dst):
    ##Needed for Spec #3
    bno = get_max_booking_id()[0]+1
    book_member = '''
                INSERT INTO bookings(bno,email,rno,cost,seats,pickup,dropoff) VALUES
                    (:bno,:email,:rno,:cost,:seats,:src,:dst)
                '''
    cursor.execute(book_member,{"bno":bno,"email":email,"rno":rno,"cost":cost,"seats":seatsBooked,"src":src,"dst":dst});
    connection.commit()
    return

def book_member_for_ride_by_driver(rno,email,seatsBooked,cost,src,dst,driver):
    ##Needed for Spec #3
    bno = get_max_booking_id()[0]+1
    book_member = '''
                INSERT INTO bookings(bno,email,rno,cost,seats,pickup,dropoff) VALUES
                    (:bno,:email,:rno,:cost,:seats,:src,:dst)
                '''
    cursor.execute(book_member,{"bno":bno,"email":email,"rno":rno,"cost":cost,"seats":seatsBooked,"src":src,"dst":dst});
    connection.commit()
    send_message_to_member(email,driver,"You have been booked for ride number: {0}".format(rno),rno)
    return



def send_message_to_member(email, sender, content, rno):
    ##Needed for Spec #3
    msgTimestamp = datetime.now();
    seen = 'N'
    send_message =      '''
                        INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) VALUES
                            (:email,:msgTimestamp,:sender,:content,:rno,:seen);
                        '''
    cursor.execute(send_message,{"email":email,"msgTimestamp":msgTimestamp,"sender":sender,"content":content,"rno":rno,"seen":seen});
    connection.commit()
    return

def set_messages_to_seen(email):
    set_seen =  '''
                UPDATE inbox
                SET seen='Y'
                WHERE email=:email;
                '''
    cursor.execute(set_seen,{"email":email});
    connection.commit()
    return

def get_unseen_messages_by_email(email):
    get_unseen = '''
                SELECT *
                FROM inbox
                WHERE email=:email
                AND seen = 'N';
                '''
    cursor.execute(get_unseen,{"email":email});
    connection.commit()
    return cursor.fetchall()

def get_car_by_cno(cno):
    get_car =   '''
                SELECT * FROM cars WHERE cno=:cno;
                '''
    cursor.execute(get_car,{"cno":cno})
    connection.commit()
    return cursor.fetchone()

def get_car_by_driver_cno(cno,driver):
    get_car =   '''
                SELECT * FROM cars WHERE cno=:cno
                AND owner=:driver;
                '''
    cursor.execute(get_car,{"cno":cno,"driver":driver})
    connection.commit()
    return cursor.fetchone()

def get_car_by_driver(driver):
    get_car =   '''
                SELECT * FROM cars WHERE owner=:driver;
                '''
    cursor.execute(get_car,{"driver":driver})
    connection.commit()
    return cursor.fetchone()

def get_max_ride_id():
    get_max = '''
              SELECT MAX(rno) FROM rides r;
              '''
    cursor.execute(get_max)
    connection.commit()
    return cursor.fetchone()

def get_max_request_id():
    get_max = '''
              SELECT MAX(rid) FROM requests r;
              '''
    cursor.execute(get_max)
    connection.commit()
    return cursor.fetchone()

def get_max_booking_id():
    get_max = '''
              SELECT MAX(bno) FROM bookings b;
              '''
    cursor.execute(get_max)
    connection.commit()
    return cursor.fetchone()
