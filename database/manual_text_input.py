import sqlite3
import uuid

def create_table_if_not_exists():
    # Connect to the database
    conn = sqlite3.connect('all.db')
    cursor = conn.cursor()

    # SQL query to create the table if it doesn't exist
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS me_text (
        id TEXT PRIMARY KEY,
        title TEXT,
        text TEXT,
        type TEXT,
        tags TEXT,
        active INTEGER,
        views INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    '''

    # Execute the SQL command
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def insert_data(title, text, type_, tags):
    # Connect to the database
    conn = sqlite3.connect('all.db')
    cursor = conn.cursor()

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # SQL query to insert data
    insert_query = '''
    INSERT INTO me_text (id, title, text, type, tags, active, views, timestamp)
    VALUES (?, ?, ?, ?, ?, 1, 0, CURRENT_TIMESTAMP);
    '''

    # Execute the SQL command
    try:
        cursor.execute(insert_query, (unique_id, title or None, text or None, type_ or None, tags or None))
        conn.commit()
        print("Data entered successfully.")
    except sqlite3.IntegrityError as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

def main():
    # Create the table if it doesn't exist
    create_table_if_not_exists()

    while True:
        # Prompt for user input
        title = input("Enter title (or press Enter to skip): ")
        text = input("Enter text (or press Enter to skip): ")
        type_ = input("Enter type (or press Enter to skip): ")
        tags = input("Enter tags (comma separated, or press Enter to skip): ")

        # Insert data into the database
        insert_data(title, text, type_, tags)

        # Ask if the user wants to add another record
        another = input("Do you want to add another record? (y/n): ")
        if another.lower() != 'y':
            break

if __name__ == "__main__":
    main()