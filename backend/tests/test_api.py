import pytest
from flask_testing import TestCase
from api.app import app  # Import your Flask app
from io import BytesIO
import os

class TestFlaskApi(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.valid_model_name = 'densenet.keras'
        self.invalid_model_name = 'dafwoieh.keras'
        self.selected_models = 'mobilenet.keras,resnet.keras'
        
        self.image_path = '/Users/ethan/Downloads/Messidor2/train/1/IM001110.jpg'
        self.image_filename = os.path.basename(self.image_path)

        with open(self.image_path, 'rb') as image_file:
            self.image_data = image_file.read()

    def test_receive_predictions(self):
        response = self.client.post('/receive_predictions', data={
            'selectedOption': self.valid_model_name,
            'selectedFile': (BytesIO(self.image_data), self.image_filename)
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)

    def test_get_model_analysis(self):
        response = self.client.post('/get_model_analysis', data={
            'models': self.selected_models
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)

    def test_get_saved_models(self):
        response = self.client.get('/get_saved_models')
        self.assertEqual(response.status_code, 200)

    def test_receive_predictions_missing_data(self):
        response = self.client.post('/receive_predictions', data={
            'selectedOption': self.valid_model_name,
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

        response = self.client.post('/receive_predictions', data={
            'selectedFile': (self.image_data, self.image_filename)
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_receive_predictions_invalid_model(self):
        response = self.client.post('/receive_predictions', data={
            'selectedOption': self.invalid_model_name,
            'selectedFile': (self.image_data, self.image_filename)
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_get_model_analysis_invalid_models(self):
        response = self.client.post('/get_model_analysis', data={
            'models': 'invalidmodel1.keras,invalidmodel2.keras'
        }, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)

    def test_receive_predictions_unsupported_method(self):
        response = self.client.get('/receive_predictions')
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    pytest.main()
