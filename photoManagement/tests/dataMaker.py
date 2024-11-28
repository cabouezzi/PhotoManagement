import requests
import tarfile
import os

URL = r"https://data.caltech.edu/records/nyy15-4j048/files/256_ObjectCategories.tar?download=1"
PATH = r"./photoManagement/tests/test-images/"

CHUNK_SIZE = 4096 * 10

with requests.get(URL, stream=True) as response:
    if "content-disposition" in response.headers:
        file_name = response.headers["content-disposition"].split("filename=")[1]

    if "content-length" in response.headers:
        content_length = int(response.headers["content-length"])
    
    if "last-modified" in response.headers:
        last_modified = response.headers["last-modified"]

        # Check if file has been downloaded recently
        # throw exception if it has
        # delete the meta file to force redownload
        if os.path.exists(f"{PATH}{file_name}.meta"):
            with open(f"{PATH}{file_name}.meta", mode="r") as file:
                if(file.readline().split("\t")[1] == last_modified):
                    raise Exception("File is up to date!")

        with open(f"{PATH}{file_name}.meta", mode="w") as file:
            print("Saving last modified date...", end="")
            file.write(f"last-modified\t{last_modified}")
            print("...DONE!")

    with open(f"{PATH}{file_name}", mode="wb") as file:
        bytes_loaded = 0
        for chunk in response.iter_content(CHUNK_SIZE):
            bytes_loaded += len(chunk)
            print(f"Downloading {URL} -- {bytes_loaded} / {content_length} {round(bytes_loaded / content_length * 100, 2)}%", end="\r")
            file.write(chunk)
        print("\nDownload Complete!")


print("Extracting file...", end="")
with tarfile.open(f"{PATH}{file_name}") as file:
    file.extractall(path=f"{PATH}")

print("...Done!")


    


            


