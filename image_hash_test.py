from PIL import Image
from imagehash import dhash
from db import Photo, database
from datetime import datetime
from image_hash import hash_image, is_duplicate


image1 = Image.open('testData/testImages/image1.jpg')
image2 = Image.open('testData/testImages/image2.jpg')

# Convert the image to a Photo object
photo1 = hash_image(image1, title="image1.jpg", description="This is image1.jpg")
photo1_duplicate = hash_image(image1, title="image1.jpg", description="This is image1.jpg duplicate")
photo2 = hash_image(image2, title="image2.jpg", description="This is image2.jpg")

# Initialize the database
db = database()

# Clear the database before testing
try:
    all_ids = db.collection.get()['ids']
    db.collection.delete(ids=all_ids)
except:
    pass

assert not is_duplicate(photo1, db), "Image1 should not be detected as a duplicate"
db.addImages([photo1])
assert is_duplicate(photo1_duplicate, db), "Image1 duplicate should be detected as a duplicate"
assert not is_duplicate(photo2, db), "Image2 should not be detected as a duplicate"
db.addImages([photo2])

# Clean up the database after testing
try:
    all_ids = db.collection.get()['ids']
    db.collection.delete(ids=all_ids)
except:
    pass

print("Test passed!")
