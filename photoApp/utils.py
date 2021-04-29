import mysql.connector as mysql
def HasAccess(db_connection, username, ownerID):
    pass
def search(db_connection, username):
    
    cursor = db_connection.cursor()
    method = ""
    while method != "1" and method != "2" and method != "3":
        method = input("How sould you like to search?\n 1: By image name\n 2: By tag\n 3: By Date \n")
        if method == "1":
            name = input("Image Name: ")
            cursor.execute("SELECT name, reference, ownerID FROM Photos WHERE name='{}'".format(name))
            
            for (_, reference, ownerID) in cursor:
                if HasAccess(db_connection, username, ownerID):
                    pass #do work
                else:
                    print("Sorry, image could not be found or you do not have access to this image.")
        elif method == "2":
            pass
        elif method == "3":
            pass
        
    return



