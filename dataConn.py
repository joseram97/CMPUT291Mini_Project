import sqlite3
import datetime
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


def drop_tables():
    global connection, cursor

    drop_course = "DROP TABLE IF EXISTS course; "
    drop_student = "DROP TABLE IF EXISTS student; "
    drop_enroll = "DROP TABLE IF EXISTS enroll; "

    cursor.execute(drop_enroll)
    cursor.execute(drop_student)
    cursor.execute(drop_course)


def define_tables():
    global connection, cursor

    course_query = '''
                        CREATE TABLE course (
                                    course_id INTEGER,
                                    title TEXT,
                                    seats_available INTEGER,
                                    PRIMARY KEY (course_id)
                                    );
                    '''

    student_query = '''
                        CREATE TABLE student (
                                    student_id INTEGER,
                                    name TEXT,
                                    PRIMARY KEY (student_id)
                                    );
                    '''

    enroll_query = '''
                    CREATE TABLE enroll (
                                student_id INTEGER,
                                course_id INTEGER,
                                enroll_date DATE,
                                PRIMARY KEY (student_id, course_id),
                                FOREIGN KEY(student_id) REFERENCES student(student_id),
                                FOREIGN KEY(course_id) REFERENCES course(course_id)
                                );
                '''

    cursor.execute(course_query)
    cursor.execute(student_query)
    cursor.execute(enroll_query)
    connection.commit()

    return


def insert_data():
    global connection, cursor

    insert_courses =    '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                        '''

    insert_students =       '''
                            INSERT INTO student(student_id, name) VALUES
                                    (1509106, 'Jeff'),
                                    (1409106, 'Alex'),
                                    (1609106, 'Mike');
                            '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return



##TODO: Make Enroute do something! it should add to the enroute table
def offer_ride(date,driver,seats,price,desc,src,dst,cno,enroute):
    ##TODO Check that cno belongs to the driver
    ##TODO: enroute can be a list of locations. Need to factor that in
    ##Needed for spec 1
    rno = get_max_ride_id()[0] + 1
    offer_ride=     '''
                    INSERT INTO rides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno) VALUES
                        (:rno,:price,:date,:seats,:desc,:src,:dst,:driver,:cno);
                    '''
    cursor.execute(offer_ride,{"rno":rno,"price":price,"date":date,"seats":seats,"desc":desc,"src":src,"dst":dst,"driver":driver,"cno":cno});
    connection.commit()
    return


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


#Returns all locations by lCode
def get_locations_by_location_code(lCode):
    get_locations =     '''
                        SELECT * FROM locations WHERE lcode = :lcode;
                        '''
    cursor.execute(get_locations,{"lcode":lCode});
    connection.commit()
    return cursor.fetchone()

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
                    SELECT DISTINCT r.rno, r.dst, r.src
                    FROM rides r, enroute e, locations l1, locations l2, locations l3
                    WHERE (r.rno = e.rno
                    AND e.lcode = l3.lcode
                    AND r.src = l1.lcode
                    AND r.dst = l2.lcode)
                    AND (l1.city LIKE :key1
                    OR l2.city LIKE :key1
                    OR l3.city LIKE :key1
                    OR l1.prov LIKE :key1
                    OR l2.prov LIKE :key1
                    OR l3.prov LIKE :key1
                    OR l1.address LIKE :key1
                    OR l2.address LIKE :key1
                    OR l3.address LIKE :key1);
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
    # these were the other parameters date, pLoc, dLoc, amount, rid,
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
                    SELECT DISTINCT r.rid, r.pickup, r.dropoff
                    FROM requests r
                    WHERE r.pickup = :lcode
                    UNION
                    SELECT DISTINCT r.rid, r.pickup, r.dropoff
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

def remove_booking_by_id(bno):
    ##Needed for Spec #3
    delete_booking =    '''
                        DELETE FROM bookings WHERE bno = :bno;
                        '''
    cursor.execute(delete_rides,{"bno":bno});
    connection.commit()
    return

def get_rides_with_available_seats_by_member(driver):
    ##Needed for Spec #3
    ##Gets all FUTURE rides that the person is offering with how many seats remaining
    get_rides = '''
                SELECT r.rno,(r.seats-SUM(IFNULL(b.seats,0)))
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

def book_member_for_ride(rno,email,seatsBooked,cost,src,dst):
    ##Needed for Spec #3
    bno = get_max_booking_id()[0]
    book_member = '''
                INSERT INTO bookings(bno,email,rno,cost,seats,pickup,dropoff) VALUES
                    (:bno,:email,:rno,:cost,:seats,:src,:dst)
                '''
    cursor.execute(book_member,{"bno":bno,"email":email,"rno":rno,"cost":cost,"src":src,"dst":dst});
    connection.commit()
    return



def send_message_to_member(email, sender, content, rno):
    ##Needed for Spec #3
    msgTimestamp = datetime.now().strftime('%Y-%m-%d');
    seen = 'N'
    send_message =      '''
                        INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) VALUES
                            (:email,:msgTimestamp,:sender,:content,:rno,:seen);
                        '''
    cursor.execute(send_message,{"email":email,"msgTimestamp":msgTimestamp,"sender":sender,"content":content,"rno":rno,"seen":seen});
    connection.commit()
    return

def set_message_to_seen(email,msgTimestamp):
    set_seen =  '''
                UPDATE inbox
                SET seen='Y'
                WHERE email=:email
                AND msgTimestamp=:msgTimestamp;
                '''
    cursor.execute(set_seen,{"email":email,"msgTimestamp":msgTimestamp});
    connection.commit()
    return

def get_car_by_cno(cno):
    get_car =   '''
                SELECT * FROM cars WHERE cno=:cno;
                '''
    cursor.execute(get_car,{"cno":cno})
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
