import sqlite3

# Connect to SQLite database (this will create the file if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a query
cursor.execute("ALTER TABLE excel_data RENAME TO image_data")

# Commit the changes
conn.commit()

# Close the connection
conn.close()