
import torch
from diffusers import DiffusionPipeline
from typing import Optional
from PIL.Image import Image

from dreamdraw_api.utils import STABLE_INPAINT_MODEL_LIST
from dreamdraw_api import config

class StableDiffusionInpaintGenerator:
    def __init__(self, hf_token:str=config.HUGGINGFACE_TOKEN):
        self.pipe = None
        self.hf_token = hf_token

    def load_model(self, model_path:Optional[str]=STABLE_INPAINT_MODEL_LIST[0]):
        if self.piple is None:
            self.model_path = model_path
            self.pipe = DiffusionPipeline.from_pretrained(
                model_path,
                revision="fp16",
                torch_dtype=torch.float16,
                use_auth_token=self.hf_token
            )

        self.pipe.to("cuda")
        self.pipe.enable_xformers_memory_efficient_attention()

        return self.pipe

    def generate_image(
        self,
        init_image: Image,
        mask_image: Image,
        prompt: str,
        negative_prompt: str,
        num_images: int=1,
        guidance_scale: int=7.5,
        num_inference_steps: int=50,
        seed_generator:int=0,
    ):
        init_image = init_image.resize((512, 512))
        mask_image = mask_image.resize((512, 512))
        pipe = self.load_model()

        if seed_generator == 0:
            random_seed = torch.randint(0, 1000000, (1, ))
            generator = torch.manual_seed(random_seed)
        else:
            generator = torch.manual_seed(seed_generator)

        output = pipe(
            prompt=prompt,
            image=init_image,
            mask_image=mask_image,
            negative_prompt=negative_prompt,
            num_images_per_prompt=num_images,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            generator=generator,
        ).images

        return output

    
