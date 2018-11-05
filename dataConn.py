import sqlite3

#this is the data class that will hold all of the information for the
# mini-project

#The following is all code from the lab that I did for getting the data
# from the tables
connection = None
cursor = None

def connect(path):
    global connection, cursor

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
    ##Needed for spec 1
    rno = get_max_ride_id()[0] + 1
    offer_ride=     '''
                    INSERT INTO rides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno) VALUES
                        (:rno,:price,:date,:seats,:desc,:src,:dst,:driver,:cno);
                    '''
    cursor.execute(send_message,{"rno":rno,"price":price,"date":date,"seats":seats,"desc":desc,"src":src,"dst":dst,"driver":driver,"cno":cno});
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
def search_for_rides(key1,key2,key3):
    key1 = '%'+key1+'%'
    key2 = '%'+key2+'%'
    key3 = '%'+key3+'%'

    ride_search =   '''
                    SELECT DISTINCT r.*
                    FROM rides r, enroute e, locations l
                    WHERE r.rno = e.rno
                    AND l.lCode = e.lCode
                    AND l.city LIKE :key1
                    OR l.prov LIKE :key1
                    OR l.address LIKE :key1
                    INTERSECT
                    SELECT DISTINCT r.*
                    FROM rides r, locations l
                    WHERE r.src = l.lCode
                    AND l.city LIKE :key2
                    OR l.prov LIKE :key2
                    OR l.address LIKE :key2
                    INTERSECT
                    SELECT DISTINCT r.*
                    FROM rides r, locations l
                    WHERE r.dst = l.lCode
                    AND l.city LIKE :key3
                    OR l.prov LIKE :key3
                    OR l.address LIKE :key3;
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

def get_ride_requests_by_email(date, pLoc, dLoc, amount, rid, email):
    #Needed for Spec 5
    get_rides =     '''
                    SELECT * FROM requests WHERE email = :email;
                    '''
    cursor.execute(get_rides,{"email":email});
    connection.commit()
    return


def delete_ride_by_id(rid):
    #Needed for Spec 5
    delete_rides =      '''
                        DELETE FROM requests WHERE rid = :rid;
                        '''
    cursor.execute(delete_rides,{"rid":rid});
    connection.commit()
    return

def get_requests_by_location(lCode):
    ##TODO: see spec number 5 for details
    return

def remove_booking_by_id(bno):
    ##Needed for Spec #3
    delete_booking =    '''
                        DELETE FROM bookings WHERE bno = :bno;
                        '''
    cursor.execute(delete_rides,{"bno":bno});
    connection.commit()
    return

def get_rides_by_member(driver):
    ##Needed for Spec #3
    get_rides = '''
                SELECT b.* FROM rides r, bookings b,
                WHERE r.driver=:driver
                AND r.rno=b.rno;
                '''
    cursor.execute(get_rides,{"driver":driver});
    connection.commit()
    return

def send_message_to_member(email, msgTimestamp, sender, content, rno, seen):
    ##Needed for Spec #3
    send_message =     '''
                    INSERT INTO inbox(email, msgTimestamp, sender, content, rno, seen) VALUES
                        (:email,:msgTimestamp,:sender,:content,:rno,:seen);
                    '''
    cursor.execute(send_message,{"email":email,"msgTimestamp":msgTimestamp,"sender":sender,"content":content,"rno":rno,"seen":seen});
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

def main():
    #######################
    ## SQL TESTING TODOS ##
    #######################
    ##TEST ALL SQL QUERYS##
    ##POST SUCCESSES HERE##
    #######################
    return

if __name__ == "__main__":
    main()
