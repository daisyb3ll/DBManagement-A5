# imports
from helper import helper
from database import database

# global variables
db_ops = database("cafe.db")

# start screen
# user can 
    # make reservation
    # order food
    # order board game
    # view past orders

# main menu
    # sign in
    # create acct

def options():
    print('''Would you like to
            1. Sign In
            2. Create Account
            3. Exit''')
    return helper.get_choice([1,2,3])

def create_account():
    new_name = input("Please enter your name:\n")
    new_email = input("Please enter you email:\n")
    db_ops.create_new_customer(new_name, new_email)
    print("Your ID is: " + str(db_ops.get_id()))
    print("Save this!! You will use it to log in!")

def user_menu():
    # Ask for ID and email to log in
    print("What is your ID number?")
    entered_id = input("ID Number: ")

    # Check to see if ID number is valid and log in
    IDvalidity = db_ops.check_id(entered_id)

    if IDvalidity:
        while True:
            choice = menu_options()

#def menu_options():

# User wants to order food
def order_food():
    # show the menu
    food_menu_query = f"""
    SELECT *
    FROM MenuItems;
    """
    items = db_ops.select_query(food_menu_query)
    helper.pretty_print(items)

def order_board_game():
    # board game menu
    game_menu_query = f"""
    SELECT *
    FROM BoardGames;
    """
    games = db_ops.select_query(game_menu_query)
    helper.pretty_print(games)

#def make_reservation():

#main method
#db_ops.create_Customers_table()
#db_ops.create_BoardGames_table()
#db_ops.create_MenuItems_table()
#db_ops.create_Reservations_table()
#db_ops.create_BoardGameOrders_table()
#db_ops.create_MenuOrders_table()

#testing
db_ops.create_new_customer("alex", "lark@chapman.edu")
print(db_ops.get_customer_id("alex", "lark@chapman.edu"))
print(db_ops.check_customer_id("1"))

while True:
    user_choice = options()
    if user_choice == 1:
        user_menu()
    if user_choice == 2:
        create_account()
    if user_choice == 3:
        print("Bye bye! Come again soon!")
        break

db_ops.destructor()
