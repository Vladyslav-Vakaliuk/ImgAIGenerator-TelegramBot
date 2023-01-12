import requests
from os import path
import os
import openai

from environs import Env

from PIL import Image

def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    openai.api_key = env.str("OPENAI_API_KEY")

load_config()

image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)


async def generate_image(prompt):
    """ Create an image """
    
    # set the prompt
    prompt = prompt
    
    # call the OpenAI API
    generation_response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )

    # print response
    # print(generation_response)

    # save the image  
    i = 0
    flnm = "images\\image" + str(i) + ".png"

    while path.exists(flnm) :
        flnm = "images\\image" + str(i) + ".png"
        i += 1

    generated_image_filepath = os.path.join(flnm)
    generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
    generated_image = requests.get(generated_image_url).content  # download the image
    with open(generated_image_filepath, "wb") as image_file:
        image_file.write(generated_image)  # write the image to the file

    return generated_image_filepath


