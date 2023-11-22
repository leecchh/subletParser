from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

@app.route('/get-data')
def get_data():
    data = []
    with open('listings.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)