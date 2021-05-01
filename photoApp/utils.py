import mysql.connector as mysql
import shutil
import datetime
from time import gmtime, strftime, ctime
import os
time_format = '%Y-%m-%d %H:%M:%S'

def get_ownerID(db_connection, username):
    cursor = db_connection.cursor()
    cursor.execute("SELECT username, userID FROM Users WHERE username='{}'".format(username))
    ownerID = cursor.fetchone()[1] 
    cursor.close()
    return ownerID

def has_access(cursor, username, ownerID):
    # check if the userID for this username matches the ownerID for the image we are interested in
    cursor.execute("SELECT userID, username FROM Users WHERE username='{}'".format(username))
    
    # there should only be one row  because there is a unique constraint on username
    result_row = cursor.fetchone() 
    if result_row[0]==ownerID:
        return True
    else:
        return False

def search(db_connection, username):
    current_time = strftime(time_format, gmtime())
    directory = "/home/ImageLibrary/images/results_"+current_time
    cursor = db_connection.cursor()
    method = ""
    while method != "1" and method != "2" and method != "3":
        method = input("How sould you like to search?\n 1: By image name\n 2: By tag\n 3: By Date\n 4: Show all images available current user\n")
        if method == "1":
            name = input("Image Name: ")
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos WHERE name='{}'".format(name))
            
            for (name, reference, ownerID, format) in cursor:
                if has_access(cursor, username, ownerID):
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    shutil.copy2(reference, directory+"/"+name+"."+format)
                else:
                    print("Sorry, image could not be found or you do not have access to this image.")
        elif method == "2":

            #Get the desired tags from the user
            print("These are all the available tags")
            cursor.execute("SELECT tagName FROM Tags")
            for (tagName) in cursor:
                print(tagName,"\n")

            requested_tags = input("Add tags separated by spaces: \n").split()

            #compose the query
            query = '''
                SELECT photoID 
                FROM Tags 
                JOIN PhotoTags using(tagID) 
                JOIN Photos using(photoID) 
                GROUP BY photoID
                HAVING 
                SUM(CASE WHEN Photos.ownerID = '{}' THEN 1 ELSE 0 END) > 0 '''.format(get_ownerID(db_connection, username))

            for tag in requested_tags:
                query += " AND SUM(CASE WHEN Tags.tagName = '{}' THEN 1 ELSE 0 END) > 0  ".format(tag)

            query+=";"
            #print("\n\n",query, '\n\n')
            cursor.execute(query)
            matching_photos = []
            for photoID in cursor:
                matching_photos.append(photoID[0])
            
            
            for photoID in matching_photos:
                print("photoID ", photoID)
                cursor.execute("SELECT name, reference, ownerID,format FROM Photos WHERE photoID='{}'".format(photoID))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                for (name, reference, ownerID, format) in cursor:
                    print(name, reference, ownerID, format)
                    shutil.copy2(reference, directory+"/"+name+"."+format)
                
        elif method == "3":
            pass

        elif method == "4":
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos INNER JOIN Users ON Users.userID = Photos.ownerID WHERE username='{}'".format(username))
            print("\nYou have access to these photos:\n")
            for (name, reference, ownerID, format) in cursor:
                print(name, reference, ownerID, format,"\n\n")

    cursor.close()     
    return

def add(db_connection, username):
    reference = input("Absolute path to image in container or volume (/home/ImageLibrary/images): ")
    file=os.path.basename(reference)
    name = os.path.splitext(file)[0]
    format = os.path.splitext(file)[1][1:]
    ownerID = get_ownerID(db_connection, username)
    sizeBytes = os.path.getsize(reference)
    captureTime_ctime =ctime(os.path.getctime(reference))
    captureTime_datetime = datetime.datetime.strptime(captureTime_ctime, "%a %b %d %H:%M:%S %Y").strftime(time_format)


    cursor = db_connection.cursor()

    add_user = ("INSERT INTO Photos (name, reference, sizeBytes,captureDate, ownerID, format) VALUES (%s, %s, %s,%s, %s, %s)")
    data_user = (name, reference, sizeBytes, captureTime_datetime,ownerID, format)
    cursor.execute(add_user, data_user)
    
    db_connection.commit()
    shutil.copy2(reference, "/home/ImageLibrary/images/collection/"+file)
    cursor.close()