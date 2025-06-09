# A simple restful API
from flask import Flask, jsonify

app = Flask(__name__)

# Define a route for the API
@app.route('/api/data', methods=['GET'])
def get_data():
    # Return some sample data in JSON format
    return jsonify({'data': 'Sample Data'})

if __name__ == '__main__':
    app.run(debug=True)
