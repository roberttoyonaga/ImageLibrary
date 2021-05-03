import mysql.connector as mysql
import shutil
import datetime
from time import gmtime, strftime, ctime
import os
import requests

time_format = '%Y-%m-%d %H:%M:%S'

def get_ownerID(cursor, username):
    cursor.execute("SELECT username, userID FROM Users WHERE username='{}'".format(username))
    ownerID = cursor.fetchone()[1] 
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
    success = False
    while method != "1" and method != "2":
        method = input("How would you like to search?\n 1: By image name\n 2: By tag\n 3: Show all images available current user\n")
        if method == "1":
            name = input("Image Name: ")
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos WHERE name='{}'".format(name))
            
            for (name, reference, ownerID, format) in cursor:
                if has_access(cursor, username, ownerID):
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    shutil.copyfile(reference, directory+"/"+name+"."+format)
                    success = True                    
        elif method == "2":

            #Get the desired tags from the user
            print("These are all the available tags")
            cursor.execute("SELECT tagName FROM Tags")
            for (tagName) in cursor:
                print(tagName,"\n")

            requested_tags = input("Add tags separated by whitespace: \n").split()

            #compose the query
            query = '''
                SELECT photoID 
                FROM Tags 
                JOIN PhotoTags using(tagID) 
                JOIN Photos using(photoID) 
                GROUP BY photoID
                HAVING 
                SUM(CASE WHEN Photos.ownerID = '{}' THEN 1 ELSE 0 END) > 0 '''.format(get_ownerID(cursor, username))

            for tag in requested_tags:
                query += " AND SUM(CASE WHEN Tags.tagName = '{}' THEN 1 ELSE 0 END) > 0  ".format(tag)

            query+=";"
            #print("\n\n",query, '\n\n')
            cursor.execute(query)
            matching_photos = []
            for photoID in cursor:
                matching_photos.append(photoID[0])
            
            if len(matching_photos) > 0:
                success = True
            
            for photoID in matching_photos:
                print("photoID ", photoID)
                cursor.execute("SELECT name, reference, ownerID,format FROM Photos WHERE photoID='{}'".format(photoID))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                for (name, reference, ownerID, format) in cursor:
                    print(name, reference, ownerID, format)
                    shutil.copyfile(reference, directory+"/"+name+"."+format)

        elif method == "3":
            cursor.execute("SELECT name, reference, ownerID,format FROM Photos INNER JOIN Users ON Users.userID = Photos.ownerID WHERE username='{}'".format(username))
            print("\nYou have access to these photos:\n")
            for (name, reference, ownerID, format) in cursor:
                print(name, reference, ownerID, format,"")

    if not success:
        print("Sorry, images could not be found or you do not have access to this image.")
    cursor.close()     
    return

def process_reference(reference):
    file = reference.rsplit('/', 1)[1]
    name = file.split('.')[0]
    format = file.split('.')[1] 
    
    return (file, name, format)

def get_valid_format(format):
    if format=="jpg" or format=="JPG" or format=="jpeg" or format=="JPEG":
        return "jpg"
    elif format=="PNG" or format=="png":
        return "png"
    else:
        return None
    
    

def add(db_connection, username):
    cursor = db_connection.cursor()
    collection_dest = "/home/ImageLibrary/images/collection/"
    ownerID = get_ownerID(cursor, username)

    #add image
    method = ""
    retry = False
    while method != "1" and method != "2" or retry:
        if not retry:
            method = input("\nHow would you like to add?\n 1: From local machine\n 2: From URL\n")
        if method == "1":
            print("\nImages to add should be put inside the images/images_to_add directory because this is the volume mounted on the docker container")
            reference = "/home/ImageLibrary/images/images_to_add/"+input("Image name (ie. my_image.png): ")
            if not os.path.isfile(reference):
                print("Please ensure this file exists")
                retry = True 
                continue 

            (file, name, format) = process_reference(reference)
            if get_valid_format(format) == None:
                print("Sorry, currently only .png and .jpg files are supported.\n")
                retry = True     
                continue   
            retry = False
            sizeBytes = os.path.getsize(reference)
            captureTime_ctime =ctime(os.path.getctime(reference))
            captureTime_datetime = datetime.datetime.strptime(captureTime_ctime, "%a %b %d %H:%M:%S %Y").strftime(time_format)

            add_image = ("INSERT INTO Photos (name, reference, sizeBytes,captureDate, ownerID, format) VALUES (%s, %s, %s,%s, %s, %s)")
            data_image = (name, collection_dest+file, sizeBytes, captureTime_datetime,ownerID, format)
            cursor.execute(add_image, data_image)

            #copy the file into the collections directory
            shutil.copyfile(reference, "/home/ImageLibrary/images/collection/"+file)
    
        if method == "2":
            url = input("Provide the image URL: ")
            
            r = None
            try:
                r = requests.get(url, allow_redirects=True)
            except:
                print("Sorry, that URl does not seem to be valid\n")
                method = "-1"
                continue
            

            (file, name, format) = process_reference(url)
            if get_valid_format(format) == None:
                print("Sorry, currently only .png and .jpg files are supported.\n")
                method = "-1"  
                continue      

            open(collection_dest+file, 'wb').write(r.content)
            sizeBytes = os.path.getsize(collection_dest+file)

            add_image = ("INSERT INTO Photos (name, reference, sizeBytes,captureDate, ownerID, format) VALUES (%s, %s, %s,%s, %s, %s)")
            data_image = (name, collection_dest+file, sizeBytes, None, ownerID, format)
            cursor.execute(add_image, data_image)

    db_connection.commit()
    

    # add tags
    tags = input("\nAdd tags separated by whitespace: \n")
    if tags == "":
        cursor.close()
        return

    tags = tags.split()
    for tag in tags:
        # Update tag table
        cursor.execute("SELECT tagName, tagID FROM Tags WHERE tagName='{}'".format(tag))
        result_row = cursor.fetchone()
        tagID = ""

        # tag is new
        if result_row is None: 
            print("adding new tags to the Tags table", tag)
            cursor.execute("INSERT INTO Tags (tagName) VALUES ('{}')".format(tag))
            db_connection.commit()
            cursor.execute("SELECT tagName, tagID FROM Tags WHERE tagName='{}'".format(tag))
            tagID = cursor.fetchone()[1]
        # tag already exists
        else:
            tagID = result_row[1]

        #add tuple to PhotoTags
        cursor.execute("SELECT photoID FROM Photos WHERE name='{}'".format(name))
        photoID = cursor.fetchone()[0]

        query = "INSERT INTO PhotoTags (tagID, photoID) VALUES (%s, %s)"
        cursor.execute(query, (tagID, photoID))
        db_connection.commit()

    cursor.close()