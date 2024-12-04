import unittest
from pprint import pprint
from photomanagement import *
from PIL import Image
import pathlib


class TestTextualSearch(unittest.TestCase):

    WORKING_PATH = pathlib.Path("./test-textual-search")
    TEST_DATA_PATH = pathlib.Path(__file__).parent.parent / "images" / "animal_images"
    database: Database

    @classmethod
    def setUpClass(cls):
        cls.database = Database(path=cls.WORKING_PATH)
        cls.database.add_images_from_directory(cls.TEST_DATA_PATH)

    @classmethod
    def tearDownClass(cls):
        import shutil

        cls.database = None
        shutil.rmtree(cls.WORKING_PATH)

    def compare_image_sets(self, images1, images2):
        images1 = [tuple(image.getdata()) for image in images1]
        images2 = [tuple(image.getdata()) for image in images2]
        self.assertSetEqual(set(images1), set(images2))

    def test_chicken(self):
        photos = self.database.query_with_text("chicken")

        expected_chickens = [
            Image.open(self.TEST_DATA_PATH / "60.jpeg"),
            Image.open(self.TEST_DATA_PATH / "16.jpeg"),
        ]
        output_chickens = [photo.data for photo in photos[:2]]
        self.compare_image_sets(expected_chickens, output_chickens)

    def test_chicken_egg(self):
        photos = self.database.query_with_text("egg")

        # chicken in any order
        expected_chickens = [
            Image.open(self.TEST_DATA_PATH / "60.jpeg"),
            Image.open(self.TEST_DATA_PATH / "16.jpeg"),
        ]
        output_chickens = [photo.data for photo in photos[:2]]
        self.compare_image_sets(expected_chickens, output_chickens)
        self.assertEqual(
            list(output_chickens[0].getdata()), list(expected_chickens[0].getdata())
        )

    def test_cow(self):
        photos = self.database.query_with_text("cows")

        # chicken in any order
        expected_chickens = [
            Image.open(self.TEST_DATA_PATH / "OIP--aZkgJekoo6fjs3pfBRsBAHaE8.jpeg"),
            Image.open(self.TEST_DATA_PATH / "OIP-2RFVoPqR9gqjucro1rp7uwHaE8.jpeg"),
        ]
        output_chickens = [photo.data for photo in photos[:2]]
        self.compare_image_sets(expected_chickens, output_chickens)
        self.assertEqual(
            list(output_chickens[0].getdata()), list(expected_chickens[0].getdata())
        )
