# ECM3401 Final Project by Ethan Gallagher - ML

## Description
This is the web application developed for ECM3401 Final Project, with the accompanying paper titled "A Comparative Analysis of Convolutional Neural Network Architectures for Diagnosing Diabetic Retinopathy".

This file details the information regarding the main machine learning code for the backend section of the codebase, with information on functionality.

## Table of Contents
- [Files](#files)
- [Model Logs](#model-logs)
- [Saved Models](#saved-models)
- [Unused Code](#unused-code)
- [Functionality](#functionality)

## Files

- colab.ipynb
    - Contains all of the training and testing code used in the Google Colab environment
- ml_app.py
    - Contains the functionality to get an image diagnosis from an uploaded image from the frontend, as well as the functionality to get all the saved models

## Model Logs

This folder contains the .rtf files of the training and testing outputs from the Colab notebook and is used to create the model analysis page on the frontend. It also contains some processing files relating to that data.

- misclassification.py
    - Calculates misclassifications for a models testing
- parse_model_epochs.py
    - Parses the training data for each model into JSON serialisable Python objects for the frontend to read
- parse_model_results.py
    - Parses the testing data for each model into JSON serialisable Python objects for the frontend to read
- ttest.py
    - Carries out statistical t-tests for the training data for each model

## Saved Models

This folder contains all of the trained .keras models, ready to be used by the frontend.

## Unused Code

This folder contains any code that is no longer used, mainly from the first two stages of development outlined in the main paper.

## Functionality

The following bullet points outline each part of the APIs functionality, which is detailed further in the commenting in the actual file.

- Loading the model logs
    - The training and testing outputs from Colab are saved and parsed into Python objects in the ML folder. These objects are then loaded into the API to send in the functionality described below
- Image diagnosis
    - The frontend sends a request with the user selected model and image, which is then given to the processing functions to get a diagnosis, which is then sent back to the frontend
- Model analysis
    - The frontend sends over all the Python objects made from parsing the log files with each model having training and testing information
- Loading saved models
    - The API sends the frontend any saved models in the specific directory in the backend

## Usage
This repository is only permitted for use by the markers of ECM3401.
## Contact
If there are any issues, please contact me via the following:
- Email - eg546@exeter.ac.uk
