import pyttsx3
from dataclasses import dataclass
from PIL import Image
import json
from .chat import Chat
from .database import Photo


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

        if text == "None":
            chat = Chat()
            response = chat.invoke(prompt="Describe this photo in one sentence.", images=[photo.data])["content"]
            photo.description = response
            text = photo.description

        if not isinstance(text, str):
            raise ValueError("photo description is empty or is not a string")
        
        self.engine.say(text)
        self.engine.runAndWait()