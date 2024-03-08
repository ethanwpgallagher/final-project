import base64
from io import BytesIO
import logging
import sys
import cv2
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from ml.ml_app import get_prediction, get_saved_model
import numpy as np
from ml.preprocessing import preprocessing

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)

@app.route('/receive_predictions', methods=['POST'])
def receive_predictions():
    try:
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
        else:
            selected_model = request.form.get('selectedOption')

            selected_file = request.files.get('selectedFile')
            
            if not (selected_model and selected_file):
                raise ValueError("Invalid input format. 'selectedOption' and 'selectedFile' are required.")

            image_bytes = selected_file.read()

            # Decode base64 image (if needed)
            # image_bytes = base64.b64decode(image_bytes)

            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
            image = image.reshape(224, 224, 1)
            image = np.repeat(image, 3, axis=-1)
            print(image.shape, file=sys.stderr)
            # image = preprocessing(image, (224, 224), False)

            model = get_saved_model(selected_model)
            if model is not None:
                diagnosis = get_prediction(model, image).tolist()
                predicted_class = get_class_from_probabilities(diagnosis[0])
                response = jsonify({'diagnosis': predicted_class})
            else:
                response = jsonify({'error': 'Invalid model selected.'})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        response = jsonify({'error': str(e)})

    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Allow Content-Type header
    response.status_code = 200

    # Log the response content before returning
    response_content = response.get_data(as_text=True)
    app.logger.debug(f"Response content: {response_content}")

    return response

def get_class_from_probabilities(probabilities):
    print(probabilities, file=sys.stderr)
    predicted_index = np.argmax(probabilities)
    class_labels = ['0', '1', '2', '3', '4']
    return class_labels[predicted_index]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
