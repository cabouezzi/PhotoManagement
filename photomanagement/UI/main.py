from ..photomanagement import *
import pathlib


DB_PATH = pathlib.Path("./photo-database")

def main():
    db = Database(path=DB_PATH)
    speach_engine = speech()




if __name__ == "main":
    main()