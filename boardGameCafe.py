# imports
from helper import helper
from database import database

# global variables
db_ops = database("cafe.db")

def options():
    print('''Would you like to
            1. Sign In
            2. Create Account
            3. Exit''')
    return helper.get_choice([1,2,3])

# user wants to create an account
def create_account():
    new_name = input("Please enter your name:\n")
    new_email = input("Please enter you email:\n")
    db_ops.create_new_customer(new_name, new_email)
    print("Your ID is: " + str(db_ops.get_id()))
    print("Save this!! You will use it to log in!")

# user wants to sign in
def user_menu():
    # Ask for ID and email to log in
    print("What is your ID number?")
    entered_id = input("ID Number: ")

    # Check to see if ID number is valid and log in
    IDvalidity = db_ops.check_id(entered_id)

    if IDvalidity:
        signed_in = True
        while signed_in:
            choice = menu_options()
            if choice == 1:
                view_menu()
            if choice == 2:
                view_board_games()
            if choice == 3:
                make_reservation(entered_id)
            if choice == 4:
                view_reservations(entered_id)
            if choice == 5:
                account_info(entered_id)
    else:
        print("Not a valid ID number. Try logging in with a valid one.")

# options on main screen
def menu_options():
    print('''Where would you like to go?
            1. Menu
            2. Board Games
            3. Reserve
            4. Reservations
            5. Account
          ''')
    return helper.get_choice([1,2,3,4.5])

# user wants to view_menu
def view_menu():
    print("Here is a list of all our drinks!")
    # show the menu
    food_menu_query = f"""
    SELECT *
    FROM MenuItems;
    """
    items = db_ops.select_query(food_menu_query)
    helper.pretty_print(items)

# user wants to view board games
def view_board_games():
    print("Here is a list of all our games!")
    # show board game menu
    game_menu_query = f"""
    SELECT *
    FROM BoardGames;
    """
    games = db_ops.select_query(game_menu_query)
    helper.pretty_print(games)

def make_reservation(id):

    # asks for reservation date
    failed = True
    while failed:
        failed = False
        reserve_date = input("What day would you like to make a reservation? (YYYY-MM-DD)\n")
        if len(reserve_date) != 10:
            failed = True
        else:
            for i in range(len(reserve_date)):
                if i == 4 or i == 7:
                    if reserve_date[i] != '-':
                        failed = True
                else:
                    try:
                        int(reserve_date[i])
                    except:
                        failed = True
        if failed == False:
            if int(reserve_date[:4]) < 2024 or int(reserve_date[5:7]) > 12 or int(reserve_date[8:]) > 30:
                failed = True
        if failed:
            print("Invalid entry. Please enter a valid date in the correct format (YYYY-MM-DD)")

    # asks for reservation time
    failed = True
    while failed:
        failed = False
        reserve_time = input("What time would you like your reservation to be? (##:##)\n")
        if len(reserve_time) != 5:
            failed = True
        else:
            if reserve_time[2] != ':':
                failed = True
            else:
                try:
                    if int(reserve_time[:2]) > 23 or int(reserve_time[3:]) > 59:
                        failed = True
                except:
                    failed = True
        if failed:
            print("Invalid entry. Please enter a valid time in the correct format")

    # asks for guest number
    failed = True
    while failed:
        failed = False
        guest_amount = input("How many people will there be (including yourself)\n")
        try:
            int(guest_amount)
        except:
            failed = True
        if failed:
            print("Invalid. Please enter an integer")

    # allows them to pre-order drinks
    # print("Would you like to order drinks ahead of time?\n")
    # print('''1. Yes
    #          2. No
    #          ''')
    # if helper.get_choice([1,2]) == 1:
        
    #print("Would you like to reserve a game?")
    #print("What game would you like to reserve?")

    # adds new reservation to table
    db_ops.create_new_reservation(id, reserve_date, reserve_time, guest_amount)

# allows user to view their reservations
def view_reservations(id):
    reservations_query = f'''
    SELECT Reservation.reservationDate, Reservation.reservationTime, Reservation.guestCount, (
        SELECT SUM(MenuItems.MenuItemPrice)
        FROM MenuOrders
        INNER JOIN MenuItems on MenuOrders.menuItemID = MenuItems.menuItemID
        WHERE MenuOrders.reservationID = ?)
    FROM Reservation
    WHERE customerID LIKE "{id}";
    '''
    results = db_ops.select_query(reservations_query)
    print("Here are all of your reservations:\n")
    helper.pretty_print(results)

#main method
#db_ops.create_Customers_table()
#db_ops.create_BoardGames_table()
#db_ops.create_MenuItems_table()
#db_ops.create_Reservations_table()
#db_ops.create_BoardGameOrders_table()
#db_ops.create_MenuOrders_table()

db_ops.populate_table("Customers", "Customers.csv")
db_ops.populate_table("BoardGames", "BoardGames.csv")
db_ops.populate_table("MenuItems", "MenuItems.csv")
db_ops.populate_table("Reservations", "Reservations.csv")
db_ops.populate_table("BoardGameOrders", "BoardGameOrders.csv")
db_ops.populate_table("MenuOrders", "MenuOrders.csv")

#testing
db_ops.create_new_customer("alex", "lark@chapman.edu")
print(db_ops.get_customer_id("alex", "lark@chapman.edu"))
print(db_ops.check_customer_id("1"))
print (db_ops.get_reservation_details(1))

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
