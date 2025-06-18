from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
import pandas as pd
import numpy as np

# CSV parser & grading functions
from utils.pdf_converter import convert_to_json
from metrics.walking_distance import getWalkTime
from generate_report import generate_report

# Database connection
from utils.db import users_collection, pitt_walktimes_collection

app = Flask(__name__)
CORS(app)


# CHECKS IF USER EXSITS IN DATABASE, returns true or false
@app.route('/api/check-user', methods=['POST'])
def check_user():
    data = request.get_json()
    
    if not data or "sub" not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = users_collection.find_one({"sub": data["sub"]})
    
    if not user:
        return jsonify({"exists": False}), 200
    
    return jsonify({"exists": True}), 200


# ADDS USER TO DATABASE
@app.route('/api/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    if not data or "sub" not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = users_collection.find_one({"sub": data["sub"]})
    
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    new_user = {
        "sub": data["sub"], # Auth0 unique identifier
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "created_at": data.get("created_at", ""),
        "SavedData": []
    }
    
    users_collection.insert_one(new_user)
    
    return jsonify({'message': 'User added successfully!'}), 200


# SAVES REPORT TO DATABASE for a specific user
@app.route('/api/save-report', methods=['POST'])
def save_report():
    data = request.get_json()
    
    if not data or "sub" not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = users_collection.find_one({"sub": data["sub"]})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    users_collection.update_one({"sub" : data["sub"]}, {"$push" : {"SavedData" : data["report"]}})
    
    return jsonify({'message': 'Data added to SavedData successfully!'}), 200


# GETS ALL REPORTS FROM DATABASE for a specific user
@app.route('/api/get-reports', methods=['POST'])
def get_reports():
    data = request.get_json()
    
    if not data or "sub" not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    user = users_collection.find_one({"sub": data["sub"]})
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    reports = user.get("SavedData", [])
    
    return jsonify({'saved_data': reports}), 200


# TAKES IN FILE, CONVERTS TO JSON, 
@app.route('/api/upload', methods=['POST'])
def upload():
    if "file" not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Pass the file to the converter
        json_data = convert_to_json(file)

        # Check if the conversion returned an error
        if isinstance(json_data, dict) and "error" in json_data:
            return jsonify({'error': json_data["error"]}), 500

        return jsonify({'reportData': json_data}), 200

    except Exception as e:
        print(f"Error during upload: {e}")
        return jsonify({'error': 'Failed to process file'}), 500


@app.route('/api/generate-new-report', methods=['POST'])
def generate_new_report():
    data = request.get_json()
    
    if not data or "scheduleData" not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Debug print
    #print("Received data:", data["scheduleData"])

    report = generate_report(json.loads(data["scheduleData"]), "REPORT NAME")
    return jsonify({"report": report}), 200


@app.route('/api/get-pitt-locations', methods=['GET'])
def get_pitt_locations():
    try:
        pitt_walktime_data = pitt_walktimes_collection.find()
        
        return jsonify({"walkTimeData" : pitt_walktime_data}), 200
    
    except Exception as e:
        return jsonify({"error" : "Failed to grab walktime data"}), 400
    

@app.route('/api/add-pitt-walk', methods=['POST'])
def add_pitt_walk():
    
    data = request.get_json()
    if not data or "from" not in data or "to" not in data:
        return jsonify({"error": "Missing 'from' or 'to' in request"}), 400

    entry = {
        "from": data["from"],
        "to": data["to"],
        "walktime": ""
    }
    
    try:
        
        entry["walktime"] = getWalkTime(entry["from"], entry["to"])
        
        pitt_walktimes_collection.insert_one(entry)
        
        return jsonify({"message" : "Data added successfully!"}), 200
    except Exception as e:
        return jsonify({"error" : "Failed to grab walktime data"}), 400

if __name__ == '__main__':
    app.run(debug=True)
