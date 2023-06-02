from PIL import Image

from diffusers import (
    DDIMScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    HeunDiscreteScheduler,
    LMSDiscreteScheduler,
    UniPCMultistepScheduler,
)

SCHEDULER_LIST = [
    "DDIM",
    "EulerA",
    "Euler",
    "LMS",
    "Heun",
    "UniPC",
]

REALISTIC_STABLE_MODEL = "SG161222/Realistic_Vision_V2.0"
DEAM_STABLE_MODEL = "dreamlike-art/dreamlike-diffusion-1.0"

STABLE_MODEL_LIST = [
    "stabilityai/stable-diffusion-2-1",
    "prompthero/openjourney-v4",
]

STABLE_INPAINT_MODEL_LIST = [
    "stabilityai/stable-diffusion-2-inpainting",
    "runwayml/stable-diffusion-inpainting",
    "SG161222/Realistic_Vision_V2.0"
]


CONTROLNET_CANNY_MODEL_LIST = [
    "lllyasviel/sd-controlnet-canny",
    "lllyasviel/control_v11p_sd15_canny",
    "thibaud/controlnet-sd21-canny-diffusers",
]

CONTROLNET_DEPTH_MODEL_LIST = [
    "lllyasviel/sd-controlnet-depth",
    "lllyasviel/control_v11f1p_sd15_depth",
    "thibaud/controlnet-sd21-depth-diffusers",
]

CONTROLNET_SCRIBBLE_MODEL_LIST = [
    "lllyasviel/sd-controlnet-scribble",
    "lllyasviel/control_v11p_sd15_scribble",
    "thibaud/controlnet-sd21-scribble-diffusers",
]

def image_grid(imgs, rows, cols):
    assert len(imgs) == rows * cols

    w, h = imgs[0].size
    grid = Image.new("RGB", size=(cols * w, rows * h))

    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid

def get_scheduler(pipe, scheduler):
    if scheduler == SCHEDULER_LIST[0]:
        pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
    elif scheduler == SCHEDULER_LIST[1]:
        pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    elif scheduler == SCHEDULER_LIST[2]:
        pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config)
    elif scheduler == SCHEDULER_LIST[3]:
        pipe.scheduler = LMSDiscreteScheduler.from_config(pipe.scheduler.config)
    elif scheduler == SCHEDULER_LIST[4]:
        pipe.scheduler = HeunDiscreteScheduler.from_config(pipe.scheduler.config)
    elif scheduler == SCHEDULER_LIST[5]:
        pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
        
    return pipe