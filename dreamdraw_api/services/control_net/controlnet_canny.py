
import cv2
import torch
import numpy as np
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline
from PIL import Image

from dreamdraw_api.inference.utils import CONTROLNET_CANNY_MODEL_LIST, STABLE_MODEL_LIST
from dreamdraw_api.inference.utils import SCHEDULER_LIST, get_scheduler

class StableDiffusionControlNetCannyGenerator:
    def __init__(self) -> None:
        self.pipe = None

    def load_model(self, stable_model_path: str, controlnet_model_path: str, scheduler):
        if self.pipe is None:
            controlnet = ControlNetModel.from_pretrained(
                controlnet_model_path,
                torch_dtype=torch.float16
            )
            self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
                pretrained_model_name_or_path=stable_model_path,
                controlnet=controlnet,
                safety_checker=None,
                torch_dtype=torch.float16,
            )

        self.pipe = get_scheduler(pipe=self.pipe, scheduler=scheduler)
        self.pipe.to("cuda")
        self.pipe.enable_xformers_memory_efficient_attention()

        return self.pipe

    def controlnet_canny(self, image_path:str):
        image = Image.open(image_path)
        image = np.array(image)

        image = cv2.Canny(image, 100, 200)
        image = image[:, :, None]
        image = np.concatenate([image, image, image], axis=2)
        image = Image.fromarray(image)

        return image

    def generate_image(
        self,
        image_path: str,
        stable_model_path: str,
        controlnet_model_path: str,
        prompt: str,
        negative_prompt: str,
        num_images_per_prompt: int,
        guidance_scale: int,
        num_inference_step: int,
        scheduler: str,
        seed_generator: int
    ):
        pipe = self.load_model(
            stable_model_path=stable_model_path,
            controlnet_model_path=controlnet_model_path,
            scheduler=scheduler,
        )

        image = self.controlnet_canny(image_path=image_path)

        if seed_generator == 0:
            random_seed = torch.randint(0, 1000000, (1,))
            generator = torch.manual_seed(random_seed)
        else:
            generator = torch.manual_seed(seed_generator)

        output = pipe(
            prompt=prompt,
            image=image,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images_per_prompt,
            num_inference_step=num_inference_step,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images

        return output

