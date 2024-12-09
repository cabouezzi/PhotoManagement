import unittest
import pathlib
import photomanagement.chat


class TestChat(unittest.TestCase):

    def test_image_description(self):
        from .util import semscore

        path = (
            pathlib.Path(__file__).parent.parent / "images" / pathlib.Path("image.jpg")
        )
        data = photomanagement.chat.convert_image_to_bytes(path)

        # repetition, judge based off the median
        n = 5
        scores = []
        for _ in range(n):
            chat = photomanagement.chat.Chat()
            # uncomment/change model if your pc can't handle llama3.2
            chat.model = "llava-llama3"
            description = chat.invoke(prompt="Describe this photo", images=[data])[
                "content"
            ]
            ideal = "The image is a painting of a woman holding her baby, as well as a young girl standing next to her. There is a man dressed in a sombrero holding a bouquet of balloons. The image is surrounded by a gold frame."
            scores.append((semscore(description, ideal), description))

        sorted_data = sorted(scores, key=lambda x: x[0])
        median_index = n // 2
        score, description = sorted_data[median_index]

        self.assertTrue(score > 0.6, f"Score: {score}\n\n{description}")

    def test_history(self):
        chat = photomanagement.chat.Chat()
        # uncomment/change model if your pc can't handle llama3.2
        chat.model = "llava-llama3"
        chat.invoke("My name is Jamaica")
        response = chat.invoke("What is my name?")
        self.assertTrue("Jamaica" in response["content"])
