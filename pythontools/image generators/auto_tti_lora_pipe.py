import torch
from diffusers import LCMScheduler, AutoPipelineForText2Image
import uuid
import os

model_id = "stabilityai/stable-diffusion-xl-base-1.0"
adapter_id = "latent-consistency/lcm-lora-sdxl"

# Set folder path
folder_path = '../../database/images/new/'

pipe = AutoPipelineForText2Image.from_pretrained(model_id, torch_dtype=torch.float16, variant="fp16")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.safety_checker = None
pipe.to("cuda")

# Load and fuse lcm lora
pipe.load_lora_weights(adapter_id)
pipe.fuse_lora()

while True:
    prompt = "An illustration of a man looking in a mirror and seeing a different man reflected."
    image = pipe(prompt=prompt, num_inference_steps=7, guidance_scale=.8).images[0]
    file_name = str(uuid.uuid4()) + '.png'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image_path = os.path.join(folder_path, file_name)
    image.save(image_path)
    print(f"Image saved to {image_path}")


