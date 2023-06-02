import os
from io import BytesIO
from uuid import uuid4
from fastapi import APIRouter, Depends, Body, Header, Response

from PIL import Image
from dreamdraw_api.services.storage.storage_service import save_image
from dreamdraw_api.services.stablediffusion import (
    StableDiffusionImg2ImgGenerator,
    StableDiffusionInpaintGenerator,
    StableDiffusionText2ImageGenerator
)
from dreamdraw_api import config
from dreamdraw_api.schema.generate import (
    Text2ImgCreateRequest,
    Img2ImgCreateRequest,
    StableDiffusionResponse,
    InpaintCreateRequest
)

generate_api = APIRouter()

@generate_api.post('/text2img', response_model=StableDiffusionResponse, name="generate_api:text2img")
async def text2img(
    create_request: Text2ImgCreateRequest=Body(...),
    sd_gen: StableDiffusionText2ImageGenerator=Depends(StableDiffusionText2ImageGenerator)
    ):

    task_id = str(uuid4())

    image = await sd_gen.generate_image(
        model_path=create_request.model,
        prompt=create_request.prompt,
        negative_prompt=create_request.negative_prompt,
        num_images_per_prompt=create_request.num_images,
        scheduler=create_request.scheduler,
        guidance_scale=create_request.guidance_scale,
        num_inference_step=create_request.num_inference_step,
        height=create_request.height,
        width=create_request.width,
        seed_generator=create_request.seed_generator
    ).images[0]

    info = {
        "task": "text2img",
        "prompt": create_request.prompt,
        "negative_prompt": create_request,
        "num_images": create_request.num_images,
        "guidance_scale": create_request.guidance_scale,
        "height": create_request.height,
        "width": create_request.width,
        "num_inference_steps": create_request.num_inference_step,
    }
    '''
    image_paths = save_image(images, task_id, info=info)
    urls = [os.path.join(config.IMAGESERVER_URL, path) for path in image_paths]

    response = StableDiffusionResponse(task_id=task_id, image_urls=urls)
    return response
    '''

    image.save("testimage.png")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    imgstr = base64.b64encode(buffer.getvalue())

    return Response(content=imgstr, media_type="image/png")



@generate_api.post('/img2img', response_model=StableDiffusionResponse, name="generate_api:img2img")
async def img2img(
    create_request: Img2ImgCreateRequest=Body(...),
    sd_gen: StableDiffusionImg2ImgGenerator=Depends(StableDiffusionImg2ImgGenerator),
    ):

    init_image = Image.open(create_request.init_image.file).convert("RGB")
    task_id = str(uuid4())

    images = await sd_gen.generate_image(
        init_image=init_image,
        model_path=create_request.model,
        prompt=create_request.prompt,
        negative_prompt=create_request.negative_prompt,
        num_images_per_prompt=create_request.num_images,
        scheduler=create_request.scheduler,
        guidance_scale=create_request.guidance_scale,
        num_inference_step=create_request.num_images,
        height=create_request.height,
        width=create_request.width,
        seed_generator=create_request.seed_generator
    )

    info = {
        "task": "img2img",
        "prompt": create_request.prompt,
        "negative_prompt": create_request.negative_prompt,
        "strength": create_request.strength,
        "guidance_scale": create_request.guidance_scale,
        "seed": create_request.seed_generator,
        "num_inference_steps": create_request.num_inference_step,
    }

    image_paths = save_image(images, task_id, info=info)
    init_image.save(os.path.join(config.TEMP_DIR, task_id, "init_image.webp"))
    urls = [os.path.join(config.IMAGESERVER_URL, path) for path in image_paths]

    response = StableDiffusionResponse(task_id=task_id, image_urls=urls)
    return response

@generate_api.post("/inpaint", response_model=StableDiffusionResponse, name="generate_api:inpaint")
def inpaint(
    create_request: InpaintCreateRequest=Body(...),
    sd_gen: StableDiffusionInpaintGenerator=Depends(StableDiffusionInpaintGenerator),
):
    init_image = Image.open(create_request.init_image.file).convert("RGB")
    mask_image = Image.open(create_request.mask_image.file).convert("RGB")
    task_id = str(uuid4())

    images = sd_gen.generate_image(
        init_image=init_image,
        mask_image=mask_image,
        prompt=create_request.prompt,
        negative_prompt=create_request.negative_prompt,
        num_images=create_request.num_images,
        guidance_scale=create_request.guidance_scale,
        num_inference_steps=create_request.num_inference_step,
        seed_generator=create_request.seed_generator,
    )

    info = {
        "task": "inpaint",
        "prompt": create_request.prompt,
        "strength": create_request.strength,
        "guidance_scale": create_request.guidance_scale,
        "seed": create_request.seed_generator,
        "num_inference_steps": create_request.num_inference_step
    }

    image_paths = save_image(images, task_id, info=info)
    init_image.save(os.path.join(config.TEMP_DIR, task_id, "init_image.webp"))
    mask_image.save(os.path.join(config.TEMP_DIR, task_id, "mask_image.webp"))
    urls = [os.path.join(config.IMAGESERVER_URL, path) for path in image_paths]

    response = StableDiffusionResponse(task_id=task_id, image_urls=urls)
    return response
