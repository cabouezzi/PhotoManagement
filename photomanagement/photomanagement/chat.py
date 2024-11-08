import ollama
import pathlib


def convert_image_to_bytes(path: pathlib.Path) -> bytes:
    with open(path, "rb") as image:
        f = image.read()
    return f


class Chat:
    model: str = "llama3.2-vision:11b"
    """The name of the model on Ollama. Default is `llama3.2-vision:11b`."""

    messages: list[ollama.Message]
    """An ordered list of messages for the conversation"""

    def __init__(self, messages: list[ollama.Message] = []) -> None:
        self.messages = messages

    def invoke(self, prompt: str, images: list[bytes] = []) -> ollama.Message:
        """Prompts the model with a chat message."""

        invocation = ollama.Message(role="user", content=prompt, images=images)
        self.messages.append(invocation)

        response = ollama.chat(model=self.model, messages=self.messages)

        reply = ollama.Message(response["message"])
        self.messages.append(reply)
        return reply
