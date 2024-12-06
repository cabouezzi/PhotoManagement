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


@dataclass
class Photo:
    id: str
    title: str
    description: str
    time_created: str
    time_last_modified: str
    perceptual_hash: str
    source: str
    data: Image


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
            path = pathlib.Path(path)
        path = path or pathlib.Path("./database")

        self.image_directory_path = path / "images"
        self.client = chromadb.PersistentClient(
            path=str(path), settings=chromadb.Settings(anonymized_telemetry=False, allow_reset=True)
        )

        self.collection = self.client.create_collection(
            name="multimodal",
            embedding_function=embedding_function,
            get_or_create=True,
            data_loader=image_loader,
        )

        if not self.image_directory_path.exists():
            self.image_directory_path.mkdir()

    def add_images_from_directory(self, photo_dir: pathlib.Path) -> None:
        from .util import walk

        for filepath in walk(photo_dir):
            self.add_image(filepath)

    def add_image(self, filepath: pathlib.Path) -> None:
        try:
            image = Image.open(filepath)
        # file isn't an image
        except IOError as e:
            raise e

        # step 1: add to directory of images
        id = str(uuid.uuid4())
        controlled_path = self.image_directory_path / f"{id}.png"
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
                time_created = time.ctime(file_stat.st_ctime)
        else:
            time_created = time.ctime(file_stat.st_ctime)

        # TODO: LLM stuff takes way too long, consider moving to background thread or just ditch description entirely
        description = "None"

        self.collection.add(
            ids=id,
            images=np.array(image.convert("RGB")),
            metadatas={
                "title": filepath.name[:-4],
                "time_created": time_created,
                "time_last_modified": last_modified_time,
                "perceptual_hash": "0",  # TODO: Use hashing
                "description": description,
                "source": str(filepath),
            },
        )

    def query_with_text(self, prompt: str, limit: int = 6) -> list[Photo]:
        results = self.collection.query(
            query_texts=prompt, include=["metadatas", "data"], n_results=limit
        )

        # convert to `Photo` class
        N = len(results["ids"][0])
        photos = [None] * N
        for i in range(N):
            metadata = results["metadatas"][0][i]
            id = results["ids"][0][i]
            image_path = pathlib.Path(self.image_directory_path) / f"{id}.png"
            image_data = Image.open(image_path)
            photos[i] = Photo(id=id, **metadata, data=image_data)

        return photos

    def delete_images(self, ids: str | list[str]) -> None:
        if isinstance(ids, str):
            ids = [ids]

        # remove from images directory
        for id in ids:
            image_path = pathlib.Path(self.image_directory_path) / f"{id}.png"

            if image_path.exists():
                image_path.unlink()
                logging.info(f"Deleted image with id {id}.")
            else:
                logging.info(f"Image for {id} not found.")

        # remove entries from chroma
        self.collection.delete(ids=ids)
