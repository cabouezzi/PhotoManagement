import pyttsx3
from dataclasses import dataclass
from PIL import Image
from .chat import Chat
from .database import Photo


class Speech:
    def __init__(self):
        self.engine = pyttsx3.init()  # initialize the pyttsx3 engine
        self.engine.setProperty("rate", 150)

    def speak(self, photo: Photo):
        """
        Uses pyttsx3 to say the provided text.

        :param photo: the `Photo` to be read aloud.
        """
        if not isinstance(photo, Photo):
            raise ValueError("input must be a Photo")

        text = photo.description

        if text == "None":
            chat = Chat()
            response = chat.invoke(
                prompt="Describe this photo in one sentence.",
                images=[photo.data.filename],
            )["content"]
            photo.description = response
            text = photo.description

        if not isinstance(text, str):
            raise ValueError("photo description is empty or is not a string")

        self.engine.say(text)
        self.engine.runAndWait()

        return text

    def speak_stream(self, photo: Photo):
        """
        Uses pyttsx3 to say the provided text, which is generated as a stream.
        This begins speaking faster since it doesn't wait for the LLM response to complete.

        :param photo: the `Photo` to be read aloud.
        """
        if not isinstance(photo, Photo):
            raise ValueError("input must be a Photo")

        text = photo.description

        if text == "None":
            response = ""
            chat = Chat()

            chunk = []
            for word in chat.invoke_stream(
                prompt="Describe this photo in one sentence.",
                images=[photo.data.filename],
            ):
                chunk.append(word)
                if len(chunk) == 5:
                    self.engine.say(" ".join(chunk))
                    self.engine.runAndWait()
                    chunk = []
                response += " " + word
            photo.description = response
            text = photo.description

        if not isinstance(text, str):
            raise ValueError("photo description is empty or is not a string")

        return text
