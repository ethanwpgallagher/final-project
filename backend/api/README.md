# ECM3401 Final Project by Ethan Gallagher - API

## Description
This is the web application developed for ECM3401 Final Project, with the accompanying paper titled "A Comparative Analysis of Convolutional Neural Network Architectures for Diagnosing Diabetic Retinopathy".

This file details the information regarding the API for the codebase, with information on functionality.

## Table of Contents
- [Functionality](#functionality)

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
