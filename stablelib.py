from requests import post
from io import BytesIO
from base64 import b64decode
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from typing import List
from random import sample
from random import choice
from os import listdir


from config import wordlistv2
from config import FOLDER_NEW

# start stable diffusion web with api
# linux: ./webui.sh --skip-torch-cuda-test --api --no-half


def generate(prompt: str, width: int = 512, height: int = 512, steps: int = 5, url: str = "http://127.0.0.1:7860"):
    json = {
        "prompt": prompt,
        "steps": steps,
        "width": width,
        "height": height
    }

    response = post(f"{url}/sdapi/v1/txt2img", json=json).json()
    return Image.open(BytesIO(b64decode(response["images"][0])))



def combine_images(prompt: str, images: List[Image.Image], target_size = (128, 128), vert_offset = 100, font_size = 16, bg_color = (58,145,57), text_color = (251,221,17), stroke_width=2) -> Image.Image:
    
    assert len(images) == 9
    
    images_iter = iter([image.resize(target_size) for image in images])
    number_iter = iter(range(1, 10))
    img_size = (3 * target_size[0], vert_offset + 3 * target_size[1])

    combined_image = Image.new("RGB", img_size, bg_color)
    draw = ImageDraw.Draw(combined_image)
    font = ImageFont.truetype("Ubuntu-R.ttf", 18)

    text_position = (vert_offset / 2 - font_size / 2, 10)

    split_text = "".join([char if (i + 1) % int(target_size[0] * 3 / 10) else char + "-\n" for i, char in enumerate(prompt)])
    draw.text(text_position, split_text, text_color, font)
    

    for x in range(0, target_size[0] * 3, target_size[0]):
        for y in range(vert_offset, vert_offset + target_size[1] * 3, target_size[1]):
            combined_image.paste(next(images_iter), (x, y))
            number_pos = (x + target_size[0] - 14, y + 2)
            draw.text(number_pos, str(next(number_iter)), (10, 10, 10), font, stroke_width=stroke_width, stroke_fill=bg_color)
    
    
    return combined_image


def generate_captcha(**kwargs):
    """
    render a 9-image captcha with instruction.\n
    `**kwargs` are passed onto `combine_images`.\n
    returns image as `PIL.Image.Image` and a list of solutions as `List[int]`
    """
    files = sample(listdir(FOLDER_NEW), 9)
    images = [Image.open(f"{FOLDER_NEW}/{file}") for file in files]
    topic = choice(files).split("-")[0]

    solutions = [i for i, name in enumerate(files) if name.split("-")[0] == topic]

    instruction = f'select all images with {wordlistv2[topic]}s'
    return combine_images(instruction, images, **kwargs), solutions
    
    
    


if __name__ == "__main__":
    # create demo captchas
    for _ in range(10):
        captcha, solution = generate_captcha()
        captcha.save(f"captchas/{'+'.join([str(s) for s in solution])}.png")