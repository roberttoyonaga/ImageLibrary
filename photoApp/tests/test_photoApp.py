import unittest
from utils import * 
from authentication import *

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
    def test_get_ownerID(self):
        HOST = "localhost"
        DATABASE = "photoDB"
        USER = "user"
        PASSWORD = "photoPassword"
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        cursor = db_connection.cursor()

        ownerID = get_ownerID(cursor, "default_user")
        self.assertEqual(ownerID, 1, "Getting photo ownerID failed")

if __name__ == '__main__':
    unittest.main()
