from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from csv_parse import make_csv

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/submit', methods=['POST'])
def upload_file():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # If no file is selected
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the upload folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Use csv_parse to convert to csv 
    make_csv(file_path)

    return jsonify({'message': 'File uploaded successfully!', 'file_path': file_path}), 200

@app.route('/api/test', methods=['GET'])
def csv_to_array():
    # implement code here
    return #2d array

if __name__ == '__main__':
    app.run(debug=True)
