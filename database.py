import sqlite3
from helper import helper

class db_operations():

    # constructor with connection path to DB
    def __init__(self, conn_path):
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

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
