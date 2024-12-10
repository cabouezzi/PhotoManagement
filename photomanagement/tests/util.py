from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-mpnet-base-v2")


def semscore(r1: str, r2: str) -> float:
    (v1, v2) = model.encode([r1, r2])
    cosine = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return cosine
