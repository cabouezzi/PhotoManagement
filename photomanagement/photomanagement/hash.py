from PIL import Image
from datetime import datetime
import numpy as np


def hash_to_str(hash: list[float]) -> str:
    """
    Returns a string representation for a perceptual hash embedding.

    *Note*: Adapted from https://github.com/JohannesBuchner/imagehash

    :param hash: the perceptual hash embedding.
    """
    bit_string = "".join(str(b) for b in 1 * hash)
    width = int(np.ceil(len(bit_string) / 4))
    return "{:0>{width}x}".format(int(bit_string, 2), width=width)


def perceptual_hash(image: Image.Image, hash_size=8, highfreq_factor=4) -> list[float]:
    """
    Returns a string representation for a perceptual hash embedding.

    *Note*: Adapted from https://github.com/JohannesBuchner/imagehash

    :param image: the image to hash.
    :param hash_size: the size to reduce to for hashing.
    :param highfreq_factor: the factor to apply while resizing.
    """
    if hash_size < 2:
        raise ValueError("Hash size must be greater than or equal to 2")

    import scipy.fftpack

    img_size = hash_size * highfreq_factor
    image = image.convert("L").resize((img_size, img_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = np.where(dctlowfreq > med, 1, 0)
    return diff.reshape((-1))
