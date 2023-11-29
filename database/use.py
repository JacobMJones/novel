import sqlite3
import re

# Step 1: Read the Text File
with open('tao.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Step 2: Parse the Chapters
# Assuming each chapter starts with a number and a newline, like "1\nChapter text..."
chapters = re.split(r'\n(?=\d+\n)', text)

# Step 3: Create a SQLite Database
conn = sqlite3.connect('tao.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS chapters (id INTEGER PRIMARY KEY, text TEXT)')

# Step 4: Insert Chapters into Database
for chapter in chapters:
    chapter_number = chapter.split('\n', 1)[0].strip()
    chapter_text = chapter.split('\n', 1)[1].strip()
    c.execute('INSERT INTO chapters (id, text) VALUES (?, ?)', (chapter_number, chapter_text))

# Commit changes and close the connection
conn.commit()
conn.close()
