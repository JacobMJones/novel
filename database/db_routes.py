from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='images')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder, filename)
# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/texts')
@cross_origin(origins=["http://192.168.32.1:3000"], headers=["application/json"]) 
def get_texts():
    print('in get')
    conn = get_db_connection()
    texts = conn.execute('SELECT * FROM text_all').fetchall() 
    conn.close()
    response = jsonify([dict(row) for row in texts])
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response

# Function to create a table (if you need a specific table apart from the Excel import)
def create_table():
    conn = get_db_connection()
    # Example table creation
    conn.execute('''CREATE TABLE IF NOT EXISTS example_table (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
    conn.commit()
    conn.close()

# Function to import Excel file into the SQLite database
# curl -X POST -F "file=@C:\Users\Personal\Code\novella\novella\pythonserver\image_data.xlsx" http://localhost:5000/import_excel

@app.route('/import_excel', methods=['POST'])
def import_excel():
    file = request.files['file']
    df = pd.read_excel(file)
    conn = get_db_connection()
    # Replace 'excel_data' with your desired table name and adjust the `if_exists` parameter if needed
    df.to_sql('excel_data', conn, if_exists='replace', index=False)
    conn.close()
    return {'message': 'Excel data imported successfully'}, 201


# Route to fetch all data from the excel_data table
@app.route('/image_data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM image_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


if __name__ == '__main__':
    create_table()  # Call this function if you need to create an initial table
    app.run(debug=True, host='0.0.0.0', port=5000)