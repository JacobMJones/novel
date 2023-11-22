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
    data = request.get_json()
    print(data)
    if data:
        id = data.get('id')
        # Ensure you have a valid id and active value
        if id is not None:
            conn = sqlite3.connect('database.db')
            try:
                conn.execute('UPDATE new_image_data SET active = 0 WHERE id = ?', (id,))
                conn.commit()
                print(f"Deactivated data: {data}")
                response = {'status': 'success', 'message': 'Image deactivated'}
                status_code = 200
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                response = {'status': 'error', 'message': 'Database error'}
                status_code = 500
            finally:
                conn.close()
        else:
            response = {'status': 'error', 'message': 'Invalid ID'}
            status_code = 400
    else:
        response = {'status': 'error', 'message': 'No data received'}
        status_code = 400

    return jsonify(response), status_code

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