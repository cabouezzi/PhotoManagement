"""
A Python package for managing and interacting with your photos.

```python
%%capture
# this captures output
%pip install photomanagement/
%pip install matplotlib
```


```python
import photomanagement
import pathlib
```


```python
db = photomanagement.Database(path="./database")
```

**Adding Photos**

The following line addes photos in the directory given. Running it more than once will add them more than once.


```python
db.add_images_from_directory(pathlib.Path("./photomanagement/images/animal_images"))
```

**Searching Photos**

The following cells show how to search photos using a textual query.


```python
import matplotlib.pyplot as plt

results = db.query_with_text("eggs")

plt.figure(figsize=(10, 6))

for i in range(len(results)):
    plt.subplot(2, 3, i + 1)
    plt.imshow(results[i].data)
    plt.axis("off")

plt.show()
```


    
![png](examples_files/examples_6_0.png)
    


**Deleting Photos**

After running the following cells, the chicken with the eggs will be gone!


```python
top_result = db.query_with_text("eggs")[0]

db.delete_images(top_result)
```


```python
import matplotlib.pyplot as plt

results = db.query_with_text("eggs")

plt.figure(figsize=(10, 6))

for i in range(len(results)):
    plt.subplot(2, 3, i + 1)
    plt.imshow(results[i].data)
    plt.axis("off")

plt.show()
```


    
![png](examples_files/examples_9_0.png)
    



```python
db.add_images_from_directory(pathlib.Path("./photomanagement/images/animal_images"))
```

**Search for Duplicates** \
The following cells have functionality for photos that are exact visually identical.


```python
duplicates = db.scan_duplicates_for_photo(results[0])

plt.figure(figsize=(10, 6))

for i in range(len(duplicates)):
    plt.subplot(2, 3, i + 1)  # the number of images in the grid is 5*5 (25)
    plt.imshow(duplicates[i].data)
    plt.axis("off")

plt.show()
```


    
![png](examples_files/examples_12_0.png)
    



```python
for bin in db.scan_duplicates():
    plt.figure(figsize=(10, 6))

    for i in range(len(bin)):
        plt.subplot(2, 3, i + 1)
        plt.imshow(bin[i].data)
        plt.axis("off")

    plt.show()
```


    
![png](examples_files/examples_13_0.png)
    



    
![png](examples_files/examples_13_1.png)
    



    
![png](examples_files/examples_13_2.png)
    



    
![png](examples_files/examples_13_3.png)
    



    
![png](examples_files/examples_13_4.png)
    



    
![png](examples_files/examples_13_5.png)
    



    
![png](examples_files/examples_13_6.png)
    



    
![png](examples_files/examples_13_7.png)
    



    
![png](examples_files/examples_13_8.png)
    



    
![png](examples_files/examples_13_9.png)
    



    
![png](examples_files/examples_13_10.png)
    



    
![png](examples_files/examples_13_11.png)
    



    
![png](examples_files/examples_13_12.png)
    



    
![png](examples_files/examples_13_13.png)
    



    
![png](examples_files/examples_13_14.png)
    



    
![png](examples_files/examples_13_15.png)
    



    
![png](examples_files/examples_13_16.png)
    


**Search for Similar Photos** \
The following cell is an example for searching similar – but not necessarily identical – photos.


```python
data = db.query_with_photo(results[0])
for i in range(len(data)):
    plt.subplot(3, len(data) // 3, i + 1)
    plt.imshow(data[i].data)
    plt.axis("off")

plt.show()
```


    
![png](examples_files/examples_15_0.png)
    


**Retrieve all images sorted by date**


```python
data = db.get_all_images(sorted=True)

for i in range((len(data) // 3) + 1):
    for j in range(i * 3, i * 3 + 3):
        if j < len(data):
            plt.subplot(1, 3, j - i * 3 + 1)
            plt.imshow(data[j].data)
            plt.axis("off")
    plt.show()
```


    
![png](examples_files/examples_17_0.png)
    



    
![png](examples_files/examples_17_1.png)
    



    
![png](examples_files/examples_17_2.png)
    



    
![png](examples_files/examples_17_3.png)
    



    
![png](examples_files/examples_17_4.png)
    



    
![png](examples_files/examples_17_5.png)
    



    
![png](examples_files/examples_17_6.png)
    



    
![png](examples_files/examples_17_7.png)
    



    
![png](examples_files/examples_17_8.png)
    



    
![png](examples_files/examples_17_9.png)
    



    
![png](examples_files/examples_17_10.png)
    



    
![png](examples_files/examples_17_11.png)
    


"""

from .database import Photo, Database
from .chat import Chat
from .speech import Speech
