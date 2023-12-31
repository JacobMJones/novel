import os
import sqlite3
import uuid
from PIL import Image, UnidentifiedImageError
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
# Path to your images folder
images_folder = 'images'

# Normalize the images_folder path
images_folder = os.path.normpath(images_folder)

# Connect to SQLite database
conn = sqlite3.connect('all.db')
cursor = conn.cursor()

# Create the table with necessary fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS image_data (
        id TEXT PRIMARY KEY,
        file TEXT,
        width REAL,
        height REAL,
        size REAL,
        format TEXT,
        type TEXT,
        subtype TEXT,
        tags TEXT,
        path TEXT,
        active INTEGER,
        color TEXT,
        color_rgb TEXT     
    )
''')

# def process_tags(cursor, tags, image_id):
#     for tag in tags.split(','):
#         tag = tag.strip()
#         try:
#             cursor.execute("SELECT tag_id, images_with_tag FROM tags WHERE tag_name = ?", (tag,))
#             result = cursor.fetchone()

#             if result:
#                 tag_id, count = result
#                 cursor.execute("UPDATE tags SET images_with_tag = ? WHERE tag_id = ?", (count + 1, tag_id))
#             else:
#                 tag_id = str(uuid.uuid4())
#                 # Print debugging information for insertion
#                 print(f"Inserting new tag: tag_id={tag_id}, tag_name={tag}")
#                 cursor.execute("INSERT INTO tags (tag_id, tag_name, image_has_tag, images_with_tag) VALUES (?, ?, ?, ?)",
#                                (tag_id, tag, 1, 1))

#             # Check if the image-tag pair already exists in image_tags
#             cursor.execute("SELECT COUNT(*) FROM image_tags WHERE image_id = ? AND tag_id = ?", (image_id, tag_id))
#             if cursor.fetchone()[0] == 0:
#                 cursor.execute("INSERT INTO image_tags (image_id, tag_id) VALUES (?, ?)", (image_id, tag_id))
#             else:
#                 print(f"Image-tag pair already exists: image_id={image_id}, tag_id={tag_id}")

#         except sqlite3.IntegrityError as e:
#             print(f"Integrity Error for tag '{tag}': {e}")
#         except sqlite3.Error as e:
#             print(f"Database Error for tag '{tag}': {e}")

# Function to check if the image already exists in the database
def image_exists(cursor, file_path):
    cursor.execute("SELECT COUNT(*) FROM image_data WHERE path = ?", (file_path,))
    return cursor.fetchone()[0] > 0

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

# Function to get the dominant color
def get_dominant_color_and_name(image_path, color_names):
    with Image.open(image_path) as img:
        img = img.resize((50, 50))
        colors = img.getdata()

        # Check if the image is in grayscale mode
        if img.mode == 'L':
            # Convert grayscale to RGB
            colors = [(color, color, color) for color in colors]

        # Check if the image has an alpha channel (RGBA)
        elif img.mode == 'RGBA':
            # Convert RGBA to RGB
            colors = [color[:-1] for color in colors]  # Discard the alpha values

        most_common = Counter(colors).most_common(1)
        dominant_color = most_common[0][0]

    color_name = closest_color(dominant_color, color_names)
    return dominant_color, color_name


# Traverse the directory, and list directories as dirs and files as files
for dirpath, dirnames, files in os.walk(images_folder):
    for file in files:
        file_path = os.path.join(dirpath, file)

        # Skip if the image already exists in the database
        if image_exists(cursor, file_path):
            print(f"Skipping {file}, already in database.")
            continue

        try:
            # Extracting image details
            with Image.open(file_path) as img:
                width, height = img.size
                format = img.format

            size = os.path.getsize(file_path)

            # Generating a UUID for each image
            unique_id = str(uuid.uuid4())

            # Calculating the relative path
            relative_path = os.path.relpath(file_path)

            # Extracting all folders from the relative path
            folders = relative_path.split(os.sep)[:-1]  # Excludes the file name

            # Creating tags from folder names
            tags = 'manually added'
            tags += ''.join([f', {folder}' for folder in folders if folder])
            dominant_color, color_name = get_dominant_color_and_name(file_path, color_names)
            # Inserting the record into the table
            cursor.execute(
                "INSERT INTO image_data (id, file, width, height, size, format, type, subtype, tags, path, active, color, color_rgb) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (unique_id, file, width, height, size, format, 'image', 'art', tags, relative_path, 1, color_name, str(dominant_color))
            )
            print(f"Added {file} to image_data with ID {unique_id}, path: {relative_path}.")
            # process_tags(cursor, tags, unique_id)
        except UnidentifiedImageError as e:
            print(f"Error processing file {file}: {e}")
        # process_tags(cursor, tags, unique_id)
# Commit the changes and close the database connection
conn.commit()
conn.close()

print("All images processed and data stored in database. You're all set, my coding maestro!")
