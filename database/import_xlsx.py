import pandas as pd
import sqlite3
import uuid


## A script for loading and preparing excel files in different shapes
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_rumi_poetry_into_db(file_path, table_name):
    # Read the Excel file
    df = pd.read_excel(file_path, usecols=['Title', 'Poem'], keep_default_na=False)

    # Rename 'Poem' column to 'text' and ensure whitespace is preserved
    df = df.rename(columns={'Poem': 'text'})

    # Debugging: Print some entries to verify whitespace
    print("Debugging DataFrame Entries:")
    print(df['text'].head())

    # Additional fields
    df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    df['active'] = 1
    df['likes'] = 0
    df['type'] = 'poetry'
    df['subtype'] = 'rumi'
    df['tags'] = 'persian, 13th century'

    # Insert into database
    conn = get_db_connection()
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()

if __name__ == "__main__":
    insert_rumi_poetry_into_db("rumi_poetry.xlsx", "text_all")