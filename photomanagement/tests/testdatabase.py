import unittest
from pprint import pprint
import PIL.Image
from photomanagement import *
import pathlib
import os

class TestDatabase(unittest.TestCase):

    WORKING_PATH = pathlib.Path("./test-database")
    TEST_DATA_PATH = pathlib.Path(__file__).parent / "test-images"
    database: Database
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.database = Database(path=cls.WORKING_PATH)
    
    def tearDown(self) -> None:
        self.database.client.reset()

    
    def test_database_pings(self):
        self.assertTrue(self.database.client.heartbeat())
    
    def test_add_image(self):
        test_image_path = self.TEST_DATA_PATH / "image.jpg"
        self.database.add_image(test_image_path)
        
        resp = self.database.collection.get(where={"title": "image"})
        
        
        resp_source_path = pathlib.Path(resp["metadatas"][0]["source"])
        original_image = PIL.Image.open(test_image_path)
        new_image = PIL.Image.open(self.WORKING_PATH / "images" / 
                                   f"{resp["ids"][0]}.png").convert("RGB")


        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertEqual(test_image_path, resp_source_path, 
                        msg="Source path is not original path!")
        self.assertListEqual(list(original_image.getdata()), list(new_image.getdata()),
                        msg="Images are not the same!")
        
    # def test_add_images_from_directory(self):
    #     num_of_images = len(os.listdir(self.TEST_DATA_PATH / "animal_images"))
    #     self.database.add_images_from_directory(self.TEST_DATA_PATH / "animal_images")
    #     print(num_of_images)
    #     raise NotImplementedError
    
