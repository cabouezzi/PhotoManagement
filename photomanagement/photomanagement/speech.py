import pyttsx3

class speech:
    def __init__(self):  
        self.engine = pyttsx3.init() #initialize the pyttsx3 engine
    
    def speak(self, text: str):
        """
        Uses pyttsx3 to say the provided text.
        :param text: The string to be read aloud.
        """
        if not isinstance(text, str):
            raise ValueError("input must be string")
        
        self.engine.say(text)
        self.engine.runAndWait()
        