from flask import Flask, jsonify, make_response
from backend.ml.ml_app import train_model, predict_output

app = Flask(__name__)

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
    response = make_response(jsonify(sample_response))

    # Add Access-Control-Allow-Origin header to allow cross-site request
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

    return response

@app.route('/receive_predictions', methods=['POST', 'GET'])
def receive_predictions():
    output = predict_output(model)
    return jsonify(output)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
