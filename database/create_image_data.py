import os
import sqlite3
import uuid
from PIL import Image, UnidentifiedImageError



######### SCANS IMAGES folder and creates table


# Path to your images folder
images_folder = 'images'

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the new table
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
        active INTEGER
    )
''')

# List all files and directories in the images folder
all_items = os.listdir(images_folder)

# Process each item in the folder
for item in all_items:
    item_path = os.path.join(images_folder, item)

    # Check if the item is a file
    if os.path.isfile(item_path):
        try:
            # Extracting image details
            with Image.open(item_path) as img:
                width, height = img.size
                format = img.format

            size = os.path.getsize(item_path)

            # Generating a UUID for each image
            unique_id = str(uuid.uuid4())

            # Inserting the record into the new table
            cursor.execute(
                "INSERT INTO image_data (id, file, width, height, size, format, type, subtype, tags, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (unique_id, item, width, height, size, format, 'image', 'art', 'painting, surreal, Piet Mondrian', 1)
            )

            print(f"Added {item} to image_data with ID {unique_id}.")

        except UnidentifiedImageError as e:
            print(f"Error processing file {item}: {e}")
    else:
        print(f"Skipped directory {item}")

# Commit the changes and close the connection
conn.commit()
conn.close()
