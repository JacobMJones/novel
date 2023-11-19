import os
import random
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch

# Load the model
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe.safety_checker = None
pipe = pipe.to("cuda")

# Directory path for the images folder
images_folder = "../images"

# Get a list of files in the images folder
image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]



# Define the ranges for guidance scale and image strength
guidance_scales = [5, 6, 7, 8, 8.5]
strength_values = [0.6, 0.65, 0.7, 0.9]

# Counter for unique filenames
counter = 1

# Loop over the parameter combinations
for guidance_scale in guidance_scales:
    for strength in strength_values:
        # Select a random image file
        random_image_file = random.choice(image_files)

# Load and prepare the initial image
        init_image = Image.open(os.path.join(images_folder, random_image_file)).convert("RGB").resize((512, 512))

        # Define the prompt
        prompt = "An oil painting of flowers in the style of Van Gogh, uplifting, detailed"
        # Generate the image
        num_inference_steps = 20 
        images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale).images

        # Save the image with a unique filename
        filename = f"guide{guidance_scale}-str-{int(strength * 10)}-c{counter}.png"
        images[0].save(filename)

        # Increase the counter for the next filename
        counter += 1

        # Repeat the process for a second image with the same parameters
        images = pipe(prompt=prompt, image=init_image, strength=strength, guidance_scale=guidance_scale,num_inference_steps=num_inference_steps).images
        filename = f"guide{guidance_scale}-str-{int(strength * 10)}-c{counter}.png"
        images[0].save(filename)
        counter += 1