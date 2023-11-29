from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import pandas as pd
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='images')
CORS(app, resources={r"/*": {"origins": "*"}})
color_names = {
    "Red": (255, 0, 0),
    "Green": (0, 128, 0),
    "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0),
    "Orange": (255, 165, 0),
    "Purple": (128, 0, 128),
    "Pink": (255, 192, 203),
    "Brown": (165, 42, 42),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray": (128, 128, 128),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),
    "Lime": (0, 255, 0),
    "Maroon": (128, 0, 0),
    "Olive": (128, 128, 0),
    "Navy": (0, 0, 128),
    "Teal": (0, 128, 128),
    "Aqua": (0, 255, 255),
    "Fuchsia": (255, 0, 255),
    "Silver": (192, 192, 192),
    "Gold": (255, 215, 0),
    "Beige": (245, 245, 220),
    "Coral": (255, 127, 80),
    "Ivory": (255, 255, 240),
    "Khaki": (240, 230, 140),
    "Lavender": (230, 230, 250),
    "Mint": (189, 252, 201),
    "Navy Blue": (0, 0, 128),
    "Tomato": (255, 99, 71)
}
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder, filename)
# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('all.db')
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
                conn.execute('UPDATE image_data SET active = 0 WHERE id = ?', (id,))
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
    texts = conn.execute('SELECT * FROM me_text').fetchall() 
    conn.close()
    return jsonify([dict(row) for row in texts])

# Route to fetch all image data
@app.route('/image_data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM image_data').fetchall()
    conn.close()
    return jsonify([dict(row) for row in data])

# Route to add tag
@app.route('/add_tag', methods=['POST'])
def add_tag():

    data = request.get_json()
    if data:
        id = data.get('id')
        new_tag = data.get('tag')
        print(id, new_tag)
        if id is not None and new_tag:
            conn = get_db_connection()
            try:
                # Fetch current tags
                current_tags = conn.execute('SELECT tags FROM image_data WHERE id = ?', (id,)).fetchone()
                if current_tags:
                    updated_tags = f"{current_tags['tags']},{new_tag}"
                    # Update record with new tags
                    conn.execute('UPDATE image_data SET tags = ? WHERE id = ?', (updated_tags, id))
                    conn.commit()
                    response = {'status': 'success', 'message': 'Tag added'}
                    status_code = 200
                else:
                    response = {'status': 'error', 'message': 'Record not found'}
                    status_code = 404
            except sqlite3.Error as e:
                response = {'status': 'error', 'message': f'Database error: {e}'}
                status_code = 500
            finally:
                conn.close()
        else:
            response = {'status': 'error', 'message': 'Invalid ID or tag'}
            status_code = 400
    else:
        response = {'status': 'error', 'message': 'No data received'}
        status_code = 400

    return jsonify(response), status_code

@app.route('/update_color', methods=['POST'])
def update_color():

    data = request.get_json()
    if data:
        id = data.get('id')
        new_color = data.get('color')
        new_color_rgb = data.get('color_rgb')

        if id is not None and new_color:
            conn = get_db_connection()
            try:
                # Fetch current tags

                if new_color:
                 
                    # Update record with new tags
                    conn.execute('UPDATE image_data SET color = ?, color_rgb = ? WHERE id = ?', (new_color, new_color_rgb, id))
                    conn.commit()
                    response = {'status': 'success', 'message': 'Tag added'}
                    status_code = 200
                else:
                    response = {'status': 'error', 'message': 'Record not found'}
                    status_code = 404
            except sqlite3.Error as e:
                response = {'status': 'error', 'message': f'Database error: {e}'}
                status_code = 500
            finally:
                conn.close()
        else:
            response = {'status': 'error', 'message': 'Invalid ID or tag'}
            status_code = 400
    else:
        response = {'status': 'error', 'message': 'No data received'}
        status_code = 400

    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)