import sqlite3
import requests
from PIL import Image
from collections import Counter

color_names = {
    "Red": (255, 0, 0),
    "Green": (0, 128, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Pink": (255, 192, 203),
    "Brown": (165, 42, 42),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray": (128, 128, 128),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Lime": (0, 255, 0),
    "Maroon": (128, 0, 0),
    "Olive": (128, 128, 0),
    "Navy": (0, 0, 128),
    "Teal": (0, 128, 128),
    "Aqua": (0, 255, 255),
    "Fuchsia": (255, 0, 255),
    "Silver": (192, 192, 192),
    "Gold": (255, 215, 0),
    "Beige": (245, 245, 220),
    "Coral": (255, 127, 80),
    "Ivory": (255, 255, 240),
    "Khaki": (240, 230, 140),
    "Lavender": (230, 230, 250),
    "Mint": (189, 252, 201),
    "Navy Blue": (0, 0, 128),
    "Tomato": (255, 99, 71)
}
import sqlite3


# Function to find the closest color name
def closest_color(rgb, color_names):
    if not color_names:
        raise ValueError("Color names dictionary is empty")

    r, g, b = rgb
    color_diffs = []
    for color_name, color_value in color_names.items():
        cr, cg, cb = color_value
        color_diff = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        color_diffs.append((color_diff, color_name))

    if not color_diffs:
        raise ValueError("No color differences calculated")

    return min(color_diffs)[1]
# Function to get the dominant color and its name
def get_dominant_color_and_name(image_path, color_names):
    with Image.open(image_path) as img:
        img = img.resize((50, 50))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        colors = img.getdata()
        most_common = Counter(colors).most_common(1)
        dominant_color = most_common[0][0]
    color_name = closest_color(dominant_color, color_names)
    return dominant_color, color_name

# Function to retrieve image paths and IDs from a SQLite database
def get_image_data(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, path FROM image_data")
    image_data = cursor.fetchall()
    conn.close()
    return image_data

# Function to send the color information to the Flask server
def update_color_on_server(image_id, rgb, color_name, server_url):
    payload = {
        'id': image_id,
        'color_rgb': str(rgb),
        'color': color_name
    }
    response = requests.post("http://localhost:5000/update_color", json=payload)
    if response.status_code == 200:
        print('Color updated:', response.json())
    else:
        print('Error updating color:', response.status_code, response.text)

# Main script execution
def process_images(db_path, server_url, color_names):
    image_data = get_image_data(db_path)
    for image_id, path in image_data:
        rgb, color_name = get_dominant_color_and_name(path, color_names)
        update_color_on_server(image_id, rgb, color_name, server_url)

# Define the database path, Flask server URL, and color names
db_path = 'database.db'
server_url = 'http://localhost:5000'

# Run the script
process_images(db_path, server_url, color_names)