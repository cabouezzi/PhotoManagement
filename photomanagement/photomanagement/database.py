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

from .hash import perceptual_hash, hash_to_str


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
    phash_collection = chromadb.Collection

    def __init__(self, path: pathlib.Path | None) -> None:
        embedding_function = OpenCLIPEmbeddingFunction()
        image_loader = ImageLoader()

        if isinstance(path, str):
            path = pathlib.Path(path)
        path = path or pathlib.Path("./database")

        self.image_directory_path = path / "images"
        self.client = chromadb.PersistentClient(
            path=str(path), settings=chromadb.Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.create_collection(
            name="multimodal",
            embedding_function=embedding_function,
            get_or_create=True,
            data_loader=image_loader,
        )
        self.phash_collection = self.client.create_collection(
            name="phash",
            get_or_create=True,
        )

        if not self.image_directory_path.exists():
            self.image_directory_path.mkdir()

    def add_images_from_directory(self, photo_dir: pathlib.Path):
        from .util import walk

        for filepath in walk(photo_dir):
            self.add_image(filepath)

    def add_image(self, filepath: pathlib.Path):
        try:
            image = Image.open(filepath)
        # file isn't an image
        except IOError:
            return

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

        raw_hash = perceptual_hash(image)
        hash = hash_to_str(raw_hash)

        self.collection.add(
            ids=id,
            images=np.array(image.convert("RGB")),
            metadatas={
                "title": "title",
                "time_created": time_created,
                "time_last_modified": last_modified_time,
                "perceptual_hash": hash,
                "description": description,
                "source": str(filepath),
            },
        )

        # step 3: bin by hash for duplicate search
        # retrieve bin
        results = self.phash_collection.get(hash)

        # unfortunately chroma does not support lists in metadata
        # add id to the bin
        source_ids = {id: True}

        if len(results["metadatas"]) > 0:
            # loop through existing ids and add retain source_ids
            if results["metadatas"][0]:
                for key in results["metadatas"][0].keys():
                    if not (key == "count"):
                        source_ids[key] = True
            else:
                logging.error(f"Entry corrupted for perceptual hash {hash}")

        # keep a count variable to filter for bins with length > 1
        source_ids.update({"count": len(source_ids.keys())})
        self.phash_collection.upsert(
            ids=hash,
            embeddings=raw_hash,
            metadatas=source_ids,
        )

    def query_with_text(self, prompt: str, limit: int = 6) -> list[Photo]:
        """Returns photos most relevant to the text prompt."""
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

    def query_with_photo(self, photo: Photo, limit: int = 6) -> list[Photo]:
        """Returns most similar photos, including duplicates."""
        results = self.collection.query(
            query_images=np.array(photo.data.convert("RGB")),
            include=["metadatas", "data"],
            n_results=limit,
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

    def scan_duplicates_for_photo(self, photo: Photo) -> list[Photo]:
        """Returns exact perceptual duplicates of the photo."""
        results = self.phash_collection.get(ids=photo.perceptual_hash)

        # get ids from metadata
        ids = results["metadatas"][0]
        ids.pop("count")
        ids = list(ids.keys())
        # get the entries for the ids
        entries = self.collection.get(ids)
        # map each entry to a photo object
        photos = [
            Photo(
                id=entries["ids"][j],
                **(entries["metadatas"][j]),
                data=Image.open(
                    pathlib.Path(self.image_directory_path) / f"{entries["ids"][j]}.png"
                ),
            )
            for j in range(len(entries["ids"]))
        ]

        return photos

    def scan_duplicates(self) -> list[list[Photo]]:
        """Returns bins of duplicate photos. Bins containing only one photo will not be included."""
        results = self.phash_collection.get(where={"count": {"$gt": 1}})
        N = len(results["ids"])
        bins = [None] * N

        for i in range(N):
            # get ids from metadata
            ids = results["metadatas"][i]
            ids.pop("count")
            ids = list(ids.keys())
            # get the entries for the ids
            entries = self.collection.get(ids)
            # map each entry to a photo object
            photos = [
                Photo(
                    id=entries["ids"][j],
                    **(entries["metadatas"][j]),
                    data=Image.open(
                        pathlib.Path(self.image_directory_path)
                        / f"{entries["ids"][j]}.png"
                    ),
                )
                for j in range(len(entries["ids"]))
            ]
            # store the photos in their bin
            bins[i] = photos

        return bins

    def delete_images(self, photos: Photo | list[Photo]):
        if isinstance(photos, Photo):
            photos = [photos]

        ids = [photo.id for photo in photos]

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

        # remove from duplicate collection
        hashes = [photo.perceptual_hash for photo in photos]
        entries = self.phash_collection.get(hashes, include=["embeddings", "metadatas"])
        bins = entries["metadatas"]

        for i in range(len(bins)):
            for id in ids:
                print(bins[i])
                print(id)
                if id in bins[i]:
                    del bins[i][id]
                    bins[i]["count"] -= 1

        # remove old data
        self.phash_collection.delete(ids=entries["ids"])
        # add old data
        self.phash_collection.upsert(
            entries["ids"], embeddings=entries["embeddings"], metadatas=bins
        )
