import unittest
from pprint import pprint
import PIL.Image
import PIL.ImageChops
from photomanagement import *
import pathlib
import shutil
import os
import time
import gc

class TestDatabaseConfig(unittest.TestCase):

    WORKING_PATH = pathlib.Path("./test-database-Config")
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
        self.database.delete_images(self.ids_uploaded)

    def test_database_pings(self):
        self.assertTrue(self.database.client.heartbeat())

class TestDatabaseCRUD(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-database-CRUD")
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
        self.database.delete_images(self.ids_uploaded)
        

    def test_add_image_by_path0(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"
        
        img_id = self.database.add_image_by_path(test_image_path)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
    def test_add_image_by_path1(self):
        
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"
        
        img_id = self.database.add_image_by_path(test_image_path)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])
        
        resp_source_path = pathlib.Path(resp["metadatas"][0]["source"])

        self.assertEqual(len(resp["ids"]), 1,
                        msg="More or less than 1 image was found!")
        self.assertEqual(test_image_path, resp_source_path, 
                        msg="Source path is not original path!")
    def test_add_image_by_path2(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"
        
        img_id = self.database.add_image_by_path(test_image_path)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        original_image = PIL.Image.open(test_image_path)
        new_image = PIL.Image.open(self.WORKING_PATH / "images" / 
                                   f"{resp["ids"][0]}.PNG").convert("RGB")
        
        diff_image = PIL.ImageChops.difference(original_image, new_image)
        is_different = diff_image.getbbox() and original_image.getexif() != new_image.getexif()

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertFalse(is_different,
                        msg="Images are not the same!")
    def test_add_image_by_path3(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"
        
        img_id = self.database.add_image_by_path(test_image_path)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertEqual(img_id, resp["ids"][0],
                        msg="Image ids are not the Same!")
    
    def test_add_image0(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        image = PIL.Image.open(test_image_path)
        title="Hispanic Painting"
        description="A painting with 3 people in it"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
    def test_add_image1(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        image = PIL.Image.open(test_image_path)
        title="Hispanic Painting"
        description="A painting with 3 people in it"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])
        
        resp_source_path = pathlib.Path(resp["metadatas"][0]["source"])

        self.assertEqual(len(resp["ids"]), 1,
                        msg="More or less than 1 image was found!")
        self.assertEqual(test_image_path, resp_source_path, 
                        msg="Source path is not original path!")
    def test_add_image2(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        image = PIL.Image.open(test_image_path)
        title="Hispanic Painting"
        description="A painting with 3 people in it"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        original_image = PIL.Image.open(test_image_path)
        new_image = PIL.Image.open(self.WORKING_PATH / "images" / 
                                   f"{resp["ids"][0]}.PNG").convert("RGB")
        
        diff_image = PIL.ImageChops.difference(original_image, new_image)
        is_different = diff_image.getbbox() and original_image.getexif() != new_image.getexif()

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertFalse(is_different,
                        msg="Images are not the same!")   
    def test_add_image3(self):
        test_image_path = self.TEST_DATA_PATH / f"image.jpg"

        image = PIL.Image.open(test_image_path)
        title="Hispanic Painting"
        description="A painting with 3 people in it"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.collection.get(ids=[img_id])

        self.assertEqual(len(resp["ids"]), 1, 
                        msg="More or less than 1 image was found!")
        self.assertEqual(img_id, resp["ids"][0], 
                        msg="Images ids are not the same!")
        
    def test_add_images_from_directory0(self):
        test_image_path = self.TEST_DATA_PATH / f"animal_images"

        img_ids = self.database.add_images_from_directory(test_image_path)
        original_img_paths = os.listdir(test_image_path)

        self.assertEqual(len(img_ids), len(original_img_paths),
                         msg=f"The number of ids returned {img_ids}, != the number of images expected {original_img_paths}!") 
    def test_add_images_from_directory1(self):
        test_image_path = self.TEST_DATA_PATH / "animal_images"

        img_ids = self.database.add_images_from_directory(test_image_path)
        original_img_paths = os.listdir(test_image_path)

        for idx, orig_img_path in enumerate(original_img_paths):
            with self.subTest(msg=f"subTest {idx} testing: {orig_img_path}"):
                resp = self.database.collection.get(ids=[img_ids[idx]])

                original_image = PIL.Image.open(test_image_path / orig_img_path)
                new_image = PIL.Image.open(self.WORKING_PATH / "images" / 
                                        f"{resp["ids"][0]}.PNG").convert("RGB")
                
                diff_image = PIL.ImageChops.difference(original_image, new_image)
                is_different = diff_image.getbbox() and original_image.getexif() != new_image.getexif()

                self.assertEqual(len(resp["ids"]), 1, 
                                msg="More or less than 1 image was found!")
                self.assertFalse(is_different,
                                msg="Images are not the same!")   

class TestDatabaseQUERY(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-database-QUERY")
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
        self.database.delete_images(self.ids_uploaded)
        
    def test_query_with_text0(self):
        test_image_path = self.TEST_DATA_PATH / "eyes" / "eyesclosed.jpg"

        image = PIL.Image.open(test_image_path)
        title="eyesclosed"
        description="A guy with his eyes closed"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.query_with_text("Someone with closed eyes", 1)
        self.assertEqual(len(resp), 1, 
                        msg="More than 1 image was returned!")
    def test_query_with_text1(self):
        test_image_path = self.TEST_DATA_PATH / "eyes" / "eyesclosed.jpg"

        image = PIL.Image.open(test_image_path)
        title="eyesclosed"
        description="A guy with his eyes closed"
        time_created=test_image_path.stat().st_birthtime
        time_last_modified=test_image_path.stat().st_mtime
        perceptual_hash=image_hash.hash_image(image)
        src = test_image_path
        
        photo = Photo(title, description, 
                      time_created, time_last_modified, 
                      perceptual_hash, src, image)
        
        img_id = self.database.add_image(photo)
        self.ids_uploaded.append(img_id)

        resp = self.database.query_with_text("Someone with closed eyes", 1)
        self.assertEqual(photo.perceptual_hash, resp[0][1].perceptual_hash,
                        msg="Image returned is not the same!")
        

    
