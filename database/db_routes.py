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

@app.route('/deactivate_image', methods=['POST'])
def deactivate():
    print('in deactivate')
    # Extract data from request
    data = request.get_json()
    if data:
        # Perform your logic here, e.g., updating the database
        # For example, if you're deactivating an image by its ID:
        # id = data.get('id')
        # active = data.get('active')
        # ... update database logic ...

        print(f"Deactivated data: {data}")
        # Return a success response
        return jsonify({'status': 'success', 'message': 'Image deactivated'}), 200
    else:
        # Return an error response if no data is received
        return jsonify({'status': 'error', 'message': 'No data received'}), 400

@app.route('/texts', methods=['GET'])
def get_texts():
    print('in get')
    conn = get_db_connection()
    texts = conn.execute('SELECT * FROM text_all').fetchall() 
    conn.close()
    return jsonify([dict(row) for row in texts])

# Route to fetch all image data
@app.route('/image_data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM new_image_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)