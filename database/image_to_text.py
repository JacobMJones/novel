import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np

# Load the pre-trained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

def recognize_objects(image_path):
    # Load and preprocess the image
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make predictions
    predictions = model.predict(img_array)

    # Decode and print the predictions
    print('Predictions:', decode_predictions(predictions, top=3)[0])

# Replace 'path_to_your_image.jpg' with the path to your image
image_path = '1.jpg'
recognize_objects(image_path)
