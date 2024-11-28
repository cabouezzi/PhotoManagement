from unittest import TestCase
from elasticsearch import Elasticsearch
from datetime import datetime

ELASTIC_USER="elastic"
ELASTIC_PASSWORD="elastic"
ELASTIC_PATH="https://localhost:9200"
ELASTIC_CERT=r"../ElasticSearchDatabase/ca.crt"

ELASTIC_TEST_INDEX = "test-index"

class Elasticsearch_Config_Tests(TestCase):
    def test_connection(self):
        client = Elasticsearch(
            ELASTIC_PATH,
            ca_certs=ELASTIC_CERT,
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        )
        resp = client.info()
        TestCase.assertIs(resp, object)

class Elasticsearch_CD_Tests(TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_ID = "test-id-1"
        cls.TEST_TIME = datetime.now()
        cls.entry = {
            "image-title": "Elasticsearch-Test-index.png",
            "created-timestamp": cls.TEST_TIME,
            "last-edited-timestamp": cls.TEST_TIME,
            "description": "This is to test indexing elasticsearch.",
            "perceptual-hash": ""
        }
        # cls.image_id = cls.entry["image-title"] + "-" + str(cls.entry["created-timestamp"])


        cls.client = Elasticsearch(
            ELASTIC_PATH,
            ca_certs=ELASTIC_CERT,
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
        )
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close() 
        return super().tearDownClass()
    

class Elasticsearch_Tests(TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_TIME = datetime.now()
        cls.entry = {
            "id": "test-id-1",
            "image-title": "Elasticsearch-Test-index.png",
            "created-timestamp": cls.TEST_TIME,
            "last-edited-timestamp": cls.TEST_TIME,
            "description": "This is to test indexing elasticsearch.",
            "perceptual-hash": ""
        }
        # cls.image_id = cls.entry["image-title"] + "-" + str(cls.entry["created-timestamp"])


        cls.client = Elasticsearch(
            ELASTIC_PATH,
            ca_certs=ELASTIC_CERT,
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
        )
        return super().setUpClass()
    
    def setUp(self) -> None:
        return super().setUp()
    

    def test_index_create(self):
        resp = self.client.index(index=ELASTIC_TEST_INDEX, document=self.entry, op_type="create")
        TestCase.assertEqual(self, "created", resp['result'], 
                             msg="Indexing document was unsuccessful")
        
    def test_get(self):
        resp = self.client.get(index=ELASTIC_TEST_INDEX, id=self.TEST_ID)
        TestCase.assertEqual(self, self.entry, resp['result'])