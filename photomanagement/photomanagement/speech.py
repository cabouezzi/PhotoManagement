import pyttsx3
from dataclasses import dataclass
import json
from dataclasses import dataclass
from database import Photo


class Speech:
    def __init__(self):  
        self.engine = pyttsx3.init() #initialize the pyttsx3 engine
        self.engine.setProperty("rate", 150)
    
    def speak(self, photo: Photo):
        """
        Uses pyttsx3 to say the provided text.
        :param text: The string to be read aloud.
        """
        if not isinstance(photo, Photo):
            raise ValueError("input must be a Photo")
        
        text = photo.description

        if not isinstance(text, str):
            raise ValueError("photo description is empty or is not a string")
        
        self.engine.say(text)
        self.engine.runAndWait()

resp_get = Photo("title", "this is an image description", "12-3-2024", "12-3-2024", "hash")
print(resp_get.description)
engine = Speech()
engine.speak(resp_get)