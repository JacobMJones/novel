import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the tags table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tags (
  tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag_name TEXT NOT NULL UNIQUE,
  image_has_tag BOOLEAN NOT NULL DEFAULT 1,
  text_has_tag BOOLEAN NOT NULL DEFAULT 0
)
""")

# Select all tags from image_data
cursor.execute("SELECT id, tags FROM image_data")
rows = cursor.fetchall()

# This set will ensure each tag is only added once
unique_tags = set()

# Process each row
for row in rows:
    image_id, tags_string = row
    tags = tags_string.split(',')  # Split the tags by comma
    for tag in tags:
        clean_tag = tag.strip().lower()  # Convert tags to lowercase and strip whitespace
        if clean_tag: 
            unique_tags.add(clean_tag) # Check if the tag is empty
        else:   
            error_message = f"Blank tag found in image ID {image_id} with original tag string: '{tags_string}'"
            print(error_message)
        

# Insert unique tags into the tags table
for tag in unique_tags:
    # Avoid inserting duplicate tags
    cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag,))

# Commit the changes and close the connection
conn.commit()
conn.close()
