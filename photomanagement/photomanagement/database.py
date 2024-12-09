import pathlib
import os
import time
import uuid
import numpy as np
import logging
from dataclasses import dataclass
from PIL import Image


import chromadb
from chromadb.utils.data_loaders import ImageLoader
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from chromadb.utils.embedding_functions.open_clip_embedding_function import (
    OpenCLIPEmbeddingFunction,
)

import glob
import logging
import shutil
@dataclass
class Photo:
    title: str = None
    description: str = None
    time_created: str = None
    time_last_modified: str = None
    perceptual_hash: str = None
    source: pathlib.Path | str = None
    data: Image = None


class Database(chromadb.Collection):
    client: chromadb.PersistentClient
    image_directory_path: pathlib.Path
    """The working directory of Chroma DB."""

    # different collections
    # one for textual search, one for duplicate search
    collection = chromadb.Collection
    """Collection used for vector search."""

    def __init__(self, path: pathlib.Path | None) -> None:
        embedding_function = OpenCLIPEmbeddingFunction()
        image_loader = ImageLoader()

        if isinstance(path, str):
            self.db_path = pathlib.Path(path)
        self.db_path = path or pathlib.Path("./database")

        self.image_directory_path = self.db_path / "images"
        self.client = chromadb.PersistentClient(
            path=str(self.db_path), 
            settings=chromadb.Settings(anonymized_telemetry=False, allow_reset=True)
        )
        

        self.collection = self.client.create_collection(
            name="multimodal",
            embedding_function=embedding_function,
            get_or_create=True,
            data_loader=image_loader,
        )

        if not self.image_directory_path.exists():
            self.image_directory_path.mkdir()

    def add_images_from_directory(self, photo_dir: pathlib.Path) -> list[str]:
        '''
        Adds all images from a directory to the database.
        Also generates any required information. 

        Throws IOError if a filepath does not lead to an image.
        All images before the IOError will be inserted into the database
        Returns a list of all ids added
        '''

        from .util import walk

        img_ids = []
        for filepath in walk(photo_dir):
            img_ids.append(self.add_image_by_path(filepath))

        return img_ids

    def add_image_by_path(self, filepath: pathlib.Path) -> str:
        '''
        Add an image to the database.
        Also generates any required information. 

        Throws IOError if filepath does not lead to an image.
        Returns the id of the image
        '''
        try:
            image = Image.open(filepath)
        # file isn't an image
        except IOError as e:
            logging.exception(f"Exception when adding image by path: {filepath}")
            raise e

        # step 1: add to directory of images
        id = str(uuid.uuid4())
        controlled_path = self.image_directory_path / f"{id}.PNG"
        image.save(controlled_path, format="PNG")

        # step 2: add properties to chroma
        # file metadata
        # do we really need `last_modified``...?
        file_stat = os.stat(filepath)
        last_modified_time = time.ctime(file_stat.st_mtime)
        
        # photo metadata
        if exif := image._getexif():
            if "36867" in exif:
                time_created = exif["36867"]
            elif "36868" in exif:
                time_created = exif["36868"]
            else:
                time_created = time.ctime(file_stat.st_birthtime)
        else:
            time_created = time.ctime(file_stat.st_birthtime)

        # TODO: LLM stuff takes way too long, consider moving to background thread or just ditch description entirely
        description = "None"

        self.collection.add(
            ids=id,
            images=np.array(image.convert("RGB")),
            metadatas={
                "title": filepath.name[:-4],
                "time_created": time_created,
                "time_last_modified": last_modified_time,
                "perceptual_hash": "None",  # TODO: Use hashing
                "description": description,
                "source": str(filepath),
            },
        )
        return id

    def add_image(self, image: Photo) -> str:
        '''
        Add an image to the database. Using a Photo object.
        Does NOT auto generate missing data.

        Throws IOError if filepath does not lead to an image.
        Returns the id of the image
        '''
        img_id = str(uuid.uuid4())
        controlled_path = self.image_directory_path / f"{img_id}.PNG"
        image.data.save(controlled_path, format="PNG")

        self.collection.add(
            ids=img_id,
            images=np.array(image.data.convert("RGB")),
            metadatas={
                "title": image.title,
                "time_created": image.time_created,
                "time_last_modified": image.time_last_modified,
                "perceptual_hash": image.perceptual_hash,
                "description": image.description,
                "source": str(image.source),
            },
        )
        return img_id

    def query_with_text(self, prompt: str, limit: int = 6) -> list[(str, Photo)]:
        '''
        Query the database fot *images* with the above text and return *limit* photos.
        '''
        results = self.collection.query(
            query_texts=prompt, include=["metadatas", "data"], n_results=limit
        )

        # convert to `Photo` class
        N = len(results["ids"][0])
        photos = [None] * N
        for i in range(N):
            metadata = results["metadatas"][0][i]
            img_id = results["ids"][0][i]
            
            image_path = pathlib.Path(self.image_directory_path) / f"{img_id}.PNG"
            with Image.open(image_path) as image_data:
                # photos[i] = Photo(id=id, **metadata, data=image_data)
                photos[i] = (img_id, Photo( **metadata, data=image_data))
            

        return photos

    def delete_images(self, ids: str | list[str]) -> bool:
        if isinstance(ids, str):
            ids = [ids]

        if len(ids) == 0:
            return False
        
        # remove from images directory
        for id in ids:
            image_path = pathlib.Path(self.image_directory_path) / f"{id}.PNG"

            if image_path.exists():
                image_path.unlink()
                logging.info(f"Deleted image with id {id}.")
            else:
                logging.info(f"Image for {id} not found.")

        # remove entries from chroma
        self.collection.delete(ids=ids)
        return True

        
        

        # if is_reset:
        #     shutil.rmtree(self.db_path / "images")
        #     while pathlib.Path(self.db_path / "images").exists():
        #         pass

        #     os.mkdir(self.db_path / "images")
        #     while not pathlib.Path(self.db_path / "images").exists():
        #         pass
        # else:
        #     raise IOError("Cannot Reset the database!")
        
        # self.__init__(self.db_path)

        # self.client = chromadb.PersistentClient(
        #     path=str(self.db_path), settings=chromadb.Settings(anonymized_telemetry=False, allow_reset=True)
        # )

