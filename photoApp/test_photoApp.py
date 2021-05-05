import unittest
import sys
sys.path.insert(0, "/home/ImageLibrary/photoApp")
from authentication import *
from utils import *

class TestReferenceProcessing(unittest.TestCase):

    def test_URL_processing(self):
        self.assertEqual(process_reference("https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png"), ("025.png", "025", "png"), "URL processing failed")
    def test_path_processing(self):
        self.assertEqual(process_reference("/home/somefolder/image.PNG"), ("image.PNG", "image", "PNG"), "URL processing failed")
    
    def test_format_processing(self):
        self.assertEqual(get_valid_format("png"), "png", "format processing failed")
        self.assertEqual(get_valid_format("PNG"), "png", "format processing failed")
        self.assertEqual(get_valid_format("JPG"), "jpg", "format processing failed")
        self.assertEqual(get_valid_format("jpeg"), "jpg", "format processing failed")
        self.assertEqual(get_valid_format("abc"), None, "Should indicate incorrect format")

class TestDatabase(unittest.TestCase):

    # def test_get_ownerID(self): # dependent on state of Users table
    #     HOST = "localhost"
    #     DATABASE = "photoDB"
    #     USER = "user"
    #     PASSWORD = "photoPassword"
    #     db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    #     cursor = db_connection.cursor()

    #     ownerID = get_ownerID(cursor, "default_user")
    #     self.assertEqual(ownerID, 1, "Getting photo ownerID failed")
    #     cursor.close()

    def test_login(self):
        HOST = "localhost"
        DATABASE = "photoDB"
        USER = "user"
        PASSWORD = "photoPassword"
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = db_connection.cursor()
        
        # Add dummy test user
        test_username = "test_user_99"
        test_password = "password"

        add_user = ("INSERT INTO Users "
                    "(username, password, userType) "
                    "VALUES (%s, %s, %s)")
        data_user = (test_username, hash_password(test_password), "admin")
        cursor.execute(add_user, data_user)
        db_connection.commit()

        self.assertEqual(login_successful(cursor, test_username, test_password), True, "Valid login failed")
        self.assertEqual(login_successful(cursor, "random_999!*&281", "abc"), False, "Short password login should fail")
        self.assertEqual(login_successful(cursor, test_username, "incorrect_5"), False, "Incorrect password login should fail")

        #delete the test user's account
        cursor.execute("DELETE FROM Users WHERE username='{}'".format(test_username))
        db_connection.commit()

        cursor.close()

    def test_add_tags(self):
        HOST = "localhost"
        DATABASE = "photoDB"
        USER = "user"
        PASSWORD = "photoPassword"
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = db_connection.cursor()

        # Add dummy test user
        test_username = "test_user_99"
        test_password = "password"

        add_user = ("INSERT INTO Users "
                    "(username, password, userType) "
                    "VALUES (%s, %s, %s)")
        data_user = (test_username, hash_password(test_password), "admin")
        cursor.execute(add_user, data_user)
        db_connection.commit()
        

        #make a dummy image to add tags to 
        dummy_image_name = "test_add_tags"
        add_image = ("INSERT INTO Photos (name, reference, sizeBytes,captureDate, ownerID, format) VALUES (%s, %s, %s,%s, %s, %s)")
        data_image = (dummy_image_name, "/fake/reference/{}".format(dummy_image_name),None,  None, get_ownerID(cursor, test_username), "png")
        cursor.execute(add_image, data_image)
        db_connection.commit()
        cursor.close()
        
        # check if tags got added correctly
        add_tags(db_connection,"tag1 tag2 tag3",dummy_image_name)
        
        cursor = db_connection.cursor()
        success = True
        cursor.execute("SELECT tagName FROM Tags WHERE tagName='tag1'")
        result_row = cursor.fetchone()
        if result_row == None:
            success = False

        cursor.execute("SELECT tagName FROM Tags WHERE tagName='tag2'")
        result_row = cursor.fetchone()
        if result_row == None:
            success = False
        cursor.execute("SELECT tagName FROM Tags WHERE tagName='tag3'")
        result_row = cursor.fetchone()
        if result_row == None:
            success = False

        self.assertEqual(success, True, "Tags did not get added to Tags table correclty")

        #check if tags got associated with corrcect image
        cursor.execute("SELECT photoID, name FROM Photos WHERE name='{}'".format(dummy_image_name))

        dummy_photoID = cursor.fetchone()[0]

        #compose the query
        query = '''
            SELECT photoID 
            FROM Tags 
            JOIN PhotoTags using(tagID) 
            JOIN Photos using(photoID) 
            GROUP BY photoID
            HAVING 
            SUM(CASE WHEN Photos.ownerID = '{}' THEN 1 ELSE 0 END) > 0 
            AND SUM(CASE WHEN Tags.tagName = 'tag1' THEN 1 ELSE 0 END) > 0 
            AND SUM(CASE WHEN Tags.tagName = 'tag2' THEN 1 ELSE 0 END) > 0 
            AND SUM(CASE WHEN Tags.tagName = 'tag3' THEN 1 ELSE 0 END) > 0 ;'''.format(get_ownerID(cursor, test_username))

        cursor.execute(query)
        matching_photos = []
        success = False
        for photoID in cursor:
            print(photoID[0],dummy_photoID)
            if photoID[0] == dummy_photoID:
                success = True
        self.assertEqual(success, True, "Tags not associated with image correctly")

        #clean up
        cursor.execute("Delete FROM PhotoTags WHERE photoID='{}'".format(dummy_photoID))
        cursor.execute("Delete FROM Photos WHERE photoID='{}'".format(dummy_photoID))
        cursor.execute("Delete FROM Tags WHERE tagName='tag1'")
        cursor.execute("Delete FROM Tags WHERE tagName='tag2'")
        cursor.execute("Delete FROM Tags WHERE tagName='tag3'")

        #delete the test user's account
        cursor.execute("DELETE FROM Users WHERE username='{}'".format(test_username))
        db_connection.commit()

        cursor.close()



if __name__ == '__main__':
    unittest.main()
