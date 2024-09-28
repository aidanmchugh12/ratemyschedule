from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    print(f"Received: {data}")
    return jsonify({"status": "success", "received": data})

if __name__ == '__main__':
    app.run(debug=True)
