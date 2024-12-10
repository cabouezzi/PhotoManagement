from PIL import Image
from datetime import datetime
from photomanagement.hash import perceptual_hash, hash_to_str
from photomanagement import Photo, Database
import unittest
import pathlib


class TestHash(unittest.TestCase):
    WORKING_PATH = pathlib.Path("./test-dbs/test-hash")
    TEST_DATA_PATH = (
        pathlib.Path(__file__).parent.parent / "images" / "duplicate-images"
    )
    database: Database

    @classmethod
    def setUpClass(cls):
        cls.database = Database(path=cls.WORKING_PATH)
        cls.database.add_images_from_directory(cls.TEST_DATA_PATH)

    @classmethod
    def tearDownClass(cls):

        # https://stackoverflow.com/questions/76518144/trouble-deleting-chromadb-documents
        from chromadb.api.client import SharedSystemClient
        cls.database.client._system.stop()
        SharedSystemClient._identifier_to_system.pop(cls.database.client._identifier, None)

        import shutil
        cls.database = None
        shutil.rmtree(cls.WORKING_PATH)

    def test_hash_duplicate(self):
        original = Image.open(self.TEST_DATA_PATH / "flag.jpg")
        # flag_shrunk is an image that was shrunken down in size,
        # so the bytes are different but the image looks the same
        shrunk = Image.open(self.TEST_DATA_PATH / "flag_shrunk.jpg")

        original_hash = perceptual_hash(original)
        shrunken_hash = perceptual_hash(shrunk)

        self.assertEqual(original_hash.tolist(), shrunken_hash.tolist())
        self.assertEqual(hash_to_str(original_hash), hash_to_str(shrunken_hash))

    def test_hash_different(self):
        image1 = Image.open(self.TEST_DATA_PATH / "flag.jpg")
        image2 = Image.open(self.TEST_DATA_PATH / "blimp.jpg")
        hash1 = perceptual_hash(image1)
        hash2 = perceptual_hash(image2)

        self.assertNotEqual(hash1.tolist(), hash2.tolist())
        self.assertNotEqual(hash_to_str(hash1), hash_to_str(hash2))

    def test_scan_database(self):
        bins = self.database.scan_duplicates()
        # the only duplicate is the flags
        # the blimp and butterfly count is 1 and shouldn't be returned
        self.assertEqual(len(bins), 1)
        self.assertEqual(len(bins[0]), 2)

        sample = Image.open(self.TEST_DATA_PATH / "flag.jpg")
        hash = hash_to_str(perceptual_hash(sample))

        self.assertEqual(hash, bins[0][0].perceptual_hash)

    def test_scan_database_for_photo_multiple(self):
        sample = Image.open(self.TEST_DATA_PATH / "flag.jpg")
        hash = hash_to_str(perceptual_hash(sample))
        # only perceptual hash is used
        photo = Photo(
            id="id",
            title="title",
            description="desc",
            time_created="timec",
            time_last_modified="timem",
            perceptual_hash=hash,
            source="source",
            data=sample,
        )
        # scan, expect bin with two photos
        bins = self.database.scan_duplicates_for_photo(photo)
        self.assertEqual(len(bins), 2)
        self.assertEqual(hash, bins[0].perceptual_hash)

    def test_scan_database_for_photo_single(self):
        sample = Image.open(self.TEST_DATA_PATH / "blimp.jpg")
        hash = hash_to_str(perceptual_hash(sample))
        # only perceptual hash is used
        photo = Photo(
            id="id",
            title="title",
            description="desc",
            time_created="timec",
            time_last_modified="timem",
            perceptual_hash=hash,
            source="source",
            data=sample,
        )
        # expect bin even if bin count = 1
        bins = self.database.scan_duplicates_for_photo(photo)
        self.assertEqual(len(bins), 1)
        self.assertEqual(hash, bins[0].perceptual_hash)
