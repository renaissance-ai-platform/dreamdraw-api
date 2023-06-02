
from pydantic import BaseModel, Field, HttpUrl
from fastapi import UploadFile
from typing import Optional, List, Union

from dreamdraw_api.utils import STABLE_MODEL_LIST, SCHEDULER_LIST

class StableDiffusionBaseRequest(BaseModel):
    model:str=STABLE_MODEL_LIST[0]
    prompt: str = Field(..., description="Image Create Prompt")
    negative_prompt: str = Field(..., description="Image Create Negative Prompt")
    seed_generator: Optional[int] = 42
    num_images: Optional[int] = 1
    scheduler: Optional[str] = SCHEDULER_LIST[0]
    guidance_scale: Optional[int] = 7.5
    num_inference_step: int = 50
    height: Optional[int] = 512
    width: Optional[int] = 512

class Text2ImgCreateRequest(StableDiffusionBaseRequest):
    pass
    

class Img2ImgCreateRequest(StableDiffusionBaseRequest):
    init_image: UploadFile
    strength: float

class InpaintCreateRequest(Img2ImgCreateRequest):
    mask_image: UploadFile
    

class StableDiffusionResponse(BaseModel):
    task_id: str = Field(..., description="Task ID")
    image_urls: List[Union[str, HttpUrl]] = Field(..., description="Image URLs")
