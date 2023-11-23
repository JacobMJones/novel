import os
import sqlite3
import uuid
from PIL import Image, UnidentifiedImageError

# Path to your images folder
images_folder = 'images'

# Normalize the images_folder path
images_folder = os.path.normpath(images_folder)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Update the table creation statement to include 'path'
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
        active INTEGER
    )
''')

# Traverse the directory, and list directories as dirs and files as files
for dirpath, dirnames, files in os.walk(images_folder):
    for file in files:
        file_path = os.path.join(dirpath, file)

        try:
            # Extracting image details
            with Image.open(file_path) as img:
                width, height = img.size
                format = img.format

            size = os.path.getsize(file_path)

            # Generating a UUID for each image
            unique_id = str(uuid.uuid4())

            # Extracting folder name from dirpath
            folder_name = os.path.basename(dirpath)

            # Preparing tags, include folder name if it's not the root images_folder
            tags = 'painting, surreal, Piet Mondrian'
            if dirpath != images_folder:
                tags += f', {folder_name}'

            # Calculating the relative path
            relative_path = os.path.relpath(file_path)

            # Inserting the record into the new table, including the relative path
            cursor.execute(
                "INSERT INTO image_data (id, file, width, height, size, format, type, subtype, tags, path, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (unique_id, file, width, height, size, format, 'image', 'art', tags, relative_path, 1)
            )

            print(f"Added {file} to image_data with ID {unique_id}, path: {relative_path}.")

        except UnidentifiedImageError as e:
            print(f"Error processing file {file}: {e}")

# Commit the changes and close the connection
conn.commit()
conn.close()
