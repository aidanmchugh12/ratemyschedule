from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import pandas as pd
import numpy as np

# Other python functions
from csv_parse import make_csv
from rmp_grading import getProfGrades

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

@app.route('/api/input', methods=['GET'])
def csv_to_array():
    try:
        # Load the CSV file
        df = pd.read_csv('schedule.csv')

        df_unique = df.drop_duplicates(subset=['class_id'])

        # Change null values to none to properly jsonify 2d array
        df_unique = df_unique.applymap(lambda x: None if pd.isna(x) else x)

        unique_array = df_unique.values.tolist()
        return jsonify(unique_array)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/input', methods=['POST'])
def data_into_csv():
    print("TEST!")
    data_input = request.get_json()
    
    if not data_input:
        return jsonify({'error': 'No data provided'}), 400
    
    df = pd.read_csv('schedule.csv')

    # split data_input into class names, professors, and credits
    class_names = data_input['classes'][0]
    class_profs = data_input['classes'][1]
    class_credits = data_input['classes'][2]
    
    # generate a set to keep track of updated classes in csv
    updated_classes = set()
    
    # loop through the dataframe to update professor and credits columns
    for index, class_id in enumerate(df['class_id']):
        # check if class_id matches any class from the array class names
        if class_id in class_names:
            # if  class hasn't been updated yet
            if class_id not in updated_classes:
                # get the index of the class in class_names
                class_index = class_names.index(class_id)

                # update the professor and credits columns
                df.at[index, 'professor'] = class_profs[class_index]
                df.at[index, 'credits'] = class_credits[class_index]

                # mark the class as updated
                updated_classes.add(class_id)
            else:
                # for duplicate classes, set professor and credits to nan
                df.at[index, 'professor'] = np.nan
                df.at[index, 'credits'] = np.nan
        else:
            # if the class_id is not found in class_names leave it
            pass

    # save the df back to the csv file
    df.to_csv('schedule.csv', index=False)
    return jsonify({'message': 'CSV updated successfully!'}), 200

@app.route('/api/output', methods=['GET'])
def get_grading_results():
    
    csv_file = 'schedule.csv'
    
    data = {
        "overallGrade": "",
        "overallGradeBlurb": "",
        "classBreaks": 0,
        "classBreaksBlurb": "",
        "profRating": 0,
        "profRatingBlurb": "",
        "creditsTaken": 0,
        "creditsTakenBlurb": "",
    }
    
    # data['classBreaks'] = breakFunction
    
    
    
    return 


if __name__ == '__main__':
    app.run(debug=True)
