
import torch
import os

from diffusers import StableDiffusionPipeline
from dreamdraw_api.utils import get_scheduler
from dreamdraw_api import config

class StableDiffusionText2ImageGenerator:
    def __init__(self, hf_token: str=config.HUGGINGFACE_TOKEN):
        self.pipe = None
        self.hf_token = hf_token

    def load_model(self, model_path, scheduler):
        if self.pipe is None:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_path,
                safety_checker=None,
                torch_dtype=torch.float16,
                use_auth_token=self.hf_token
            )
        if torch.backends.mps.is_available():
            device = "mps"
        else: 
            device = "cuda" if torch.cuda.is_available() else "cpu"

        self.pipe = get_scheduler(pipe=self.pipe, scheduler=scheduler)
        self.pipe.to(device)
        self.pipe.enable_xformers_memory_efficient_attention()

        return self.pipe

    def generate_image(
        self,
        model_path: str,
        prompt: str,
        negative_prompt: str,
        num_images_per_prompt: int,
        scheduler: str,
        guidance_scale: int,
        num_inference_step: int,
        height: int,
        width: int,
        seed_generator=0,
    ):
        pipe = self.load_model(model_path=model_path, scheduler=scheduler)
        if seed_generator == 0:
            random_seed = torch.randint(0, 1000000, (1,))
            generator = torch.manual_seed(random_seed)
        else:
            generator = torch.manual_seed(seed_generator)

        images = pipe(
            prompt=prompt,
            height=height,
            width=width,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images_per_prompt,
            num_inference_step=num_inference_step,
            guidance_scale=guidance_scale,
            generator=generator
        ).images

        return images

