import torch
import os

from typing import List, Optional, Union
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

from dreamdraw_api.utils import get_scheduler
from dreamdraw_api import config

class StableDiffusionImg2ImgGenerator:
    def __init__(self, hf_token:str=config.HUGGINGFACE_TOKEN):
        torch.backends.cuda.matmul.allow_tf32 = True
        self.pipe = None
        self.hf_token = hf_token

    def load_model(self, model_path, scheduler):
        if self.pipe is None:
            self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_path,
                safety_checker=None,
                torch_dtype=torch.float16,
                use_auth_token=self.hf_token,
            )
        self.device = ""
        if torch.backends.mps.is_available():
            self.device = "mps"
        else: 
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.pipe = get_scheduler(pipe=self.pipe, scheduler=scheduler)
        self.pipe.to(self.device)
        self.pipe.enable_sequential_cpu_offload()
        self.pipe.enable_attention_slicing(1)
        self.pipe.enable_xformers_memory_efficient_attention()
  
        return self.pipe

    def generate_image(
        self,
        image_path: str,
        model_path: str,
        prompt: str,
        negative_prompt: str,
        num_images_per_prompt: int,
        scheduler: str,
        guidance_scale: int,
        num_inference_step: int,
        seed_generator=0,
    ):

        pipe = self.load_model(model_path=model_path, scheduler=scheduler)

        if seed_generator == 0:
            random_seed = torch.randint(0, 1000000, (1,))
            generator = [torch.Generator(device="cuda").manual_seed(random_seed + i) for i in range(num_images_per_prompt)]
        else:
            generator = [torch.Generator(device="cuda").manual_seed(seed_generator + i) for i in range(num_images_per_prompt)]

        image = Image.open(image_path)
        images = pipe(
            prompt,
            image=image,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images_per_prompt,
            num_inference_step=num_inference_step,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images

        return images

