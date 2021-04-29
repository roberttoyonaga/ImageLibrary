from authentication import *
from utils import *


if __name__ == "__main__":
    print("\nImage Library App\n")

    # connect to MySQL server
    HOST = "localhost"
    DATABASE = "photoDB"
    USER = "user"
    PASSWORD = "photoPassword"
    db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    print("Connected to:", db_connection.get_server_info())

    username = ""
    # Step 1: register(a) or access data(b)
    # Step 1a: register - pick username, password, country
    # Step 1b: access data - authenticate yourself
    register_prompt = ""
    while register_prompt != "1" and register_prompt != "2":
        register_prompt = input("Pick and option:\n 1: Register as a user\n 2: Login\n")

    if register_prompt ==  '1':
        username = registration(db_connection)
    elif register_prompt == '2':
        username = authentication(db_connection)

        # does the user want to edit their account?
        edit = ""
        while edit != "1" and edit != "2":
            edit = input("Would you like to edit your account?\n 1: yes\n 2: no \n")
            if edit == "1":
                edit_account(db_connection, username)
            elif edit == "2":
                print("")

    permission_list = user_permissions(db_connection, username)

    # Primary application event loop
    while True:
        # Present user with options based on their permissions
        print("Main Menu: What action would you like to perform?")
        print(" 0 : Exit application")
        for i in range(len(permission_list)):
            print(" {} : {}".format(i + 1, permission_list[i].capitalize()))

        # Ask user to make a selection
        user_selection = input("")

        # Handle non-numeric selections
        try:
            user_selection = int(user_selection)
        except ValueError:
            print("Input must be a number!\n")
            continue

        if (user_selection == 0):
            # exit option
            break
        elif (user_selection < 1 or user_selection > len(permission_list)):
            # user picked something outside of the presented options
            print("Invalid selection. Please try again\n")
        else:
            # valid option selected
            option = permission_list[user_selection - 1]
            print("----------- You have selected {} -----------\n".format(option))

            if option == 'search':
                search(db_connection, username)
            elif option == 'add':
                pass
            elif option == 'delete':
                pass
            elif option == 'edit':
                pass

    print("Application closed. Thank you!")
    db_connection.close()