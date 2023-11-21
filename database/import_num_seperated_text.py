import pandas as pd
import sqlite3
import uuid
import re

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn



def insert_chapters_into_db(file_path, table_name):
    # Read the entire text file
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Split the text into chapters based on numbers
    chapters = re.split(r'\n\d+\n', text)

    # Prepare a DataFrame for the chapters
    df = pd.DataFrame({'text': chapters})
    df['text'] = df['text'].str.strip()  # Remove leading/trailing whitespace
    df = df[df['text'].str.len() > 0]  # Filter out empty chapters

    # Add additional fields
    df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df['active'] = 1
    df['likes'] = 0
    df['type'] = 'poetry'
    df['subtype'] = 'tao'
    df['tags'] = 'philosophy, east asian'

    # Insert into database
    conn = get_db_connection()
    df.to_sql(table_name, conn, if_exists='append', index=False)  # Use 'append' instead of 'replace'
    conn.close()

if __name__ == "__main__":
    insert_chapters_into_db("tao.txt", "text_all")
