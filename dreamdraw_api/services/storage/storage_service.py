
import os
import json
from io import BytesIO
from PIL.Image import Image
from typing import List
from dreamdraw_api import config


def save_image(images: List[Image], task_id: str, info: dict):
    save_dir = os.path.join(config.IMAGE_SAVE_DIR, task_id)
    os.makedirs(save_dir)

    image_urls = []

    with open(os.path.join(save_dir, "info.json"), "w") as f:
        json.dump(info, f)

    for i, image in enumerate(images):
        filename = f"{str(i).zfill(2)}.webp"
        save_path = os.path.join(save_dir, filename)
        image_url = os.path.join(task_id, filename)
        image.save(save_path)
        image_urls.append(image_url)
        
    return image_urls
    