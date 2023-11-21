from flask import Flask, jsonify, send_file,send_from_directory, request, redirect, url_for
from flask_cors import CORS, cross_origin
import pandas as pd
import os
import time


app = Flask(__name__, static_folder='images')
CORS(app, resources={r"/*": {"origins": "*"}})
UPLOAD_FOLDER = './' 
ALLOWED_EXTENSIONS = {'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(app.static_folder, filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/<filename>')
def download_file(filename):
    if filename not in ['image_data.xlsx', 'text_data.xlsx']:
        return "File not found.", 404
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

@app.route('/<filename>', methods=['GET', 'POST'])
def upload_file(filename):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'{filename} updated successfully'


@app.route('/update_excel', methods=['POST'])
@cross_origin()
def update_excel():
    print('in update excel')
    data = request.json
    print('DATA%%%', data)
    id = data['id']
    active = data['active']
    type = data['type']

    try:
        # Load the Excel file
        if(type=='image'):
            df = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'image_data.xlsx'))
            df.loc[df['id'] == id, 'active'] = active
            df.to_excel(os.path.join(UPLOAD_FOLDER, 'image_data.xlsx'), index=False)
        elif(type=='text'):
            df = pd.read_excel(os.path.join(UPLOAD_FOLDER, 'text_data.xlsx'))
            df.loc[df['id'] == id, 'active'] = active
            df.to_excel(os.path.join(UPLOAD_FOLDER, 'text_data.xlsx'), index=False)


        return jsonify({"message": f"{id} updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error updating the file: {e}"}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
