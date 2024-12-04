import unittest
from pprint import pprint
from photomanagement import *


class TestDatabase(unittest.TestCase):

    def test_add_images(self):
        img = [Photo("boxer.png", "A picture of a boxer dog!", "0", "0", "0")]
        db = Database()
        db.addImages(img)
        pprint(db.collection.get())
