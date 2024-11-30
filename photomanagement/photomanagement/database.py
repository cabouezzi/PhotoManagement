import chromadb
from chromadb.utils import embedding_functions
from dataclasses import dataclass

DB_PATH = r"./database"
# Change this line to change the sentence transformer
# List of transformers: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
# sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
SENTENENCE_TRANSFORMER_EF = embedding_functions.DefaultEmbeddingFunction()


@dataclass
class Photo:
    title: str
    description: str
    time_created: str
    time_last_modified: str
    perceptual_hash: str


class Database(chromadb.Collection):
    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.collection = self.client.create_collection(
            name="photo_management",
            embedding_function=SENTENENCE_TRANSFORMER_EF,
            get_or_create=True,
        )

    def addImages(self, images: list[Photo]):
        id_list = []
        descriptions = []
        metadata_list = []

        for idx, img in enumerate(images):
            id_list.append(str(idx))
            descriptions.append(img.description)
            metadata_list.append(
                {
                    "title": img.title,
                    "time_created": img.time_created,
                    "time_last_modified": img.time_last_modified,
                    "perceptual_hash": img.perceptual_hash,
                }
            )

        self.collection.add(
            ids=id_list, documents=descriptions, metadatas=metadata_list
        )
