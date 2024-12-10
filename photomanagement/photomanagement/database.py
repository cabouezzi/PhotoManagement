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
    """The id of the photo within the system"""
    title: str
    """The title of the photo"""
    description: str
    """A textual description of the photo. This is stored after calling `Speech().speak(•)`, otherwise the value is "None"."""
    time_created: str
    """Time that the photo was taken"""
    time_last_modified: str
    """Time that the photo was last modified"""
    perceptual_hash: str
    """The perceptual hash string of the photo"""
    source: str
    """The name of the original photo"""
    data: Image.Image
    """A representation of the photo as a `PIL.Image.Image`"""


class Database(chromadb.Collection):
    client: chromadb.PersistentClient
    """The Chroma client object"""

    image_directory_path: pathlib.Path
    """The working directory of Chroma."""

    # different collections
    # one for textual search, one for duplicate search
    collection = chromadb.Collection
    """Collection used for vector search."""
    phash_collection = chromadb.Collection
    """Collection used for binning the ids of duplicate photos"""

    def __init__(self, path: pathlib.Path | None) -> None:
        """
        :param path: the directory for the `Database` to work within.
        """
        embedding_function = OpenCLIPEmbeddingFunction()
        image_loader = ImageLoader()

        if isinstance(path, str):
            path = pathlib.Path(path)
        path = path or pathlib.Path("./database")

        self.image_directory_path = path / "images"
        self.client = chromadb.PersistentClient(
            path=str(path), settings=chromadb.Settings(anonymized_telemetry=False, )
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
        """
        Adds all images from a directory to the database.
        Also generates any required information. 

        Returns a list of the photos.

        :param photo_dir: the directory of the images to add.
        """
        from .util import walk

        for filepath in walk(photo_dir):
            photos.append(self.add_image(filepath))

        return photos


    def add_image(self, filepath: pathlib.Path) -> Photo:
        '''
        Add an image to the database.
        Also generates any required information. 

        Returns the a Photo object
        '''

    def add_image(self, filepath: pathlib.Path):
        """
        Adds the image at the filepath into the system

        :param filepath: the path of the image to add.
        """
        try:
            image = Image.open(filepath)
        # file isn't an image
        except IOError as e:
            logging.exception(f"Exception when adding image @ {filepath}: {e}")

        # step 1: add to directory of images
        id = str(uuid.uuid4())
        controlled_path = self.image_directory_path / f"{id}.png"
        image.save(controlled_path, format="PNG", exif=image.info.get("exif"))

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

        raw_hash = perceptual_hash(image)
        hash = hash_to_str(raw_hash)

        photo = Photo(
            id=id,
            title=filepath.name[:-4],
            time_created=time_created,
            time_last_modified=last_modified_time,
            perceptual_hash=hash,
            description=description,
            source=str(filepath),
            data=np.array(image.convert("RGB"))
        )
        self.collection.add(
            ids=id,
            images=np.array(image.convert("RGB")),
            metadatas={
                "title": filepath.name[:-4],
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

        image.close()
        return photo

    def query_with_text(self, prompt: str, limit: int = 6) -> list[Photo]:
        """
        Returns photos most relevant to the text prompt.

        :param prompt: the textual query.
        :param limit: an integer limit for how many `Photo`s to return.
        """
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
        """
        Returns most similar photos, including duplicates.

        :param photo: the `Photo` to serve as the query.
        :param limit: an integer limit for how many `Photo`s to return.
        """
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
        """
        Returns exact perceptual duplicates of the photo.

        :param photo: the `Photo` to serve as the query.
        """
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
                    pathlib.Path(self.image_directory_path) / f"{entries['ids'][j]}.png"
                ),
            )
            for j in range(len(entries["ids"]))
        ]

        return photos

    def scan_duplicates(self) -> list[list[Photo]]:
        """
        Returns bins of duplicate photos.
        *Note*: Bins containing only one photo will not be included.
        """
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
                        / f"{entries['ids'][j]}.png"
                    ),
                )
                for j in range(len(entries["ids"]))
            ]
            # store the photos in their bin
            bins[i] = photos

        return bins

    def delete_images(self, photos: Photo | list[Photo]) -> None:
        """
        Deletes photos from the system.

        :param photo: can either be a single or list of `Photo`s. Data will be deleted from the system using the `Photo.id` field.
        """
        if isinstance(photos, Photo):
            photos = [photos]

        if len(photos) == 0:
            raise ValueError
        
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
        hashes = list(set([photo.perceptual_hash for photo in photos]))
        entries = self.phash_collection.get(hashes, include=["embeddings", "metadatas"])
        bins = entries["metadatas"]

        for i in range(len(bins)):
            for id in ids:
                if id in bins[i]:
                    del bins[i][id]
                    bins[i]["count"] -= 1

        # remove old data
        self.phash_collection.delete(ids=entries["ids"])
        # add old data
        self.phash_collection.upsert(
            entries["ids"], embeddings=entries["embeddings"], metadatas=bins
        )

    def get_all_images(self, sorted: bool = False) -> list[Photo]:
        """
        Returns a list of photos, sorted by the time they were created.

        :param sorted: whether or not to sort the photos by time before returning.
        """
        results = self.collection.get()
        # convert to `Photo` class
        N = len(results["ids"])
        photos = [None] * N
        for i in range(N):
            metadata = results["metadatas"][i]
            id = results["ids"][i]
            image_path = pathlib.Path(self.image_directory_path) / f"{id}.png"
            image_data = Image.open(image_path)
            photos[i] = Photo(id=id, **metadata, data=image_data)

        if sorted:
            photos.sort(key=lambda photo: photo.time_created)
        return photos
