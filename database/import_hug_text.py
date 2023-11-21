from datasets import load_dataset
import pandas as pd
import sqlite3
import uuid

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def load_and_insert_data(dataset_name, table_name):
    # Load dataset from Hugging Face
    dataset = load_dataset(dataset_name)

    # Convert to pandas DataFrame
    df = pd.DataFrame(dataset['train'])

    # Convert column names to lowercase
    df.columns = [col.lower() for col in df.columns]
    # Filter out rows where 'text' column has more than 200 characters
    df = df[df['text'].str.len() <= 200]
    # Add a UUID to each row
    df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]

    # Add additional fields with default values
    df['active'] = 1
    df['likes'] = 0
    df['type'] = 'poetry'
    df['subtype'] = 'classical european'
    df['tags'] = None  # Or use '' for an empty string

    # Insert into database
    conn = get_db_connection()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    # Example usage
    load_and_insert_data("DanFosing/public-domain-poetry", "text_all")
