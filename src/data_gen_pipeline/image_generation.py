import openai
import requests


class ImageGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_image(self, prompt, n=1, size="512x512"):
        response = openai.Image.create(prompt=prompt, n=n, max_width=size)

        return response

    def generate_save_image(self, prompt, path, n=1, size="512x512"):
        response = openai.Image.create(prompt=prompt, n=n, max_width=size)

        # retrieve image url from response and download
        image_url = response["data"][0]
        image = requests.get(image_url)
        with open(path, "wb") as f:
            f.write(image.content)
