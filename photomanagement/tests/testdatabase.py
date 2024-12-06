import unittest
from pprint import pprint
import PIL.IcnsImagePlugin
import PIL.Image
import PIL.ImageChops
from photomanagement import *
import pathlib
import PIL


class TestDatabase(unittest.TestCase):

    WORKING_PATH = pathlib.Path("./test-database")
    TEST_DATA_PATH = pathlib.Path(__file__).parent / "test-images"
    database: Database
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.database = Database(path=cls.WORKING_PATH)
        
    @classmethod
    def tearDownClass(cls) -> None:
        cls.database.client.reset()
        return super().tearDownClass()
    
    def test_database_pings(cls):
        cls.assertTrue(cls.database.client.heartbeat())
    
    def test_add_image(cls):
        test_image_path = cls.TEST_DATA_PATH / "image.jpg"
        cls.database.add_image(test_image_path)
        
        resp = cls.database.collection.get(where={"title": "image"})
        
        
        resp_source_path = pathlib.Path(resp["metadatas"][0]["source"])
        original_image = PIL.Image.open(test_image_path)
        new_image = PIL.Image.open(cls.WORKING_PATH / "images" / 
                                   f"{resp["ids"][0]}.png").convert("RGB")


        cls.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        cls.assertEqual(test_image_path, resp_source_path, 
                        msg="Source path is not original path!")
        cls.assertListEqual(list(original_image.getdata()), list(new_image.getdata()),
                        msg="Images are not the same!")
        
    def test_query_with_text(cls):
        pass
        
# class TestDatabaseFunctionality(unittest.TestCase):
#     WORKING_PATH = pathlib.Path("./test-database")
#     TEST_DATA_PATH = pathlib.Path(__file__).parent / "test-images"
#     database: Database

    
