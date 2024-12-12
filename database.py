import sqlite3
from helper import helper

class database():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]

    # function that creates BoardGames table in our database
    def create_BoardGames_table(self):
        query = '''
        CREATE TABLE BoardGames(
            gameID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            gameName VARCHAR(20),
            gameGenre VARCHAR(20),
            MinPlayers INTEGER,
            MAXPLAYERS INTEGER,
            isAvailable BOOL
        );
        '''
        self.cursor.execute(query)
        print('BoardGames table Created')

    # function that creates Menu table in our database
    def create_MenuItems_table(self):
        query = '''
        CREATE TABLE MenuItems(
            MenuItemsID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            MenuItemName VARCHAR(20),
            MenuItemPrice DOUBLE,
            isVegan BOOL
        );
        '''
        self.cursor.execute(query)
        print('MenuItems table Created')

    # function that creates customers table in our database
    def create_Customers_table(self):
        query = '''
        CREATE TABLE Customers(
            customerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            customerName VARCHAR(20),
            customerEmail VARCHAR(20)
        );
        '''
        self.cursor.execute(query)
        print('Customers table Created')

    # function that creates reservations table in our database
    def create_Reservations_table(self):
        query = '''
        CREATE TABLE Reservation(
            resevationID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            customerID INTEGER,
            reservationDate VARCHAR(20),
            reservationTime VARCHAR(20),
            guestCount INT,
            FOREIGN KEY (customerID) REFERENCES Customers(customerID)
        );
        '''
        self.cursor.execute(query)
        print('Reservations table Created')

    # function that creates BoardGameOrders table in our database
    def create_BoardGameOrders_table(self):
        query = '''
        CREATE TABLE BoardGameOrders(
            boardGameOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reservationID INTEGER,
            gameID INTEGER,
            isReturned BOOL,
            FOREIGN KEY (reservationID) REFERENCES Reservations(reservationID),
            FOREIGN KEY (gameID) REFERENCES BoardGames(gameID)
        );
        '''
        self.cursor.execute(query)
        print('BoardGameOrders table Created')    

    # function that creates MenuOrders table in our database
    def create_MenuOrders_table(self):
        query = '''
        CREATE TABLE MenuOrders(
            menuOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reservationID INTEGER,
            menuItemID INTEGER,
            itemSpecifications VARCHAR(20),
            FOREIGN KEY (reservationID) REFERENCES Reservations(reservationID),
            FOREIGN KEY (menuItemID) REFERENCES MenuItems(menuItemID)
        );
        '''
        self.cursor.execute(query)
        print('MenuOrders table Created')

    #function to populate a given table with a given filepath
    def populate_table(self, table, filepath):
        if self.is_table_empty(table):
            data = helper.data_cleaner(filepath)
            attribute_count = len(data[0])
            placeholders = ("?,"*attribute_count)[:-1]
            query = f"INSERT INTO {table} VALUES("+placeholders+")"
            self.bulk_insert(query, data)

    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    # function that returns if given table has records
    def is_table_empty(self, table):
        query = f'''
        SELECT COUNT(*)
        FROM "{table}";
        '''
        result = self.single_record(query)
        return result == 0
    
    #Function to create a new customer given the name and email
    def create_new_customer(self, name, email):
        query = f"INSERT INTO Customers (customerName, customerEmail) Values(?, ?)"
        self.cursor.execute(query, (name, email))

    #Function to return a customerID based on name and email
    def get_customer_id(self, name, email):
        query = '''
        SELECT customerID
        FROM customers
        WHERE customerName LIKE ? AND customerEmail LIKE ?;
        '''
        return self.single_record_params(query, (name, email))
    
    #Function to check if an ID exists in the customers table
    def check_customer_id(self, id):
         query = f'''
            SELECT COUNT(*)
            FROM customers
            WHERE customerID = ?
            '''
         result = self.single_record_params(query, (id))
         return result != 0
    
    def create_new_reservation(self, customerID, reservationDate, reservationTime, guestCount):
        query = f"INSERT INTO Reservations (customerID, reservationDate, reservationTime, guestCount) Values(?, ?, ?, ?)"
        self.cursor.execute(query, (customerID, reservationDate, reservationTime, guestCount))
    
    def create_new_reservation(self, customerID, reservationDate, reservationTime, guestCount):
        query = f"INSERT INTO Reservations (customerID, reservationDate, reservationTime, guestCount) Values(?, ?, ?, ?)"
        self.cursor.execute(query, (customerID, reservationDate, reservationTime, guestCount))
