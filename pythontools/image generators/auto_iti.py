import os
import random
import uuid
from PIL import Image
from diffusers import StableDiffusionImg2ImgPipeline
import torch

# Load the model
model_id_or_path = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
pipe.safety_checker = None
pipe = pipe.to("cuda")

# Directory path for the images folder
images_folder = "../../database/images/new"

# Loop over the parameter combinations
while True:
        # Update the list of files in the images folder
    image_files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f))]

    # Select a random image file and remove it from the list for this iteration
    random_image_file = random.choice(image_files)
    image_files.remove(random_image_file)

    # Load and prepare the initial image
    init_image = Image.open(os.path.join(images_folder, random_image_file)).convert("RGB").resize((512, 512))

    # Define the prompt
    prompt = "A crowded theater in victorian england, robots jostle for space in the grand opera house."

    # Generate the image and save it with a random filename in the photos folder
    num_inference_steps = 40
    images = pipe(prompt=prompt, image=init_image, strength=.65, guidance_scale=9).images
    filename = os.path.join(images_folder, f"{uuid.uuid4()}.png")
    images[0].save(filename)

