from database import *
#Importing data from database

# Creating a database file
database = "TaxiApp.db"

# Connecting to database
conn = create_connection(database)

# If connection to database is failed - Show an error and exit
if not conn:
    print("Error! cannot create the database connection.")
    exit()

# Use the funcions defined in database.py It creates needed tables
create_tables(conn)

#Creating some drivers in case there are none in database
# Using defined function and directly putting data into the table
if (not get_driversNOTDATABASE(conn)):
  company_data = ("CS2020 Taxis Ltd",)
  company_id = create_company(conn, company_data)
  driver_data = ("Mr.", "Eric", "Idle", "haha@lol.com", "xxx", "IOH2421")
  create_driver(conn, driver_data)
  driver_data = ("Mr", "John", "Cleese", "lol@haha.com", "xxx", "FSD1241")
  create_driver(conn, driver_data)
  
  

# No user is logged. Thanks to it the app knows which menu to display (see show_menu)
current_user = None



# Just saying hello and leaving company name
print("Welcome to CS2020 Taxis!")
print(" ")

# Registry. Inserting all demanded data, double checking password, putting data into database
def register():
    global current_user
# Definies global variable for current_user. Below connects inputs with variables
    print(" ")
# Loop where email is checked by it's existence in the database. We create a cursor and a small code that checks if there is anything
# Returned when asked for an email(input) as a client put it in. If the same one exists we recieve a return and then "if" funcion
# Is on. There are options for either going back to login menu or back to the beggining of registration (Which is basically repeating
# Putting email in
# The loop breaks if there is no return (no cursor.Fetchall() result)
    while True:
        email = input("Enter your email:\n")
        with sqlite3.connect('TaxiApp.db') as db:
            cursor = db.cursor()
            check_if_exists = "SELECT * FROM customer WHERE email = ?"
            cursor.execute(check_if_exists, [email])

            if cursor.fetchall():
                try_again = input("[ERROR] Email already exists in the database. Please press 'l' to login, or 't' to try again:\n")
                if try_again in ("l", "L"):
                    login()
                elif try_again in ("t", "T"):
                    register()
                else:
                    print("Invalid anwser. Going back to menu")
                    show_menu()


            else:
                break
                    
    title = input("Enter your title:\n")
    firstname = input("Enter your first name:\n")
    lastname = input("Enter your last name:\n")            
    telno = input("Enter your telephone number:\n")
    password = input("Password: ")
    password2 = input("Confirm your password:")
# Putting all the data in and connecting them to phrases title/firstname/last name etc
    
# A small loop that goes on as long as the passwords do not match. Infinite number of tries. Loop breaks once two passwords are exact

    while(not password==password2):
        print("Password do not match, please try again!\n")
        password = input("Password: ")
        password2 = input("Confirm your password:")
        if password==password2:
            break
    address1 = input("Enter the first line of your address:\n")
    town = input("Enter your town:\n")
    country = input("Enter your country:\n")
    postcode = input("Enter your postcode:\n")
    paymentmethod = input("Enter your paymentmethod:\n")
    


    data = (title, firstname, lastname, email, telno, password, address1, town, country, postcode, paymentmethod)
    current_user = create_customer(conn, data)
# Uses data to put all provided informations into customer table. The order matters depending
# on the way it was definied in database file
    print(" ")
    print("Hello"+" "+firstname+"! Your account has been created.")
    input("Press any key to continue...")
    print(" ")
    show_menu()
# Saying hello to the customer using his/her name (as put in input firstname)
# Creating system of login
def login():
    global current_user
    print(" ")
    email = input("Please enter your email: ")
    password = input("Please enter your password: ")

    data = (email,password)
# Creating set of data (email, password) and comparing them with existing ones in the database
# Trying to create connection:
    try: 
        user = login_customer(conn, data)
        user_id = user[0]
        user_first_name = user[2]
        current_user = user_id
# The login_customer is definied in the database. It searches the customer table and compares
# Email and password with existing ones. If they fit 1==1 then the code proceeds with
# Current_user being set as the one logged in 
    except:
        print(" ")
        print("Bad email or password.")
        print(" ")
        show_menu()
