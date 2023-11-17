from diffusers import DiffusionPipeline
import torch
import random
import pandas as pd
import os
import uuid

#make pipeline
pipe = DiffusionPipeline.from_pretrained("wavymulder/Analog-Diffusion")
pipe.safety_checker = None
pipe.to(torch_device="cuda", torch_dtype=torch.float32)


#read excel file
excel_path = os.path.join(os.path.dirname(__file__), '..', 'text_data.xlsx')
df = pd.read_excel(excel_path)

while True:
    
    #prompt from text_data, selecting a random row from the 'content' column
    prompt = random.choice(df['content'].dropna()) + ", analog style, life affirming, positive, detailed, beautiful"
    
    #static prompt
    #prompt = "happy, bunny, dance, marathon"
    
    # Negative prompt (constant)
    negative_prompt = 'blurry'

    num_inference_steps = 40

    images = pipe(prompt=prompt, 
                  negative_prompt=negative_prompt,
                  num_inference_steps=num_inference_steps,
                  guidance_scale=6.0, lcm_origin_steps=70, output_type="pil").images

    # Save each image as a PNG file
    folder_path = '../images'  
    random_string = str(uuid.uuid4())
    file_name = random_string + '.png'

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Save the image
    image_path = os.path.join(folder_path, file_name)
    images[0].save(image_path)
    print(f"Image saved to {image_path}")
