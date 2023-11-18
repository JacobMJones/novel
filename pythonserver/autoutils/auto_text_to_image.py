from diffusers import DiffusionPipeline
import torch
import os
import pandas as pd
import random
import uuid


#set up base
model_id = "nitrosocke/Ghibli-Diffusion"
base = DiffusionPipeline.from_pretrained(model_id)
base.safety_checker = None
base.to(torch_device="cuda", torch_dtype=torch.float32)

#read excel file, used for prompt generation
excel_path = os.path.join(os.path.dirname(__file__), '..', 'text_data.xlsx')
dataframe = pd.read_excel(excel_path)

#set folder path
folder_path = '../images'

#set parameters
n_steps = 20
high_noise_frac = 0.75

while True:

    #Prompt from text_data
    #prompt = random.choice(dataframe['content'].dropna()) + ", Joe Sacco,Moebius, illustration, simple, beautiful, masterpiece"

    #Static Prompt
    prompt = "ghibli style, Joe Sacco, Moebius, Daniel Clowes, illustration, simple, beautiful, portrait, kind face, masterpiece"

    #Dynamic Prompt --this will use random selection, Mad Lib style, to make prompts
    

    negative_prompt = 'bad anatomy, blurry, child, young, ugly, low quality, soft, soft blurry'


    image = base(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=n_steps,
    denoising_end=high_noise_frac
    ).images

   

    ####################
    #save image as file#
    ####################

    #generate random file name
    file_name = str(uuid.uuid4()) + '.png'

    #Create folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    #Save the image
    image_path = os.path.join(folder_path, file_name)
    image[0].save(image_path)
    print(f"Image saved to {image_path}")




# output_type = latent is used for further processing, like, I am guessing a refiner. 

# prompt: A string or a list of strings specifying the text prompt(s) to guide the image generation.
# num_inference_steps: The number of denoising steps.
# guidance_scale: The scale for classifier-free guidance.
# generator: An optional Python generator or torch.Generator for reproducibility.
# height: The height of the generated image in pixels.
# width: The width of the generated image in pixels.
# seed: A seed for reproducibility of the generation.
# eta: A parameter for stochastic sampling; lowering this can lead to less random results.
# callback: An optional callback function to get updates on the image generation process.