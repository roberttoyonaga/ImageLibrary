from getpass import getpass
import mysql.connector as mysql


def edit_account(db_connection, username):
    """
    Allows user to change password or delete account. If account deleted, exits application.

    Parameters
    ----------
    db_connection : mysql.connector object
    username : username for current user
    """
    action = ""
    while action != "1" and action != "2":
        action = input("Pick an option: \n 1: Change password\n 2: Delete account \n")

    cursor = db_connection.cursor()

    if action == "1":
        # ask user to input a valid new password
        new_password = ""
        valid_password = False
        while not valid_password:
            valid_password = True
            new_password =  getpass(prompt="Enter new password: ")
            if len(new_password) < 5 or len(new_password) > 20:
                valid_password = False
                print("Password must be between 5-10 letters\n")

        query = "UPDATE Users SET password=%s WHERE username=%s"
        cursor.execute(query, (new_password, username))
        db_connection.commit()
        print("Password changed\n")
    elif action == "2":
        cursor.execute("DELETE FROM Users WHERE username='{}'".format(username))
        db_connection.commit()
        print("Account deleted\n")
        exit(0)


def registration(db_connection):
    """
    Walks user through registration process.

    Parameters
    ----------
    db_connection : mysql.connector object

    Returns
    -------
    username: registered username
    """
    cursor = db_connection.cursor()

    username = ""
    valid_username = False

    while not valid_username:
        valid_username = True
        username = input("Create username: ")

        # ensure valid length
        if len(username) < 5 or len(username) > 20:
            valid_username = False
            print("Username must be between 5-10 letters\n")
            continue

        # ensure unique
        query = ("SELECT username FROM Users WHERE username=%s %s")
        cursor.execute(query, (username, ""))

        for (ret_username) in cursor:
            valid_username = False
            print("Username already exists\n")

    user_password = ""
    valid_password = False
    while not valid_password:
        valid_password = True
        user_password =  getpass(prompt="Create password: ")
        if len(user_password) < 5 or len(user_password) > 20:
            valid_password = False
            print("Password must be between 5-10 letters\n")

    user_type = ""
    while user_type != "1" and user_type != "2":
        user_type =  input("What user type?\n 1: admin \n 2: individual \n")
    if user_type == "1":
        user_type= "admin"
    elif user_type == "2":
        user_type = "individual"
        
    # add info to DB
    add_user = ("INSERT INTO Users "
                "(username, password, userType) "
                "VALUES (%s, %s, %s)")
    data_user = (username, user_password, user_type)
    cursor.execute(add_user, data_user)

    # Make sure data is committed to the database
    db_connection.commit()

    cursor.close()

    print("--- Thank you for registering! ---\n")
    return username


def authentication(db_connection):
    """
    Prompts user for username & password in order to sign in.

    Parameters
    ----------
    db_connection : mysql.connector object

    Returns
    -------
    username: registered username
    """
    cursor = db_connection.cursor()
    success = False

    while not success:
        # get input for user
        username = input("Username: ")
        user_password =  getpass("Password: ")

        # set up query
        query = ("SELECT username, password FROM Users "
                "WHERE username=%s AND password=%s ")
        cursor.execute(query, (username, user_password))
        result_row = cursor.fetchone()
        if result_row is None:
            print("Login failed")
        elif result_row[0]==username and result_row[1] == user_password:
            success = True
        else:
            print("Login failed")

    print("Login success\n")
    cursor.close()
    return username


def user_permissions(db_connection, username):
    """
    Checks user type and returns permissions

    Parameters
    ----------
    db_connection : mysql.connector object
    username : registered username

    Returns
    -------
    result: array of permissions available to use
    """
    cursor = db_connection.cursor()
    result = []

    # find this user in db
    cursor.execute("SELECT username,userType FROM Users WHERE username='{}'".format(username))

    for (_, user_type) in cursor:
        if user_type == "admin":
            result = ["search", "add", "delete", "edit"]
        elif user_type == "individual":
            result = ["search"]

    return result