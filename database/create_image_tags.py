import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the image_tags table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS image_tags (
  image_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  FOREIGN KEY (image_id) REFERENCES image_data(id),
  FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
  PRIMARY KEY (image_id, tag_id)
)
""")

# Select all tags from image_data
cursor.execute("SELECT id, tags FROM image_data")
rows = cursor.fetchall()

# A set to keep track of all unique tags
unique_tags = set()

# Process each row for unique tags
for row in rows:
    tags = row[1].split(',')  # Split the tags by comma
    unique_tags.update([tag.strip().lower() for tag in tags])  # Normalize and add tags to the set

# Insert unique tags into the tags table
for tag in unique_tags:
    cursor.execute("SELECT tag_id FROM tags WHERE tag_name = ?", (tag,))
    tag_record = cursor.fetchone()
    if tag_record is None:
        cursor.execute("INSERT INTO tags (tag_name) VALUES (?)", (tag,))
        conn.commit()
        tag_id = cursor.lastrowid
    else:
        tag_id = tag_record[0]

    # Now, find all images that have this tag and insert into image_tags
    for row in rows:
        image_id = row[0]
        image_tags = [t.strip().lower() for t in row[1].split(',')]
        if tag in image_tags:
            cursor.execute("INSERT OR IGNORE INTO image_tags (image_id, tag_id) VALUES (?, ?)", (image_id, tag_id))

# Commit the changes and close the connection
conn.commit()
conn.close()
