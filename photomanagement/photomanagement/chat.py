import ollama
import pathlib
from typing import Generator


def convert_image_to_bytes(path: pathlib.Path) -> bytes:
    with open(path, "rb") as image:
        f = image.read()
    return f


class Chat:
    """A class to make it easier to keep track of message history when chatting with LLM's using Ollama."""

    model: str = "llama3.2-vision:11b"
    """The name of the model on Ollama. Default is `llama3.2-vision:11b`."""

    messages: list[ollama.Message]
    """An ordered list of messages for the conversation"""

    def __init__(self, messages: list[ollama.Message] = []) -> None:
        self.messages = messages

    def invoke(self, prompt: str, images: list[bytes] = []) -> ollama.Message:
        """
        Prompts the model with a chat message.

        :param prompt: the next message to invoke to the LLM.
        :param images: a list of images (raw bytes) to pass along with the message.
        """

        invocation = ollama.Message(role="user", content=prompt, images=images)
        self.messages.append(invocation)

        response = ollama.chat(model=self.model, messages=self.messages)

        reply = ollama.Message(response["message"])
        self.messages.append(reply)
        return reply

    def invoke_stream(
        self, prompt: str, images: list[bytes] = []
    ) -> Generator[str, None, ollama.Message]:
        """
        Prompts the model with a chat message and returns a stream of tokens.

        :param prompt: the next message to invoke to the LLM.
        :param images: a list of images (raw bytes) to pass along with the message.
        """
        invocation = ollama.Message(role="user", content=prompt, images=images)
        self.messages.append(invocation)
        stream = ollama.chat(model=self.model, messages=self.messages, stream=True)

        reply = ""
        for chunk in stream:
            yield chunk["message"]["content"]
            reply += " " + chunk["message"]["content"]

        reply = ollama.Message(role="assistant", content=reply)
        self.messages.append(reply)
        return reply
