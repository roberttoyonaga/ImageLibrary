import mysql.connector as mysql
import shutil
from time import gmtime, strftime
import os

def HasAccess(cursor, username, ownerID):
    # check if the userID for this username matches the ownerID for the image we are interested in
    cursor.execute("SELECT userID, username FROM Users WHERE username='{}'".format(username))
    
    # there should only be one row  because there is a unique constraint on username
    result_row = cursor.fetchone() 
    if result_row[0]==ownerID:
        return True
    else:
        return False

def search(db_connection, username):
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    cursor = db_connection.cursor()
    method = ""
    while method != "1" and method != "2" and method != "3":
        method = input("How sould you like to search?\n 1: By image name\n 2: By tag\n 3: By Date\n 4: Show all images available current user\n")
        if method == "1":
            name = input("Image Name: ")
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos WHERE name='{}'".format(name))
            
            for (name, reference, ownerID, format) in cursor:
                if HasAccess(cursor, username, ownerID):
                    directory = "/home/ImageLibrary/images/results_"+current_time
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    shutil.copy2(reference, directory+"/"+name+"."+format)
                else:
                    print("Sorry, image could not be found or you do not have access to this image.")
        elif method == "2":
            pass
        elif method == "3":
            pass
        elif method == "4":
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos INNER JOIN Users ON Users.userID = Photos.ownerID WHERE username='{}'".format(username))
            print("\nYou have access to these photos:\n")
            for (name, reference, ownerID, format) in cursor:
                print(name, reference, ownerID, format,"\n\n")
        
    return



