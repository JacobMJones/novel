from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

init_image = Image.open("robots.png").convert("RGB").resize((768, 512))
prompt = "Robots Marching, Moebius"

images = pipe(prompt=prompt, image=init_image, strength=0.15, guidance_scale=1.5).images
images[0].save("f.png")

# from PIL import Image
# from diffusers import StableDiffusionImg2ImgPipeline
# import torch
# import os
# import uuid
# model_id_or_path = "runwayml/stable-diffusion-v1-5"
# pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
# pipe.safety_checker = None
# pipe = pipe.to("cuda")

# init_image = Image.open("./results/health.png").convert("RGB").resize((512, 512))
# prompt = "simple line drawing, positive, black and white"

# images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images


# # Define the folder and filename
# folder_path = 'results'  
# random_string = str(uuid.uuid4())
# file_name = random_string + '.png'
# image_path = os.path.join(folder_path, file_name)
# images[0].save(image_path)
# print(f"Image saved to {image_path}")