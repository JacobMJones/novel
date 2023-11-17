from diffusers import DiffusionPipeline
import torch
import os
import pandas as pd
import random
import uuid

base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
"stabilityai/stable-diffusion-xl-base-1.0"
torch.backends.cuda.matmul.allow_tf32 = True
base.safety_checker = None
base.to("cuda")
refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)

refiner.to("cuda")

# Define how many steps 
n_steps = 2
# ratio between base and refinement, higher number is more base
high_noise_frac = 0.7

#Reading the Excel file
excel_path = os.path.join(os.path.dirname(__file__), '..', 'text_data.xlsx')
df = pd.read_excel(excel_path)
# Selecting a random row from the 'content' column
prompt = random.choice(df['content'].dropna()) + ", Joe Sacco,Moebius, illustration, simple, beautiful, masterpiece"
print("Prompt:",prompt)
negative_prompt = 'realistic, photograph, blurry, bad, shit, ugly, poor'

# run base and refiner
image = base(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=n_steps,
    denoising_end=high_noise_frac,
    output_type="latent",
).images
image = refiner(
    prompt=prompt,
     negative_prompt=negative_prompt,
    num_inference_steps=n_steps,
    denoising_start=high_noise_frac,
    image=image,
).images[0]

# Define the folder and filename
folder_path = 'results'  

random_string = str(uuid.uuid4())
file_name = random_string + '.png'

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Save the image
image_path = os.path.join(folder_path, file_name)
image.save(image_path)
print(f"Image saved to {image_path}")
