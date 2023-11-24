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
        active INTEGER
    )
''')

# Function to check if the image already exists in the database
def image_exists(cursor, file_path):
    cursor.execute("SELECT COUNT(*) FROM image_data WHERE path = ?", (file_path,))
    return cursor.fetchone()[0] > 0

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

            # Creating tags from folder names, including 'art' and 'africa' by default
            tags = 'manually added, 19th'
            tags += ''.join([f', {folder}' for folder in folders if folder])

            # Inserting the record into the table
            cursor.execute(
                "INSERT INTO image_data (id, file, width, height, size, format, type, subtype, tags, path, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (unique_id, file, width, height, size, format, 'image', 'art', tags, relative_path, 1)
            )

            print(f"Added {file} to image_data with ID {unique_id}, path: {relative_path}.")

        except UnidentifiedImageError as e:
            print(f"Error processing file {file}: {e}")

# Commit the changes and close the database connection
conn.commit()
conn.close()

print("All images processed and data stored in database. You're all set, my coding maestro!")
