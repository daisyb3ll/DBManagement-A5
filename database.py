import sqlite3
from helper import helper

class database():
    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path,check_same_thread=False)
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
        self.connection.commit()
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
        self.connection.commit()
        print('MenuItems table Created')

    # function that creates customers table in our database
    def create_Customers_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS Customers(
            customerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            customerName VARCHAR(20),
            customerEmail VARCHAR(20)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Customers table Created')

    # function that creates reservations table in our database
    def create_Reservations_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS Reservations(
            resevationID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            customerID INTEGER,
            reservationDate VARCHAR(20),
            reservationTime VARCHAR(20),
            guestCount INT,
            FOREIGN KEY (customerID) REFERENCES Customers(customerID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('Reservations table Created')

    # function that creates BoardGameOrders table in our database
    def create_BoardGameOrders_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS BoardGameOrders(
            boardGameOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reservationID INTEGER,
            gameID INTEGER,
            isReturned BOOL,
            FOREIGN KEY (reservationID) REFERENCES Reservations(reservationID),
            FOREIGN KEY (gameID) REFERENCES BoardGames(gameID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('BoardGameOrders table Created')    

    # function that creates MenuOrders table in our database
    def create_MenuOrders_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS MenuOrders(
            menuOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            reservationID INTEGER,
            menuItemID INTEGER,
            itemSpecifications VARCHAR(20),
            FOREIGN KEY (reservationID) REFERENCES Reservations(reservationID),
            FOREIGN KEY (menuItemID) REFERENCES MenuItems(menuItemID)
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print('MenuOrders table Created')

    #function to populate a given table with a given filepath
    def populate_table(self, table, filepath):
        if self.is_table_empty(table):
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns_info = self.cursor.fetchall()
            columns = [col[1] for col in columns_info if col[5] != 1]  # col[5] is 'pk' (primary key flag)
            data = helper.data_cleaner(filepath)
            placeholders = ",".join(["?" for _ in columns])
            column_names = ",".join(columns)
            query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
            self.bulk_insert(query, data)
            print(f"Table {table} populated with data from {filepath}.")
        else:
            print(f"Table {table} is already populated. Skipping.")

            # attribute_count = len(columns)
            # placeholders = ("?," * attribute_count)[:-1]
            # column_names = ",".join(columns)
            # query = f"INSERT INTO {table} ({column_names}) VALUES({placeholders})"
            # self.bulk_insert(query, data)

    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()

    # function that returns if given table has records
    def is_table_empty(self, table):
        query = f"SELECT COUNT(*) FROM {table};"
        return self.single_record(query) == 0
        # query = f'''
        # SELECT COUNT(*)
        # FROM "{table}";
        # '''
        # result = self.single_record(query)
        # return result == 0
    
    #Function to create a new customer given the name and email
    def create_new_customer(self, name, email):
        query = f"INSERT INTO Customers (customerName, customerEmail) Values(?, ?)"
        self.cursor.execute(query, (name, email))
        self.connection.commit()

        # query = "INSERT INTO Customers (customerName, customerEmail) VALUES (?, ?)"
        # self.cursor.execute(query, (name, email))
        # self.connection.commit()
        print(f"New customer added: {name} ({email})")

    #Function to return a customerID based on name and email
    def get_customer_id(self, name, email):
        query = '''
        SELECT customerID
        FROM Customers
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
        return self.single_record_params(query, (id,)) > 0
        # result = self.single_record_params(query, (id))
        # return result != 0
    
    def create_new_reservation(self, customerID, reservationDate, reservationTime, guestCount):
        query = '''
        INSERT INTO Reservations (customerID, reservationDate, reservationTime, guestCount)
        VALUES (?, ?, ?, ?)
        '''
        try:
            self.cursor.execute(query, (customerID, reservationDate, reservationTime, guestCount))
            self.connection.commit()
            print(f"New reservation added for customer {customerID} on {reservationDate} at {reservationTime} with {guestCount} guests.")  # Debugging
        except sqlite3.Error as e:
            print(f"Database error: {e}")  # Debugging

    def select_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []


    def __del__(self):
            self.connection.close()
            print("Database connection closed.")