from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Load your analysis data
econ_data = pd.read_csv('../../docs/Economid_data.csv')
tech_data = pd.read_csv('../../docs/technological_data.csv')


@app.route('/api/econ_data', methods=['GET'])
def get_econ_data():
    return jsonify(econ_data.to_dict(orient='records'))

@app.route('/api/tech_data', methods=['GET'])
def get_tech_data():
    return jsonify(tech_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