# In case data were not found - print error and go back to menu
    print(" ")
    print(f"Hello {user_first_name}, You are logged in.")    
    input("Press any key to continue...")
    print(" ")
    show_menu()
# Creation of booking
def create_booking():
# Using predefined funcion from database. It shows only the drivers that have no booking and are availible (see database comments)
     drivers = get_drivers(conn)
     print(" ")

          
     
     if not drivers:
             print("\nNo availible drivers! Going back to main menu.\n")
             show_menu()
     else:
             print("Available drivers:")

             for i, driver in enumerate(drivers):
              print(str(i)+"."+str(driver[1])+" "+str(driver[2])+" "+str(driver[3]))   

# The line above demands listing all items from print, exported from drivers table. And then bellow allows to select one 
             print(" ")
             _input = input("Select option: ")
             index = int(_input)
             driver = drivers[index]
             driverid = driver[0]
             customerid = current_user
# Chooses the driver and demands inputs for a trip
             startaddress = input("Enter your pickup address:\n ")
             destinationaddress = input("Enter your destination:\n ")
             date = input("Enter your booking date:\n")
             time = input("Enter the pickup time:\n ")
# Saves data in trip table
             data = (customerid, driverid, startaddress, destinationaddress, date, time)
             trip = create_trip(conn, data)
             print("Booking created!")
             input("Press any key to continue...")
             print(" ")
             show_menu()
         
# After choosing a driver from the listed ones, we create a booking saved in trip table with data
# provided

# We check if there are any bookings assosited with  an user
def show_bookings():
    customerid = current_user
    bookings = get_trips(conn, customerid)
# Allows us to see content of trips table assosiated with customerid
# If bookings is empty
    if not bookings:
        print("No bookings.")
# If not and there is something, then it gets listed with data demanded (3,4 for start and end places)
    else:
        print("Available bookings:")
        for i, booking in enumerate(bookings, 1):
            print(str(i)+". "+str(booking[3])+" -> "+str(booking[4])+" at "+str(booking[6])+" on "+str(booking[5]))
        
    input("Press any key to continue...")
    print(" ")
    show_menu()
# Time to delete bookings
def remove_booking():
    global current_user
    customerid = current_user
    bookings = get_trips(conn, customerid)
# If bookings are empty
    if not bookings:
        print(" ")
        print("No bookings.")
        print(" ")
# If there is something in bookings assosiated with customerid it lists it in form demanded (2 -> 3), then deletes trips assosiaated with customerid
    else:
        print(" ")
        print("Select booking to delete:")
        for i, booking in enumerate(bookings):
            print(str(i)+". "+str(booking[3])+" -> "+str(booking[4]))
        
        _input = input("Select option: ")
        index = int(_input)
        booking = bookings[index]
        bookingid = booking[0]

        delete_trip(conn, bookingid)
        print(" ")
        print("Booking deleted.")
        print(" ")
    print(" ")
    input("Press any key to continue...")
    print(" ")
    show_menu()

# Exits app
def log_out():
    exit()
    
# main menu
def show_menu():
   
      
    if(not current_user):
        print("1.Register")
        print("2.Login")
        print(" ")
# Small loop that makes sure that only demanded options are chosen. Loop is not necessary here, as else function describing any other options would be enough, but i left it as a base for other ideas
        while True:
     
         _input = input("Select option: ")
         print(" ")


        
       
         if _input == "1":
            register()
            False
            
         elif _input == "2":
            login()
            False
         else:
              print(" ")
              print("Please select '1' or '2'")
              print("1.Register")
              print("2.Login")
              print(" ")
              True
        

    else:
        
        print("1.Make Booking")
        print("2.View Bookings")
        print("3.Cancel Booking")
        print("4.Quit")
        print(" ")
        

# Just like above      
        while True:
            
            _input = input("Select option: ")
            print(" ")
            if _input == "1":
                create_booking()
                False

            elif _input == "2":
                show_bookings()
                False

            elif _input == "3":
                remove_booking()
                False
            elif _input == "4":
                log_out()
                False
            else:
                print(" ")
                print("Please choose one of the options:"),
                print("1.Make Booking")
                print("2.View Bookings")
                print("3.Cancel Booking")
                print("4.Exit")
                print(" ")
                True
            

    


show_menu()
