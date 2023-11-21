import sqlite3

def delete_poetry_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS text_all;")
    conn.commit()

    print("Table 'text_all' has been deleted.")

    conn.close()

delete_poetry_table()
