import sqlite3

def test_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Print schema
    cursor.execute("PRAGMA table_info(text_all);")
    columns = cursor.fetchall()
    print("Schema:", columns)

    # Fetch some data
    cursor.execute("SELECT * FROM text_all WHERE subtype = 'tao' LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

test_database()
