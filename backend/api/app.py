import logging
import sys
import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
from ml.ml_app import get_prediction, get_saved_model, get_saved_model_names
from ml.model_logs import parse_model_epochs, parse_model_results
import numpy as np
import os

app = Flask(__name__)
CORS(app)
app.logger.setLevel(logging.DEBUG)
epoch_log_parsers = parse_model_epochs.load_logs_from_directory(os.path.dirname(os.path.dirname(__file__)))
result_log_parsers = parse_model_results.load_logs_from_directory(os.path.dirname(os.path.dirname(__file__)))
serialized_results = {model_name: parser.__json__() for model_name, parser in result_log_parsers.items()}

@app.route('/receive_predictions', methods=['POST'])
def receive_predictions():
    try:
        selected_model = request.form.get('selectedOption')

        selected_file = request.files.get('selectedFile')
        
        if not (selected_model and selected_file):
            app.logger.error("Invalid input format. 'selectedOption' and 'selectedFile' are required.")
            return jsonify({'error': "Invalid input format. 'selectedOption' and 'selectedFile' are required."}), 400


        image_bytes = selected_file.read()

        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.addWeighted(image, 4, cv2.GaussianBlur(image, (0,0), 10), -4, 128)
        img = cv2.resize(img, (224, 224))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.medianBlur(image, 5)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        image = clahe.apply(image)
        image = cv2.resize(image, (224, 224))
        image = np.stack((image,)*3, axis=-1)
        print(image.shape, file=sys.stderr)

        model = get_saved_model(str(selected_model))
        if model is not None:
            diagnosis = get_prediction(model, image).tolist()
            predicted_class = get_class_from_probabilities(diagnosis[0])
            response = jsonify({'diagnosis': predicted_class})
        else:
            response = jsonify({'error': 'Invalid model selected.'})
    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500 

    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.status_code = 200

    response_content = response.get_data(as_text=True)
    app.logger.debug(f"Response content: {response_content}")

    return response

@app.route('/get_model_analysis', methods=['POST'])
def get_model_analysis():
    try:
        selected_models = request.form.get('models').split(',')
        if not selected_models:
            return jsonify({'error': "Invalid input format. 'models' not set"}), 500
        epoch_return = {}
        result_return = {}
        for name in selected_models:
            name = name.split('.')[0]
            if name not in epoch_log_parsers.keys() or name not in serialized_results.keys():
                return jsonify({'error': "Invalid models"}), 400
            epoch_return[name] = epoch_log_parsers[name]
            result_return[name] = serialized_results[name]
        response = jsonify({'epoch_data': epoch_return, 'result_data': result_return})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.status_code = 200
        return response
    except Exception as e:
        print(e, file=sys.stderr)
        return jsonify({'error': str(e)}), 500

@app.route('/get_saved_models', methods=['GET'])
def get_saved_models():
    try:
        saved_models = get_saved_model_names()
        return jsonify(saved_models)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_class_from_probabilities(probabilities):
    print(probabilities, file=sys.stderr)
    predicted_index = np.argmax(probabilities)
    class_labels = ['0', '1', '2', '3', '4']
    return class_labels[predicted_index]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
