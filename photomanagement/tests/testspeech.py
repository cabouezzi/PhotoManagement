import unittest
import pathlib
from photomanagement import *
from PIL import Image

class TestSpeech(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-speech")
    TEST_DATA_PATH = pathlib.Path(__file__).parent.parent / "images" / "animal_images"
    database: Database
    speechEngine = Speech()

    @classmethod
    def setUpClass(cls):
        cls.database = Database(path=cls.WORKING_PATH)
        cls.database.add_images_from_directory(cls.TEST_DATA_PATH)

    @classmethod
    def tearDownClass(cls):
        import shutil

        cls.database = None
        shutil.rmtree(cls.WORKING_PATH)
    
    def test_print_desc(self):
        photo = self.database.query_with_text("cat")
        desc = self.speechEngine.speak(photo[0])
        self.database.update_photo(photo[0], desc)
        result = self.database.get(ids=photo[0].id)
        print(desc)
        print(result)
        self.assertNotEqual(result["metadatas"][0]["description"], "None")
