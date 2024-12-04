from PIL import Image
from imagehash import dhash
from db import Photo, database
from datetime import datetime

def hash_image(image: Image, title: str = "", description: str = "") -> Photo:
    # Calculate the perceptual hash using dhash
    hash_value = str(dhash(image))
    # Get current time as ISO formatted string
    current_time = datetime.now().isoformat()
    # Create and return the Photo object
    return Photo(
        title=title,
        description=description,
        time_created=current_time,
        time_last_modified=current_time,
        perceptual_hash=hash_value
    )

def is_duplicate(photo: Photo, db: database) -> bool:
    # Query the database for a matching perceptual hash
    results = db.collection.get(where={"perceptual_hash": photo.perceptual_hash})
    # Check if any results were returned
    return bool(results['metadatas'])

# image1 = Image.open('testData/testImages/image1.jpg')
# photo1 = hash_image(image1, title="image1.jpg", description="This is image1.jpg")
# db = database()
# db.addImages([photo1])
# print(is_duplicate(photo1, db))  # Output: True