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
            isVegan BOOL,
            isGlutenFree BOOL,
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
            customerEmail VARCHAR(20),
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

    # function that returns if given table has records
    def is_table_empty(self, table):
        query = f'''
        SELECT COUNT(*)
        FROM "{table}";
        '''
        result = self.single_record(query)
        return result == 0