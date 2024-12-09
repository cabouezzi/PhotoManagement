import pyttsx3
from dataclasses import dataclass
from PIL import Image
from .chat import Chat
from .database import Photo

class Speech:
    def __init__(self):  
        self.engine = pyttsx3.init() #initialize the pyttsx3 engine
        self.engine.setProperty("rate", 150)
        self.chat = Chat() # initialize a Chat() class that invokes ollama
    
    # input: photo object, returns a string of the image description
    def speak(self, photo: Photo):
        """
        Uses pyttsx3 to say the provided text.
        :param text: The string to be read aloud.
        """
        if not isinstance(photo, Photo): # check for correct photo type
            raise ValueError("input must be a Photo")
        
        text = photo.description

        if text == "None": # check if a description has already been generated and stored into database
            response = self.chat.invoke(prompt="Describe this photo in one sentence.", images=[photo.data.filename])["content"]
            text = response

        if not isinstance(text, str):
            raise ValueError("photo description is empty or is not a string")
        
        self.engine.say(text)
        self.engine.runAndWait()

        return text