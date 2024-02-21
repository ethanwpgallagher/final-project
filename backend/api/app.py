from flask import Flask, jsonify, make_response
from flask_cors import CORS
from ml.ml_app import train_model, predict_output

app = Flask(__name__)
CORS(app)
model = train_model()

@app.route('/api/v1.0/test', methods=['GET'])
def test_response():
    """Return a sample JSON response."""
    sample_response = {
        "items": [
            { "id": 1, "name": "Apples",  "price": "$2" },
            { "id": 2, "name": "Peaches", "price": "$5" }
        ]
    }
    # JSONify response
    response = jsonify(sample_response)

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return response

@app.route('/receive_predictions', methods=['POST', 'GET'])
def receive_predictions():
    output = jsonify(predict_output(model))
    output.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return output

@app.route('/', methods=["POST", "GET"])
def main_page():
    response = jsonify("<p>Hello, World!</p>")
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
