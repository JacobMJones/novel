from diffusers import DiffusionPipeline
import torch
import os

# load both base & refiner
base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
)
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

# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 30
high_noise_frac = 0.6

prompt = "Joe Sacco, Daniel Clowes, Moebius, illustration, dramatic, exploding, tree of life"

# run both experts
image = base(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_end=high_noise_frac,
    output_type="latent",
).images
image = refiner(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_start=high_noise_frac,
    image=image,
).images[0]

# Define the folder and filename
folder_path = 'results'  # Replace with your actual folder path
file_name = 'please.png'

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Save the image
image_path = os.path.join(folder_path, file_name)
image.save(image_path)
print(f"Image saved to {image_path}")
