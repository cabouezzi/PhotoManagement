import ollama
import pathlib


def convert_image_to_bytes(path: pathlib.Path) -> bytes:
    with open(path, "rb") as image:
        f = image.read()
    return f


class Chat:
    messages: list[ollama.Message]

    def __init__(self, messages: list[ollama.Message] = []) -> None:
        self.messages = messages

    def invoke(self, prompt: str, images: list[bytes] = []) -> ollama.Message:
        invocation = ollama.Message(role="user", content=prompt, images=images)
        self.messages.append(invocation)

        response = ollama.chat(model="llava-llama3", messages=self.messages)

        reply = ollama.Message(response["message"])
        self.messages.append(reply)
        return reply
