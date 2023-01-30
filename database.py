import sqlite3
from sqlite3 import Error
# Create connection to database file, print error if connection is not possible. 
def create_connection(db_file):
    """ Connection to database """
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    
    return conn
# Creation of table in sql, error inc case it doesn't work
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
# Create customer. It puts values into demanded parts of a customer table
def create_customer(conn, customer):
    sql = ''' INSERT INTO customer(title, firstname, lastname, email, telno, password, address1, town, country, postcode, paymentmethod)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    conn.commit()
    return cur.lastrowid
# Create driver. It enters provided data into taxidriver table 
def create_driver(conn, taxidriver):
    sql = ''' INSERT INTO taxidriver(title, firstname, lastname, email, password, regno)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, taxidriver)
    conn.commit()
    return cur.lastrowid
# Enters provided data (name) into companies table
def create_company(conn, company):
    sql = ''' INSERT INTO companies(name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, company)
    conn.commit()
    return cur.lastrowid
# Enters data provided into booking table
def create_trip(conn, booking):
    sql = ''' INSERT INTO booking(customerid, driverid, startaddress, destinationaddress, date, time)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, booking)
    conn.commit()
    return cur.lastrowid

# Definition of SQL tables creation. In green all the fields the table has. Name, if text/int, can it be empty.
# Primary key  integer makes sure id is unique and then it can be compared with IDs in other tables the id works as
# both driver and customer id
# Unique doesnt allow for entering the same data twice into the table
# Not Null makes sure that the entry won't be empty
def create_tables(conn):
    sql_create_companies_table = """ CREATE TABLE IF NOT EXISTS companies (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                               ); """
    
    sql_create_drivers_table = """ CREATE TABLE IF NOT EXISTS taxidriver (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        email text UNIQUE,
                                        password text NOT NULL,
                                        regno text NOT NULL
                                    ); """
    
    sql_create_customers_table = """ CREATE TABLE IF NOT EXISTS customer (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        firstname text NOT NULL,
                                        lastname text NOT NULL,
                                        email text UNIQUE NOT NULL,
                                        telno text NOT NULL,
                                        password text NOT NULL,
                                        address1 text NOT NULL,
                                        town text NOT NULL,
                                        country text NOT NULL,
                                        postcode text NOT NULL,
                                        paymentmethod text NOT NULL
                                    ); """

    sql_create_trips_table = """ CREATE TABLE IF NOT EXISTS booking (
                                    id integer PRIMARY KEY,
                                    customerid integer NOT NULL,
                                    driverid integer NOT NULL,
                                    startaddress text NOT NULL,
                                    destinationaddress text NOT NULL,
                                    date text NOT NULL,
                                    time text NOT NULL,
                                    FOREIGN KEY (driverid) REFERENCES drivers (id),
                                    FOREIGN KEY (customerid) REFERENCES customers (id)
                                ); """
    
# create customers table
    create_table(conn, sql_create_customers_table)
# create drivers table
    create_table(conn, sql_create_drivers_table)
# create companies table
    create_table(conn, sql_create_companies_table)
# create trips table
    create_table(conn, sql_create_trips_table)
    
# ===BELOW=== I describe not only the def itself, but also how it cooperates with the code in app
# Selects data from input and (as used in the app) tries to connect with it by checking if data exists and is valid
# Once it is confirmed that it is, the current user changes for the one providing a data and new menu is visible
def login_customer(conn, user):
    sql = ''' SELECT * FROM customer WHERE email=? AND password=?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    first = cur.fetchall()[0] 
    return first

def get_drivers(conn):
    sql = '''SELECT * FROM taxidriver WHERE id NOT IN(SELECT id FROM booking)'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
# This one is a def of function that runs at the start of the app. It creates some dummy drivers if there aren't any
# Had to create it as in the situation where all drivers were not availible (booked trip), get_drivers from above wouldnt be able to
# Create dummies as it wouldn't find anything in the table, but at the same time wouldn't be able to duplicate things - So an error
# Would occur
def get_driversNOTDATABASE(conn):
    sql = ''' SELECT * FROM taxidriver'''
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_trips(conn, customerid):
    sql = ''' SELECT * FROM booking WHERE customerid=?'''
    cur = conn.cursor()
    cur.execute(sql, str(customerid))
    return cur.fetchall()

def delete_trip(conn, customerid):
    sql = 'DELETE FROM booking WHERE customerid=?'
    cur = conn.cursor()
    cur.execute(sql, str(customerid))
    conn.commit()

