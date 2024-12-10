import unittest
from pprint import pprint
import PIL.Image
import PIL.ImageChops
from photomanagement import Database, hash
import pathlib
import shutil
import os
import logging

class TestDatabaseConfig(unittest.TestCase):

    WORKING_PATH = pathlib.Path("./test-dbs/test-database-Config")
    TEST_DATA_PATH = pathlib.Path(__file__).parent.parent / "images"
    database: Database
    ids_uploaded = []

    @classmethod
    def setUpClass(cls) -> None:
        if cls.WORKING_PATH.exists():
            shutil.rmtree(cls.WORKING_PATH)
        
        cls.database = Database(path=cls.WORKING_PATH)

    @classmethod
    def tearDownClass(self) -> None:
        try:
            self.database.delete_images(self.ids_uploaded)
        except ValueError as e:
            logging.warning(f"No entries in delete! {e}")

    def test_database_pings(self):
        self.assertTrue(self.database.client.heartbeat())

class TestDatabaseCRUD(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-dbs/test-database-CRUD")
    TEST_DATA_PATH = pathlib.Path(__file__).parent.parent / "images"
    database: Database
    photos_uploaded = []

    @classmethod
    def setUpClass(cls) -> None:
        if cls.WORKING_PATH.exists():
            shutil.rmtree(cls.WORKING_PATH)
        
        cls.database = Database(path=cls.WORKING_PATH)
    
    @classmethod
    def tearDownClass(self) -> None:
        try:
            self.database.delete_images(self.photos_uploaded)
        except ValueError as e:
            logging.warning(f"No entries in delete! {e}")
    
    def test_add_image0(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        img = self.database.add_image(test_image_path)
        self.photos_uploaded.append(img)

        resp = self.database.collection.get(ids=[img.id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
    def test_add_image1(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        img = self.database.add_image(test_image_path)
        self.photos_uploaded.append(img)

        resp = self.database.collection.get(ids=[img.id])
        
        resp_source_path = pathlib.Path(resp["metadatas"][0]["source"])

        self.assertEqual(len(resp["ids"]), 1,
                        msg="More or less than 1 image was found!")
        self.assertEqual(test_image_path, resp_source_path, 
                        msg="Source path is not original path!")
    def test_add_image2(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        photo = PIL.Image.open(test_image_path)
        img = self.database.add_image(test_image_path)
        self.photos_uploaded.append(img)
        img_hash = hash.hash_to_str(hash.perceptual_hash(photo))
        photo.close()

        resp = self.database.collection.get(ids=[img.id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertEqual(img_hash, resp["metadatas"][0]["perceptual_hash"],
                        msg="Images are not the same!")   
    def test_add_image3(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        img = self.database.add_image(test_image_path)
        self.photos_uploaded.append(img)

        resp = self.database.collection.get(ids=[img.id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertEqual(img.id, resp["ids"][0], 
                        msg="Images ids are not the same!")
        
    def test_add_images_from_directory0(self):
        test_image_path = self.TEST_DATA_PATH / f"animal_images"

        img_ids = self.database.add_images_from_directory(test_image_path)
        original_img_paths = os.listdir(test_image_path)

        self.assertEqual(len(img_ids), len(original_img_paths),
                         msg=f"The number of ids returned {img_ids}, != the number of images expected {original_img_paths}!") 
    def test_add_images_from_directory1(self):
        test_image_path = self.TEST_DATA_PATH / "animal_images"

        imgs = self.database.add_images_from_directory(test_image_path)
        original_img_paths = os.listdir(test_image_path)

        for idx, orig_img_path in enumerate(original_img_paths):
            with self.subTest(msg=f"subTest {idx} testing: {orig_img_path}"):
                resp = self.database.collection.get(ids=[imgs[idx].id])

                with PIL.Image.open(test_image_path / orig_img_path) as original_image:
                    img_hash = hash.hash_to_str(hash.perceptual_hash(original_image))
                
                self.assertEqual(len(resp["ids"]), 1, 
                                msg="More or less than 1 image was found!")
                self.assertEqual(img_hash, resp["metadatas"][0]["perceptual_hash"],
                                msg="Images are not the same!")   

class TestDatabaseQUERY(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-dbs/test-database-QUERY")
    TEST_DATA_PATH = pathlib.Path(__file__).parent.parent / "images"
    database: Database
    photos_uploaded = []

    @classmethod
    def setUpClass(cls) -> None:
        if cls.WORKING_PATH.exists():
            shutil.rmtree(cls.WORKING_PATH)

        cls.database = Database(path=cls.WORKING_PATH)
    
    @classmethod
    def tearDownClass(self) -> None:
        try:
            self.database.delete_images(self.photos_uploaded)
        except ValueError as e:
            logging.warning(f"No entries in delete! {e}")
        
    def test_query_with_text0(self):
        test_image_path = self.TEST_DATA_PATH / "eyes" / "eyesclosed.jpg"

        with PIL.Image.open(test_image_path) as image:
            img = self.database.add_image(test_image_path)
            self.photos_uploaded.append(img)

        resp = self.database.query_with_text("Someone with closed eyes", 1)
        self.assertEqual(len(resp), 1, 
                        msg="More than 1 image was returned!")
    def test_query_with_text1(self):
        test_image_path = self.TEST_DATA_PATH / "eyes" / "eyesclosed.jpg"
        
        with PIL.Image.open(test_image_path) as image:
            img = self.database.add_image(test_image_path)
            self.photos_uploaded.append(img)
            img_hash = hash.hash_to_str(hash.perceptual_hash(image))

        resp = self.database.query_with_text("Someone with closed eyes", 1)
        self.assertEqual(img_hash, resp[0].perceptual_hash,
                        msg="Image returned is not the same!")
        

    
