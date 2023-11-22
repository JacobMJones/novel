import os
import sqlite3
import uuid
from PIL import Image, UnidentifiedImageError

# Path to your images folder
images_folder = 'images'

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Retrieve the list of files already in the database
cursor.execute('SELECT file FROM new_image_data')
existing_files = {row[0] for row in cursor.fetchall()}

# List all files in the images folder
all_items = os.listdir(images_folder)

# Process each item in the folder
for item in all_items:
    item_path = os.path.join(images_folder, item)

    # Check if the item is a new file
    if os.path.isfile(item_path) and item not in existing_files:
        try:
            # Extracting image details
            with Image.open(item_path) as img:
                width, height = img.size
                format = img.format

            size = os.path.getsize(item_path)

            # Generating a UUID for each new image
            unique_id = str(uuid.uuid4())

            # Inserting the record into the new table
            cursor.execute(
                "INSERT INTO new_image_data (id, file, width, height, size, format, type, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (unique_id, item, width, height, size, format, 'image', 1)
            )

            print(f"Added {item} to new_image_data with ID {unique_id}.")

        except UnidentifiedImageError as e:
            print(f"Error processing file {item}: {e}")


# Commit the changes and close the connection
conn.commit()
conn.close()
